import assert from "node:assert/strict";
import test from "node:test";
import worker, {catalogMetadataUrls, gameMetadataUrls} from "../src/worker.mjs";
import {DASHBOARD_CSS, DEFAULT_CATALOG_METADATA_URL, DEFAULT_CATALOG_METADATA_FALLBACK_URL, buildDashboardData, loadCatalogMetadata, queryDashboardData, rangeStart} from "../src/dashboard.mjs";
import {RESOURCE_METADATA} from "../src/resource-metadata.mjs";
import {DEFAULT_GAME_METADATA_FALLBACK_URL, DEFAULT_GAME_METADATA_URL, buildGameDashboardData, loadGameMetadata} from "../src/game-dashboard.mjs";

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

test("records aggregate game events without visitor data", async () => {
  const writes = [];
  const env = {
    DOWNLOAD_ANALYTICS: {writeDataPoint: (point) => writes.push(point)},
  };
  const response = await worker.fetch(new Request("https://worker.example/game-event", {
    method: "POST",
    headers: {Origin: "https://simplelearningresources.com", "Content-Type": "text/plain"},
    body: JSON.stringify({version: 1, gameId: "big-or-small", eventType: "complete"}),
  }), env);
  assert.equal(response.status, 204);
  assert.deepEqual(writes, [{indexes: ["game--big-or-small"], blobs: ["game-complete"], doubles: [0]}]);
});

test("records aggregate v2 game start and completion summaries", async () => {
  const writes = [];
  const env = {DOWNLOAD_ANALYTICS: {writeDataPoint: point => writes.push(point)}};
  const request = payload => worker.fetch(new Request("https://worker.example/game-event", {
    method: "POST",
    headers: {Origin: origin, "Content-Type": "text/plain"},
    body: JSON.stringify(payload),
  }), env);
  assert.equal((await request({
    version: 2, gameId: "number-chomp", eventType: "start", difficulty: "easy", replay: true,
  })).status, 204);
  assert.equal((await request({
    version: 2,
    gameId: "number-chomp",
    eventType: "complete",
    difficulty: "easy",
    questionsAnswered: 20,
    firstTryCorrect: 17,
    mistakeCategories: {"pick-greater": 2, "symbol-equal": 1},
  })).status, 204);
  assert.deepEqual(writes, [
    {indexes: ["game--number-chomp"], blobs: ["game-start-v2", "easy"], doubles: [1, 0]},
    {indexes: ["game--number-chomp"], blobs: ["game-complete-v2", "easy"], doubles: [20, 17]},
    {indexes: ["game--number-chomp"], blobs: ["game-mistakes", "easy", "pick-greater"], doubles: [2, 0]},
    {indexes: ["game--number-chomp"], blobs: ["game-mistakes", "easy", "symbol-equal"], doubles: [1, 0]},
  ]);
});

test("rejects invalid detailed game summaries without writing", async () => {
  const writes = [];
  const response = await worker.fetch(new Request("https://worker.example/game-event", {
    method: "POST",
    headers: {Origin: origin, "Content-Type": "text/plain"},
    body: JSON.stringify({
      version: 2,
      gameId: "number-chomp",
      eventType: "complete",
      difficulty: "easy",
      questionsAnswered: 20,
      firstTryCorrect: 21,
      mistakeCategories: {},
    }),
  }), {DOWNLOAD_ANALYTICS: {writeDataPoint: point => writes.push(point)}});
  assert.equal(response.status, 400);
  assert.deepEqual(writes, []);
});

test("rejects unsupported game event fields", async () => {
  const writes = [];
  const env = {
    DOWNLOAD_ANALYTICS: {writeDataPoint: (point) => writes.push(point)},
  };
  const response = await worker.fetch(new Request("https://worker.example/game-event", {
    method: "POST",
    headers: {Origin: "https://simplelearningresources.com", "Content-Type": "application/json"},
    body: JSON.stringify({version: 1, gameId: "big-or-small", eventType: "start", visitorId: "not-allowed"}),
  }), env);
  assert.equal(response.status, 400);
  assert.equal(writes.length, 0);
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

test("game dashboard remains unavailable until its separate Access gate is enabled", async () => {
  for (const path of ["/game-dashboard", "/game-dashboard/data"]) {
    const response = await worker.fetch(new Request(`https://worker.example${path}`), {
      GAME_DASHBOARD_ENABLED: "false",
    });
    assert.equal(response.status, 404);
  }
});

test("game dashboard combines historical and detailed aggregate events", async () => {
  let queryRequest;
  const rows = [
    {index1: "game--big-or-small", blob1: "game-start", eventCount: 3, value1: 0, value2: 0},
    {index1: "game--big-or-small", blob1: "game-complete", eventCount: 2, value1: 0, value2: 0},
    {index1: "game--number-chomp", blob1: "game-start-v2", blob2: "easy", eventCount: 4, value1: 1, value2: 0},
    {index1: "game--number-chomp", blob1: "game-complete-v2", blob2: "easy", eventCount: 3, value1: 60, value2: 51},
    {index1: "game--number-chomp", blob1: "game-mistakes", blob2: "easy", blob3: "symbol-equal", eventCount: 2, value1: 4, value2: 0},
  ];
  const response = await worker.fetch(new Request("https://worker.example/game-dashboard/data?range=30"), {
    GAME_DASHBOARD_ENABLED: "true",
    GAME_METADATA_URL: null,
    ANALYTICS_SQL: {query: async request => {
      queryRequest = request;
      return {data: rows};
    }},
  });
  assert.equal(response.status, 200);
  assert.equal(response.headers.get("Content-Type"), "application/json; charset=utf-8");
  assert.equal(response.headers.get("X-Robots-Tag"), "noindex, nofollow, noarchive");
  const data = await response.json();
  assert.equal(data.totals.starts, 7);
  assert.equal(data.totals.completions, 5);
  assert.equal(data.totals.replayClicks, 1);
  assert.equal(data.totals.questionsAnswered, 60);
  assert.equal(data.totals.firstTryCorrect, 51);
  assert.equal(data.metadataGameCount, 3);
  const numberChomp = data.games.find(game => game.id === "number-chomp");
  assert.equal(numberChomp.difficulties[0].label, "Easy 1–10");
  assert.deepEqual(numberChomp.mistakes[0], {id: "symbol-equal", label: "Equal symbol", count: 4});
  assert.equal(data.games.find(game => game.id === "shape-safari").title, "Shape Safari!");
  assert.equal(queryRequest.params.controlledId, "game--analytics-deployment-check");
  assert.match(queryRequest.query, /index1 != \$controlledId/);
});

test("serves the separate read-only game dashboard with security headers", async () => {
  const response = await worker.fetch(new Request("https://worker.example/game-dashboard?range=7"), {
    GAME_DASHBOARD_ENABLED: "true",
    GAME_METADATA_URL: null,
    ANALYTICS_SQL: {query: async () => ({data: []})},
  });
  assert.equal(response.status, 200);
  const html = await response.text();
  assert.match(html, /<h1>Game analytics<\/h1>/);
  assert.match(html, /Big or Small\?/);
  assert.match(html, /Number Chomp!/);
  assert.doesNotMatch(html, /<script/);
  assert.equal(response.headers.get("Cache-Control"), "no-store");
  assert.equal(response.headers.get("X-Robots-Tag"), "noindex, nofollow, noarchive");
  assert.match(response.headers.get("Content-Security-Policy"), /frame-ancestors 'none'/);
});

test("hosted game metadata automatically labels a future game", async () => {
  const catalog = await loadGameMetadata(DEFAULT_GAME_METADATA_URL, async () => Response.json({
    version: "future-games",
    gameCount: 1,
    games: {
      "future-game": {
        title: "Future Game",
        difficulties: {default: "Standard"},
        categories: {matching: "Matching"},
      },
    },
  }));
  const data = buildGameDashboardData([
    {index1: "game--future-game", blob1: "game-start-v2", blob2: "default", eventCount: 1, value1: 0, value2: 0},
  ], "7", new Date("2026-11-08T12:00:00Z"), catalog);
  assert.equal(data.games[0].title, "Future Game");
  assert.equal(data.metadataVersion, "future-games");
  assert.equal(data.metadataSource, "website");
});

test("game metadata defaults use website and repository sources", () => {
  assert.deepEqual(gameMetadataUrls({}), [DEFAULT_GAME_METADATA_URL, DEFAULT_GAME_METADATA_FALLBACK_URL]);
  assert.deepEqual(gameMetadataUrls({GAME_METADATA_URL: null}), []);
});

test("serves the read-only dashboard with security headers when enabled", async () => {
  const response = await worker.fetch(new Request("https://worker.example/dashboard"), {
    DASHBOARD_ENABLED: "true",
    CATALOG_METADATA_URL: null,
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
  assert.match(html, new RegExp(`Catalog metadata: ${Object.keys(RESOURCE_METADATA).length} resources`));
  assert.match(html, /bundled fallback/);
  assert.doesNotMatch(html, /bundled bundled/);
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
    CATALOG_METADATA_URL: null,
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
    CATALOG_METADATA_URL: null,
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
    CATALOG_METADATA_URL: null,
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
  assert.equal(data.metadataResourceCount, Object.keys(RESOURCE_METADATA).length);
  assert.equal(data.timeZone, "America/Detroit");
});

test("website catalog metadata labels historical clicks and bypasses stale caches", async () => {
  let requestUrl;
  let requestOptions;
  const catalog = await loadCatalogMetadata(
    "https://simplelearningresources.com/download-analytics-catalog.json",
    async (url, options) => {
      requestUrl = url;
      requestOptions = options;
      return Response.json({
        version: "catalog-2026",
        resourceCount: 2,
        resources: {
          "long-ago": {title: "Long Ago & Me", pages: ["Then and Now"]},
          "future-resource": {title: "Future Resource", pages: ["New Activity"]},
        },
      });
    },
    12345,
  );
  assert.equal(requestUrl.searchParams.get("catalog-version-check"), "12345");
  assert.equal(requestOptions.cache, "no-store");
  assert.equal(requestOptions.cf.cacheTtl, 0);
  const data = buildDashboardData([
    {index1: "long-ago", blob1: "pack", double1: 0, clicks: 1},
  ], "7", new Date("2026-10-21T14:30:00.000Z"), catalog);
  assert.equal(data.resources.find(resource => resource.id === "long-ago").title, "Long Ago & Me");
  assert.equal(data.resources.find(resource => resource.id === "future-resource").title, "Future Resource");
  assert.equal(data.metadataResourceCount, 2);
  assert.equal(data.metadataVersion, "catalog-2026");
  assert.equal(data.metadataSource, "website");
});

test("current Grade 1 and seasonal resource ids resolve from generated catalog metadata", () => {
  const data = buildDashboardData([
    {index1: "adding-tens-and-ones", blob1: "pack", double1: 0, clicks: 2},
    {index1: "halloween-alphabet-hunt", blob1: "page", double1: 1, clicks: 3},
  ], "7");
  assert.equal(data.resources.find(resource => resource.id === "adding-tens-and-ones").title, "Adding Tens and Ones Within 100");
  assert.equal(data.resources.find(resource => resource.id === "halloween-alphabet-hunt").title, "Halloween Alphabet Hunt");
  assert.equal(data.resources.some(resource => resource.title.startsWith("Uncataloged resource:")), false);
});

test("prepositions resolves from complete generated catalog metadata", () => {
  assert.equal(RESOURCE_METADATA.prepositions.title, "Prepositions");
  assert.deepEqual(RESOURCE_METADATA.prepositions.pages, ["Circle the Right Word"]);
});

test("the Worker has a hosted catalog default when the environment variable is absent", () => {
  assert.equal(DEFAULT_CATALOG_METADATA_URL, "https://simplelearningresources.com/download-analytics-catalog.json");
  assert.equal(DEFAULT_CATALOG_METADATA_FALLBACK_URL, "https://raw.githubusercontent.com/rukhsana1409-netizen/simplelearningresources/main/download-analytics-catalog.json");
  assert.deepEqual(catalogMetadataUrls({}), [DEFAULT_CATALOG_METADATA_URL, DEFAULT_CATALOG_METADATA_FALLBACK_URL]);
  assert.deepEqual(catalogMetadataUrls({CATALOG_METADATA_URL: "https://example.com/catalog.json"}), ["https://example.com/catalog.json", DEFAULT_CATALOG_METADATA_FALLBACK_URL]);
  assert.deepEqual(catalogMetadataUrls({CATALOG_METADATA_URL: null}), []);
});

test("repository metadata is used when the website metadata fetch fails", async () => {
  const requests = [];
  const catalog = await loadCatalogMetadata(
    [DEFAULT_CATALOG_METADATA_URL, DEFAULT_CATALOG_METADATA_FALLBACK_URL],
    async (url) => {
      requests.push(url.origin + url.pathname);
      if (requests.length === 1) throw new Error("website metadata fetch failed");
      return Response.json({
        version: "current-catalog",
        resourceCount: 1,
        resources: {
          prepositions: {title: "Prepositions", pages: ["Circle the Right Word"]},
        },
      });
    },
    12345,
  );
  assert.deepEqual(requests, [DEFAULT_CATALOG_METADATA_URL, DEFAULT_CATALOG_METADATA_FALLBACK_URL]);
  assert.equal(catalog.source, "repository");
  assert.equal(catalog.resources.prepositions.title, "Prepositions");
});

test("dashboard fetches hosted catalog metadata when the environment variable is absent", async (context) => {
  let requestedUrl;
  context.mock.method(globalThis, "fetch", async (url) => {
    requestedUrl = url;
    return Response.json({
      version: "current-catalog",
      resourceCount: 1,
      resources: {
        "adding-tens-and-ones": {title: "Adding Tens and Ones Within 100", pages: ["Add Tens"]},
      },
    });
  });
  const response = await worker.fetch(new Request("https://worker.example/dashboard"), {
    DASHBOARD_ENABLED: "true",
    ANALYTICS_SQL: {query: async () => ({data: []})},
  });
  assert.equal(response.status, 200);
  assert.equal(requestedUrl.origin + requestedUrl.pathname, DEFAULT_CATALOG_METADATA_URL);
  const html = await response.text();
  assert.match(html, /Adding Tens and Ones Within 100/);
  assert.match(html, /Catalog metadata: 1 resources · website current-catalog/);
});

test("invalid website metadata falls back without dropping uncataloged clicks", async () => {
  const catalog = await loadCatalogMetadata(
    "https://simplelearningresources.com/download-analytics-catalog.json",
    async () => Response.json({version: "bad", resourceCount: 1, resources: {}}),
  );
  assert.equal(catalog.source, "bundled");
  const data = buildDashboardData([
    {index1: "genuinely-uncataloged", blob1: "pack", double1: 0, clicks: 2},
  ], "7", new Date(), catalog);
  const unknown = data.resources.find(resource => resource.id === "genuinely-uncataloged");
  assert.equal(unknown.title, "Uncataloged resource: genuinely-uncataloged");
  assert.equal(data.totals.totalClicks, 2);
});
