# Workers AI Streaming Endpoint

A serverless AI inference API built on Cloudflare Workers AI with real-time streaming responses.

## Live Endpoint

```
https://ai-inference.nicknicola182.workers.dev
```

## Features

- **Streaming responses** - Real-time SSE (Server-Sent Events) output
- **Non-streaming option** - JSON response when `stream: false`
- **No infrastructure** - Runs on Cloudflare's global edge network
- **Pay per request** - Generous free tier, scales automatically
- **Fast cold starts** - Milliseconds, not seconds
- **CORS enabled** - Works from any browser/frontend

## Usage

### Streaming (default)

```bash
curl -X POST "https://ai-inference.nicknicola182.workers.dev" \
  -H "Content-Type: application/json" \
  -d '{"prompt": "Explain how neural networks learn"}'
```

### Non-streaming

```bash
curl -X POST "https://ai-inference.nicknicola182.workers.dev" \
  -H "Content-Type: application/json" \
  -d '{"prompt": "Hello", "stream": false}'
```

### With custom messages

```bash
curl -X POST "https://ai-inference.nicknicola182.workers.dev" \
  -H "Content-Type: application/json" \
  -d '{
    "messages": [
      {"role": "system", "content": "You are a helpful coding assistant."},
      {"role": "user", "content": "Write a Python function to reverse a string"}
    ],
    "max_tokens": 512,
    "temperature": 0.7
  }'
```

### JavaScript/Fetch

```javascript
const response = await fetch("https://ai-inference.nicknicola182.workers.dev", {
  method: "POST",
  headers: { "Content-Type": "application/json" },
  body: JSON.stringify({ prompt: "What is the meaning of life?" })
});

const reader = response.body.getReader();
const decoder = new TextDecoder();

while (true) {
  const { done, value } = await reader.read();
  if (done) break;
  console.log(decoder.decode(value));
}
```

## Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `prompt` | string | "Hello!" | Simple text prompt |
| `messages` | array | - | Chat messages array (overrides prompt) |
| `model` | string | `@cf/meta/llama-3.3-70b-instruct-fp8-fast` | Workers AI model ID |
| `max_tokens` | number | 1024 | Maximum tokens to generate |
| `temperature` | number | 0.7 | Randomness (0-2) |
| `stream` | boolean | true | Enable streaming response |

## Deploy Your Own

### Prerequisites

- [Node.js](https://nodejs.org/) 18+
- [Cloudflare account](https://dash.cloudflare.com/sign-up)

### Setup

```bash
# Clone the repo
git clone https://github.com/nicknicola182-maker/workers-ai-streaming.git
cd workers-ai-streaming

# Install dependencies
npm install

# Login to Cloudflare
npx wrangler login

# Deploy
npm run deploy
```

### Local Development

```bash
npm run dev
```

Note: Local dev still uses remote Workers AI and will incur usage charges.

## Project Structure

```
workers-ai-streaming/
├── src/
│   └── index.ts      # Main worker code
├── wrangler.jsonc    # Cloudflare configuration
├── package.json
└── tsconfig.json
```

## Available Models

You can use any [Workers AI text generation model](https://developers.cloudflare.com/workers-ai/models/). Examples:

- `@cf/meta/llama-3.3-70b-instruct-fp8-fast` (default)
- `@cf/meta/llama-4-scout-17b-16e-instruct`
- `@cf/deepseek-ai/deepseek-r1-distill-qwen-32b`
- `@cf/qwen/qwen2.5-72b-instruct-fp8-fast`

## License

MIT
