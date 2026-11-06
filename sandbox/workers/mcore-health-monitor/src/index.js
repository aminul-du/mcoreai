/**
 * MCORE-DOCS-001 §3 — Health Check Monitor Worker
 * Scheduled cron that pings all tunnel services, stores results in KV.
 * Deployed as: mcore-health-monitor
 * Cron: every 5 minutes
 */

const SERVICES = [
  { name: "ais001-dev",     url: "https://ais001.mcoreai.dev",     expected: 200 },
  { name: "api-policy",     url: "https://api.mcoreai.dev",       expected: 200 },
  { name: "docs-ui",        url: "https://docs.mcoreai.dev",      expected: 200 },
  { name: "ssh-tunnel",     url: "https://ssh.mcoreai.dev",        expected: 200 },
  { name: "app-mcoreai",    url: "https://app.mcoreai.dev",        expected: 200 },
];

export default {
  // Cron trigger
  async scheduled(event, env, ctx) {
    ctx.waitUntil(runHealthChecks(env));
  },

  // HTTP endpoint for status dashboard
  async fetch(request, env) {
    const url = new URL(request.url);

    if (url.pathname === "/status") {
      const results = await getStoredResults(env);
      return jsonResponse(results);
    }

    if (url.pathname === "/status/run") {
      const results = await runHealthChecks(env);
      return jsonResponse(results);
    }

    if (url.pathname === "/__health") {
      return jsonResponse({ status: "healthy", service: "mcore-health-monitor" });
    }

    return jsonResponse({ error: "Use /status or /status/run" }, 404);
  },
};

async function runHealthChecks(env) {
  const results = [];
  const timestamp = new Date().toISOString();

  for (const svc of SERVICES) {
    const start = Date.now();
    try {
      const resp = await fetch(svc.url, {
        method: "HEAD",
        redirect: "manual", // Don't follow Access redirects
        signal: AbortSignal.timeout(5000),
      });
      const latency = Date.now() - start;
      const healthy = resp.status === svc.expected || resp.status === 302; // 302 = Access redirect (expected)

      results.push({
        name: svc.name,
        url: svc.url,
        status: resp.status,
        healthy,
        latency_ms: latency,
        timestamp,
      });
    } catch (e) {
      results.push({
        name: svc.name,
        url: svc.url,
        status: 0,
        healthy: false,
        latency_ms: Date.now() - start,
        error: e.message,
        timestamp,
      });
    }
  }

  // Store in KV
  if (env.MCORE_KV) {
    await env.MCORE_KV.put("health:latest", JSON.stringify(results), { expirationTtl: 3600 });
    await env.MCORE_KV.put(`health:${timestamp}`, JSON.stringify(results), { expirationTtl: 86400 });
  }

  return results;
}

async function getStoredResults(env) {
  if (!env.MCORE_KV) {
    return { error: "KV not bound", hint: "Run /status/run to check live" };
  }
  const data = await env.MCORE_KV.get("health:latest");
  if (!data) {
    return { message: "No cached results yet", hint: "Run /status/run to check now" };
  }
  return JSON.parse(data);
}

function jsonResponse(data, status = 200) {
  return new Response(JSON.stringify(data, null, 2), {
    status,
    headers: {
      "Content-Type": "application/json",
      "Access-Control-Allow-Origin": "*",
    },
  });
}
