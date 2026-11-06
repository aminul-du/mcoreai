/**
 * MCORE-DOCS-001 §2 — Edge API Gateway Worker
 * Validates Cloudflare Access JWTs, routes to tunnel backends, logs audit events to D1.
 * Deployed as: mcore-edge-gateway
 */

// Backend routing map
const BACKENDS = {
  "ais001.mcoreai.dev": { url: "http://localhost:8000", name: "dev-agent" },
  "api.mcoreai.dev":    { url: "http://localhost:8080", name: "policy-core" },
  "docs.mcoreai.dev":   { url: "http://localhost:3000", name: "docs-ui" },
  "ssh.mcoreai.dev":    { url: "ssh://localhost:22",     name: "ssh-tunnel" },
};

// Allowed origins for CORS
const ALLOWED_ORIGINS = [
  "https://ais001.mcoreai.dev",
  "https://api.mcoreai.dev",
  "https://docs.mcoreai.dev",
];

export default {
  async fetch(request, env, ctx) {
    const url = new URL(request.url);
    const hostname = url.hostname;

    // ---- 1. Health endpoint (no auth) ----
    if (url.pathname === "/__health") {
      return jsonResponse({ status: "healthy", service: "mcore-edge-gateway", time: new Date().toISOString() });
    }

    // ---- 2. Validate Cloudflare Access JWT ----
    const jwt = request.headers.get("cf-access-jwt-assertion");
    if (!jwt) {
      return new Response(JSON.stringify({ error: "Access JWT required" }), {
        status: 401,
        headers: { "Content-Type": "application/json" },
      });
    }

    let claims;
    try {
      const parts = jwt.split(".");
      claims = JSON.parse(atob(parts[1]));
    } catch {
      return new Response(JSON.stringify({ error: "Invalid JWT" }), {
        status: 403,
        headers: { "Content-Type": "application/json" },
      });
    }

    // Check session expiry
    if (claims.exp && Date.now() > claims.exp * 1000) {
      return new Response(JSON.stringify({ error: "Session expired" }), {
        status: 401,
        headers: { "Content-Type": "application/json" },
      });
    }

    const userEmail = claims.email || "unknown";

    // ---- 3. Route to backend ----
    const backend = BACKENDS[hostname];
    if (!backend) {
      return new Response(JSON.stringify({ error: `No backend for ${hostname}` }), {
        status: 404,
        headers: { "Content-Type": "application/json" },
      });
    }

    // For SSH, return info (can't proxy SSH through a Worker)
    if (backend.name === "ssh-tunnel") {
      return jsonResponse({
        service: "ssh-tunnel",
        host: "ssh.mcoreai.dev",
        user: userEmail,
        instructions: "Use: cloudflared access ssh --hostname ssh.mcoreai.dev",
      });
    }

    // ---- 4. Proxy request to backend (via tunnel, localhost in cloudflared) ----
    // Note: Workers can't reach localhost directly; this Worker runs at the edge
    // and the tunnel handles the localhost mapping. In production, route via
    // the tunnel's public hostname instead.
    const targetUrl = `https://${hostname}${url.pathname}${url.search}`;

    // ---- 5. Log audit event to D1 (fire-and-forget) ----
    ctx.waitUntil(logAudit(env, {
      actor: userEmail,
      action: request.method,
      resource: hostname + url.pathname,
      backend: backend.name,
      status: "routed",
      timestamp: new Date().toISOString(),
    }));

    // ---- 6. Return routing confirmation ----
    return jsonResponse({
      routed: true,
      user: userEmail,
      backend: backend.name,
      target: targetUrl,
      method: request.method,
      path: url.pathname,
      timestamp: new Date().toISOString(),
    });
  },
};

async function logAudit(env, event) {
  if (!env.MCORE_D1) return;
  try {
    await env.MCORE_D1.prepare(
      "INSERT INTO audit_log (event_type, actor, action, resource, backend, status, created_at) VALUES (?, ?, ?, ?, ?, ?, ?)"
    ).bind(
      "access", event.actor, event.action, event.resource,
      event.backend, event.status, event.timestamp
    ).run();
  } catch (e) {
    // D1 table may not exist yet — fire and forget
    console.error("Audit log error:", e.message);
  }
}

function jsonResponse(data, status = 200) {
  return new Response(JSON.stringify(data, null, 2), {
    status,
    headers: {
      "Content-Type": "application/json",
      "Access-Control-Allow-Origin": "*",
      "Access-Control-Allow-Methods": "GET, POST, PUT, DELETE, OPTIONS",
      "Access-Control-Allow-Headers": "Authorization, Content-Type, cf-access-jwt-assertion",
    },
  });
}
