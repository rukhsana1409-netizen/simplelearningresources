import assert from "node:assert/strict";
import test from "node:test";

import worker from "../src/worker.mjs";

const origin = "https://simplelearningresources.com";

const invoke = async (payload, options = {}) => {
  const writes = [];
  const env = {DOWNLOAD_ANALYTICS: {writeDataPoint: (point) => writes.push(point)}};
  const request = new Request(options.url || "https://worker.example/download", {
    method: options.method || "POST",
    headers: {Origin: options.origin || origin, "Content-Type": options.contentType || "text/plain;charset=UTF-8"},
    body: options.method === "OPTIONS" ? undefined : JSON.stringify(payload),
  });
  return {response: await worker.fetch(request, env), writes};
};

test("records one full-pack event", async () => {
  const {response, writes} = await invoke({version: 1, resourceId: "cvc-words-read-spell", downloadType: "pack", pageNumber: null});
  assert.equal(response.status, 204);
  assert.deepEqual(writes, [{indexes: ["cvc-words-read-spell"], blobs: ["pack"], doubles: [0]}]);
  assert.equal(response.headers.get("Access-Control-Allow-Origin"), origin);
});

test("records one individual-page event", async () => {
  const {response, writes} = await invoke({version: 1, resourceId: "cvc-words-read-spell", downloadType: "page", pageNumber: 3});
  assert.equal(response.status, 204);
  assert.deepEqual(writes, [{indexes: ["cvc-words-read-spell"], blobs: ["page"], doubles: [3]}]);
});

test("handles CORS preflight without writing", async () => {
  const {response, writes} = await invoke(null, {method: "OPTIONS"});
  assert.equal(response.status, 204);
  assert.equal(response.headers.get("Access-Control-Allow-Methods"), "POST, OPTIONS");
  assert.deepEqual(writes, []);
});

test("rejects untrusted origins", async () => {
  const {response, writes} = await invoke({version: 1, resourceId: "valid-id", downloadType: "pack", pageNumber: null}, {origin: "https://example.com"});
  assert.equal(response.status, 403);
  assert.deepEqual(writes, []);
});

test("rejects invalid fields without writing", async () => {
  for (const payload of [
    {version: 1, resourceId: "Invalid ID", downloadType: "pack", pageNumber: null},
    {version: 1, resourceId: "valid-id", downloadType: "page", pageNumber: 0},
    {version: 1, resourceId: "valid-id", downloadType: "pack", pageNumber: 2},
    {version: 1, resourceId: "valid-id", downloadType: "pack", pageNumber: null, visitorId: "x"},
  ]) {
    const {response, writes} = await invoke(payload);
    assert.equal(response.status, 400);
    assert.deepEqual(writes, []);
  }
});

test("health check does not write analytics", async () => {
  const writes = [];
  const response = await worker.fetch(new Request("https://worker.example/health"), {
    DOWNLOAD_ANALYTICS: {writeDataPoint: (point) => writes.push(point)},
  });
  assert.equal(response.status, 200);
  assert.equal(await response.text(), "ok\n");
  assert.deepEqual(writes, []);
});
