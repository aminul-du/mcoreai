/**
 * Cloudflare Workers AI Edge Inference Service
 * Model: @cf/meta/llama-3-8b-instruct
 */

export default {
  async fetch(request, env, ctx) {
    const url = new URL(request.url);

    // Health check endpoint
    if (url.pathname === "/health" || url.pathname === "/") {
      if (request.method === "GET") {
        return new Response(
          JSON.stringify({
            status: "healthy",
            service: "cf-ai-worker",
            model: "@cf/meta/llama-3-8b-instruct",
            timestamp: new Date().toISOString()
          }),
          {
            headers: {
              "Content-Type": "application/json",
              "Cache-Control": "no-cache"
            }
          }
        );
      }
    }

    // Only allow POST for inference requests
    if (request.method !== "POST") {
      return new Response(
        JSON.stringify({ error: "Method not allowed. Send a POST request with a JSON body." }),
        {
          status: 405,
          headers: { "Content-Type": "application/json" }
        }
      );
    }

    try {
      const body = await request.json().catch(() => ({}));
      const prompt = body.prompt || "Hello! Provide a brief summary of Cloudflare Workers AI.";
      const systemPrompt =
        body.system ||
        "You are an edge AI assistant running on Cloudflare Workers AI. Answer accurately and concisely.";

      const aiResponse = await env.AI.run("@cf/meta/llama-3-8b-instruct", {
        messages: [
          { role: "system", content: systemPrompt },
          { role: "user", content: prompt }
        ]
      });

      return new Response(
        JSON.stringify({
          success: true,
          model: "@cf/meta/llama-3-8b-instruct",
          data: aiResponse
        }),
        {
          headers: { "Content-Type": "application/json" }
        }
      );
    } catch (error) {
      return new Response(
        JSON.stringify({
          success: false,
          error: error.message || "Failed to execute model inference at the edge"
        }),
        {
          status: 500,
          headers: { "Content-Type": "application/json" }
        }
      );
    }
  }
};
