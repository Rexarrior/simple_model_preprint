import { handleImageOptimization, DEFAULT_DEVICE_SIZES, DEFAULT_IMAGE_SIZES } from "vinext/server/image-optimization";
import handler from "vinext/server/app-router-entry";
import { ensureSharedCalculationsTable } from "../db/index";

interface Env {
  ASSETS: Fetcher;
  DB: D1Database;
  IMAGES: {
    input(stream: ReadableStream): {
      transform(options: Record<string, unknown>): {
        output(options: { format: string; quality: number }): Promise<{ response(): Response }>;
      };
    };
  };
}

interface ExecutionContext {
  waitUntil(promise: Promise<unknown>): void;
  passThroughOnException(): void;
}

function json(payload: unknown, status = 200) {
  return new Response(JSON.stringify(payload), {
    status,
    headers: {
      "content-type": "application/json; charset=utf-8",
      "cache-control": "no-store",
      "x-content-type-options": "nosniff",
    },
  });
}

async function saveSharedCalculation(request: Request, env: Env) {
  const contentLength = Number(request.headers.get("content-length") ?? 0);
  if (contentLength > 300_000) return json({ error: "payload_too_large" }, 413);
  let body: Record<string, unknown>;
  try {
    body = await request.json() as Record<string, unknown>;
  } catch {
    return json({ error: "invalid_json" }, 400);
  }
  if (body.consent !== true || body.consentVersion !== "v1") {
    return json({ error: "explicit_consent_required" }, 403);
  }
  const config = body.config as Record<string, unknown> | undefined;
  const result = body.result as Record<string, unknown> | undefined;
  if (!config || !result || config.schemaVersion !== "m4-calculator/v1") {
    return json({ error: "invalid_calculation" }, 400);
  }
  const configJson = JSON.stringify(config);
  const resultJson = JSON.stringify(result);
  if (configJson.length + resultJson.length > 280_000) return json({ error: "payload_too_large" }, 413);

  await ensureSharedCalculationsTable(env.DB);
  const id = crypto.randomUUID();
  await env.DB.prepare(`INSERT INTO shared_calculations
    (id, created_at, schema_version, project_name, consent_version, config_json, result_json)
    VALUES (?, ?, ?, ?, ?, ?, ?)`)
    .bind(
      id,
      new Date().toISOString(),
      "m4-calculator/v1",
      String(config.projectName ?? "Без названия").slice(0, 200),
      "v1",
      configJson,
      resultJson,
    )
    .run();
  return json({ id, saved: true }, 201);
}

const worker = {
  async fetch(request: Request, env: Env, ctx: ExecutionContext): Promise<Response> {
    const url = new URL(request.url);
    if (url.pathname === "/api/share" && request.method === "POST") {
      return saveSharedCalculation(request, env);
    }
    if (url.pathname === "/api/health" && request.method === "GET") {
      return json({ status: "ok", persistence: "opt-in-only" });
    }
    if (url.pathname === "/_vinext/image") {
      const allowedWidths = [...DEFAULT_DEVICE_SIZES, ...DEFAULT_IMAGE_SIZES];
      return handleImageOptimization(request, {
        fetchAsset: (path) => env.ASSETS.fetch(new Request(new URL(path, request.url))),
        transformImage: async (body, { width, format, quality }) => {
          const result = await env.IMAGES.input(body).transform(width > 0 ? { width } : {}).output({ format, quality });
          return result.response();
        },
      }, allowedWidths);
    }
    return handler.fetch(request, env, ctx);
  },
};

export default worker;
