import assert from "node:assert/strict";
import test from "node:test";

async function render(path = "/") {
  const workerUrl = new URL("../dist/server/index.js", import.meta.url);
  workerUrl.searchParams.set("test", `${process.pid}-${Date.now()}`);
  const { default: worker } = await import(workerUrl.href);
  return worker.fetch(
    new Request(`http://localhost${path}`, { headers: { accept: "text/html" } }),
    { ASSETS: { fetch: async () => new Response("Not found", { status: 404 }) } },
    { waitUntil() {}, passThroughOnException() {} },
  );
}

test("server-renders the M4 calculator", async () => {
  const response = await render();
  assert.equal(response.status, 200);
  const html = await response.text();
  assert.match(html, /<title>M4 Workbench/);
  assert.match(html, /Stress-test your development plan/);
  assert.match(html, /Private by default/);
  assert.match(html, /End-to-end AI-assisted cycle/);
  assert.match(html, /Human share/);
  assert.match(html, /Research snapshot: 2026/);
  assert.match(html, /Calibration sources and method/);
  assert.match(html, /Generative AI and labour productivity/);
  assert.match(html, /When Code Authors Are Agents/);
  assert.match(html, /Share this calculation/);
  assert.match(html, /theme-init\.js/);
  assert.match(html, /aria-label="Language"/);
  assert.doesNotMatch(html, /codex-preview|react-loading-skeleton/);
});
