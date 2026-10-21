import assert from "node:assert/strict";
import test from "node:test";
import worker from "../src/worker.mjs";
import {DASHBOARD_CSS, buildDashboardData, queryDashboardData, rangeStart} from "../src/dashboard.mjs";

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

test("records one supporting PDF event", async () => {
  const {response, writes} = await invoke({version: 1, resourceId: "story-elements", downloadType: "supporting", pageNumber: null});
  assert.equal(response.status, 204);
  assert.deepEqual(writes, [{indexes: ["story-elements"], blobs: ["supporting"], doubles: [0]}]);
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

test("dashboard remains unavailable until the Access deployment gate is enabled", async () => {
  const response = await worker.fetch(new Request("https://worker.example/dashboard"), {
    DASHBOARD_ENABLED: "false",
  });
  assert.equal(response.status, 404);
});

test("serves the read-only dashboard with security headers when enabled", async () => {
  const response = await worker.fetch(new Request("https://worker.example/dashboard"), {
    DASHBOARD_ENABLED: "true",
    ANALYTICS_SQL: {query: async () => ({data: []})},
  });
  assert.equal(response.status, 200);
  const html = await response.text();
  assert.match(html, /PDF link analytics/);
  assert.match(html, /<style nonce="[a-f0-9]+">/);
  assert.doesNotMatch(html, /<script|Loading analytics|src="\/dashboard\/app\.js"|href="\/dashboard\/styles\.css"/);
  assert.match(html, /Total PDF clicks<\/span><strong>0<\/strong>/);
  assert.match(html, /No genuine worksheet downloads in this period/);
  assert.match(html, /Follow the Directions/);
  assert.match(html, /Catalog metadata: 96 resources/);
  assert.match(html, /America\/Detroit/);
  assert.equal(response.headers.get("Cache-Control"), "no-store");
  assert.equal(response.headers.get("X-Robots-Tag"), "noindex, nofollow, noarchive");
  assert.doesNotMatch(response.headers.get("Content-Security-Policy"), /script-src/);
  assert.match(response.headers.get("Content-Security-Policy"), /frame-ancestors 'none'/);
});

test("returns catalog-backed analytics and excludes controlled events", async () => {
  let receivedQuery;
  const response = await worker.fetch(new Request("https://worker.example/dashboard/data?range=30"), {
    DASHBOARD_ENABLED: "true",
    ANALYTICS_SQL: {
      query: async request => {
        receivedQuery = request;
        return {data: [
          {index1: "follow-directions", blob1: "pack", double1: 0, clicks: 4},
          {index1: "follow-directions", blob1: "page", double1: 2, clicks: 3},
          {index1: "analytics-deployment-check", blob1: "pack", double1: 0, clicks: 99},
        ]};
      },
    },
  });
  assert.equal(response.status, 200);
  const data = await response.json();
  assert.equal(data.range, "30");
  assert.deepEqual(data.totals, {totalClicks: 7, fullPackClicks: 4, individualPageClicks: 3, supportingPdfClicks: 0});
  assert.equal(data.resources[0].id, "follow-directions");
  assert.equal(data.resources[0].pages[1].clicks, 3);
  assert.match(receivedQuery.query, /index1 != \$controlledId/);
  assert.match(receivedQuery.query, /SUM\(_sample_interval\) AS clicks/);
  assert.doesNotMatch(receivedQuery.query, /ORDER BY resource_id|toUInt32/);
  assert.equal(receivedQuery.params.controlledId, "analytics-deployment-check");
});

test("falls back only when the sampling-aware SQL is rejected as non-retryable", async () => {
  const queries = [];
  const data = await queryDashboardData({query: async request => {
    queries.push(request);
    if (queries.length === 1) {
      const error = new Error("unknown identifier _sample_interval");
      error.retryable = false;
      throw error;
    }
    return {data: [{index1: "follow-directions", blob1: "pack", double1: 0, clicks: 2}]};
  }}, "7", new Date("2026-10-21T14:30:00.000Z"));
  assert.equal(queries.length, 2);
  assert.match(queries[0].query, /SUM\(_sample_interval\) AS clicks/);
  assert.match(queries[1].query, /COUNT\(\*\) AS clicks/);
  assert.equal(data.totals.totalClicks, 2);
});

test("does not mask retryable Analytics SQL failures", async () => {
  let attempts = 0;
  await assert.rejects(
    queryDashboardData({query: async () => {
      attempts += 1;
      const error = new Error("temporary service failure");
      error.retryable = true;
      throw error;
    }}, "7"),
    /temporary service failure/,
  );
  assert.equal(attempts, 1);
});

test("does not mask unrelated non-retryable Analytics SQL failures", async () => {
  let attempts = 0;
  await assert.rejects(
    queryDashboardData({query: async () => {
      attempts += 1;
      const error = new Error("dataset is unavailable");
      error.retryable = false;
      throw error;
    }}, "7"),
    /dataset is unavailable/,
  );
  assert.equal(attempts, 1);
});

test("dashboard data accepts only fixed date filters", async () => {
  let start;
  const response = await worker.fetch(new Request("https://worker.example/dashboard/data?range=arbitrary"), {
    DASHBOARD_ENABLED: "true",
    ANALYTICS_SQL: {query: async request => {
      start = request.params.start;
      return {data: []};
    }},
  });
  assert.equal(response.status, 200);
  assert.equal((await response.json()).range, "7");
  assert.match(start, /^\d{4}-\d{2}-\d{2}T/);
});

test("dashboard is mobile responsive and contains no client credentials", () => {
  assert.match(DASHBOARD_CSS, /@media\(max-width:640px\)/);
  assert.doesNotMatch(DASHBOARD_CSS, /CLOUDFLARE_API_TOKEN|Authorization:\s*Bearer/i);
});

test("dashboard renders a clear query failure instead of a loading state", async () => {
  const response = await worker.fetch(new Request("https://worker.example/dashboard"), {
    DASHBOARD_ENABLED: "true",
    ANALYTICS_SQL: {query: async () => { throw new Error("query failed"); }},
  });
  assert.equal(response.status, 200);
  const html = await response.text();
  assert.match(html, /Analytics are temporarily unavailable\. Please try again\./);
  assert.doesNotMatch(html, /Loading analytics/);
});

test("date ranges use America Detroit calendar boundaries across daylight saving time", () => {
  assert.equal(rangeStart("today", new Date("2026-07-15T14:30:00.000Z")).toISOString(), "2026-07-15T04:00:00.000Z");
  assert.equal(rangeStart("today", new Date("2026-01-15T14:30:00.000Z")).toISOString(), "2026-01-15T05:00:00.000Z");
  assert.equal(rangeStart("7", new Date("2026-10-21T14:30:00.000Z")).toISOString(), "2026-10-15T04:00:00.000Z");
  assert.equal(rangeStart("30", new Date("2026-10-21T14:30:00.000Z")).toISOString(), "2026-09-22T04:00:00.000Z");
});

test("unknown resources remain visible in totals with a fallback label", () => {
  const data = buildDashboardData([
    {index1: "future-resource", blob1: "pack", double1: 0, clicks: 2},
    {index1: "future-resource", blob1: "page", double1: 4, clicks: 3},
    {index1: "future-resource", blob1: "supporting", double1: 0, clicks: 1},
    {index1: "analytics-deployment-check", blob1: "pack", double1: 0, clicks: 99},
  ], "7");
  assert.deepEqual(data.totals, {totalClicks: 6, fullPackClicks: 2, individualPageClicks: 3, supportingPdfClicks: 1});
  assert.equal(data.resources[0].id, "future-resource");
  assert.equal(data.resources[0].title, "Uncataloged resource: future-resource");
  assert.deepEqual(data.resources[0].pages, [{number: 4, label: "Page 4", clicks: 3}]);
  assert.equal(data.metadataResourceCount, 96);
  assert.equal(data.timeZone, "America/Detroit");
});
