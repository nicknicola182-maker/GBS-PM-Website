export interface Env {
  AI: Ai;
}

interface ChatMessage {
  role: "system" | "user" | "assistant";
  content: string;
}

interface InferenceRequest {
  messages?: ChatMessage[];
  prompt?: string;
  model?: string;
  max_tokens?: number;
  temperature?: number;
  stream?: boolean;
}

export default {
  async fetch(request: Request, env: Env): Promise<Response> {
    // Handle CORS preflight
    if (request.method === "OPTIONS") {
      return new Response(null, {
        headers: {
          "Access-Control-Allow-Origin": "*",
          "Access-Control-Allow-Methods": "POST, OPTIONS",
          "Access-Control-Allow-Headers": "Content-Type",
        },
      });
    }

    if (request.method !== "POST") {
      return Response.json(
        { error: "Method not allowed. Use POST." },
        { status: 405 }
      );
    }

    try {
      const body: InferenceRequest = await request.json();

      // Build messages array
      const messages: ChatMessage[] = body.messages ?? [
        { role: "system", content: "You are a helpful assistant." },
        { role: "user", content: body.prompt ?? "Hello!" },
      ];

      // Model selection (default to Llama 3.3 70B)
      const model = body.model ?? "@cf/meta/llama-3.3-70b-instruct-fp8-fast";

      // Check if streaming is requested (default: true)
      const shouldStream = body.stream !== false;

      if (shouldStream) {
        // Streaming response using SSE
        const stream = (await env.AI.run(model, {
          messages,
          stream: true,
          max_tokens: body.max_tokens ?? 1024,
          temperature: body.temperature ?? 0.7,
        })) as unknown as ReadableStream;

        return new Response(stream, {
          headers: {
            "Content-Type": "text/event-stream",
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "Access-Control-Allow-Origin": "*",
          },
        });
      } else {
        // Non-streaming response
        const response = await env.AI.run(model, {
          messages,
          max_tokens: body.max_tokens ?? 1024,
          temperature: body.temperature ?? 0.7,
        });

        return Response.json(response, {
          headers: { "Access-Control-Allow-Origin": "*" },
        });
      }
    } catch (err) {
      const message = err instanceof Error ? err.message : "Unknown error";
      return Response.json({ error: message }, { status: 500 });
    }
  },
} satisfies ExportedHandler<Env>;
