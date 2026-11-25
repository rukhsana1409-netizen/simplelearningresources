import assert from "node:assert/strict";
import test from "node:test";
import worker, {catalogMetadataUrls, gameMetadataUrls} from "../src/worker.mjs";
import {DASHBOARD_CSS, DEFAULT_CATALOG_METADATA_URL, DEFAULT_CATALOG_METADATA_FALLBACK_URL, buildDashboardData, loadCatalogMetadata, queryDashboardData, queryPopularWorksheetIds, rangeStart} from "../src/dashboard.mjs";
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

test("records one v2 full-pack download event", async () => {
  const {response, writes} = await invoke({version: 2, resourceId: "cvc-words-read-spell", downloadType: "pack-download", pageNumber: null});
  assert.equal(response.status, 204);
  assert.deepEqual(writes, [{indexes: ["cvc-words-read-spell"], blobs: ["pack-download"], doubles: [0]}]);
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

test("records one v2 individual-page download event", async () => {
  const {response, writes} = await invoke({version: 2, resourceId: "cvc-words-read-spell", downloadType: "page-download", pageNumber: 3});
  assert.equal(response.status, 204);
  assert.deepEqual(writes, [{indexes: ["cvc-words-read-spell"], blobs: ["page-download"], doubles: [3]}]);
});

test("records one v2 supporting PDF download event", async () => {
  const {response, writes} = await invoke({version: 2, resourceId: "story-elements", downloadType: "supporting-download", pageNumber: null});
  assert.equal(response.status, 204);
  assert.deepEqual(writes, [{indexes: ["story-elements"], blobs: ["supporting-download"], doubles: [0]}]);
});

test("continues accepting legacy v1 download events without rewriting them", async () => {
  const {response, writes} = await invoke({version: 1, resourceId: "story-elements", downloadType: "page", pageNumber: 2});
  assert.equal(response.status, 204);
  assert.deepEqual(writes, [{indexes: ["story-elements"], blobs: ["page"], doubles: [2]}]);
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
    {version: 1, resourceId: "valid-id", downloadType: "pack-download", pageNumber: null},
    {version: 2, resourceId: "valid-id", downloadType: "pack", pageNumber: null},
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

test("popular worksheets rank intentional downloads while excluding supporting and ambiguous legacy page clicks", async () => {
  let queryRequest;
  const catalog = {
    resources: {
      "counting-objects-1-5": {title: "Counting Objects 1-5", pages: ["Page 1"]},
      "letter-sounds-a-z": {title: "Letter Sounds A-Z", pages: ["Page 1"]},
      "cvc-words-read-spell": {title: "CVC Words", pages: ["Page 1"]},
    },
    version: "test",
    source: "test",
  };
  const analytics = {query: async request => {
    queryRequest = request;
    return {data: [
      {index1: "counting-objects-1-5", blob1: "pack", double1: 0, clicks: 2},
      {index1: "counting-objects-1-5", blob1: "page-download", double1: 1, clicks: 3},
      {index1: "letter-sounds-a-z", blob1: "pack", double1: 0, clicks: 4},
      {index1: "letter-sounds-a-z", blob1: "page", double1: 1, clicks: 500},
      {index1: "letter-sounds-a-z", blob1: "supporting", double1: 0, clicks: 50},
      {index1: "cvc-words-read-spell", blob1: "supporting", double1: 0, clicks: 100},
      {index1: "retired-resource", blob1: "pack", double1: 0, clicks: 200},
      {index1: "analytics-deployment-check", blob1: "pack", double1: 0, clicks: 500},
    ]};
  }};
  const result = await queryPopularWorksheetIds(analytics, new Date("2026-11-19T18:00:00Z"), catalog, 5);
  assert.deepEqual(result.resourceIds, ["counting-objects-1-5", "letter-sounds-a-z"]);
  assert.equal(result.range, "30");
  assert.equal(result.timeZone, "America/Detroit");
  assert.match(queryRequest.query, /SUM\(_sample_interval\)/);
  assert.match(queryRequest.query, /index1 != \$controlledId/);
  assert.match(queryRequest.query, /'pack-download'/);
  assert.match(queryRequest.query, /'page-download'/);
  assert.match(queryRequest.query, /'supporting-download'/);
});

test("dashboard separates ambiguous legacy page clicks from intentional downloads", () => {
  const catalog = {resources: {pronouns: {title: "Pronouns", pages: ["Page One", "Page Two"]}}, version: "test", source: "test"};
  const data = buildDashboardData([
    {index1: "pronouns", blob1: "pack", double1: 0, clicks: 2},
    {index1: "pronouns", blob1: "pack-download", double1: 0, clicks: 3},
    {index1: "pronouns", blob1: "page", double1: 1, clicks: 7},
    {index1: "pronouns", blob1: "page-download", double1: 2, clicks: 5},
    {index1: "pronouns", blob1: "supporting-download", double1: 0, clicks: 1},
  ], "7", new Date("2026-11-24T12:00:00Z"), catalog);
  const resource = data.resources[0];
  assert.equal(resource.fullPackClicks, 5);
  assert.equal(resource.individualPageClicks, 5);
  assert.equal(resource.supportingPdfClicks, 1);
  assert.equal(resource.legacyPdfLinkClicks, 7);
  assert.equal(resource.downloadClicks, 11);
  assert.equal(resource.totalClicks, 18);
  assert.equal(resource.pages[0].clicks, 0);
  assert.equal(resource.pages[0].legacyClicks, 7);
  assert.deepEqual(data.totals, {
    totalClicks: 18,
    downloadClicks: 11,
    fullPackClicks: 5,
    individualPageClicks: 5,
    supportingPdfClicks: 1,
    legacyPdfLinkClicks: 7,
  });
});

test("popular worksheets endpoint exposes only cached resource ids to the site origin", async () => {
  const originalCaches = globalThis.caches;
  const cachedResponses = new Map();
  globalThis.caches = {default: {
    match: async request => cachedResponses.get(request.url),
    put: async (request, response) => cachedResponses.set(request.url, response),
  }};
  let queries = 0;
  const env = {
    CATALOG_METADATA_URL: null,
    ANALYTICS_SQL: {query: async () => {
      queries += 1;
      return {data: [{index1: "counting-objects-1-5", blob1: "pack", double1: 0, clicks: 7}]};
    }},
  };
  try {
    const request = () => new Request("https://worker.example/popular-worksheets", {headers: {Origin: origin}});
    const first = await worker.fetch(request(), env);
    assert.equal(first.status, 200);
    assert.equal(first.headers.get("Access-Control-Allow-Origin"), origin);
    assert.equal(first.headers.get("Cache-Control"), "public, max-age=21600, stale-while-revalidate=86400");
    assert.deepEqual(Object.keys(await first.clone().json()).sort(), ["generatedAt", "resourceIds"]);
    assert.deepEqual((await first.json()).resourceIds, ["counting-objects-1-5"]);
    const second = await worker.fetch(request(), env);
    assert.equal(second.status, 200);
    assert.equal(queries, 1);
    assert.equal([...cachedResponses.keys()][0], "https://worker.example/popular-worksheets?metric=v2-downloads");
  } finally {
    globalThis.caches = originalCaches;
  }
});

test("popular worksheets endpoint rejects unauthorized origins", async () => {
  const response = await worker.fetch(new Request("https://worker.example/popular-worksheets", {
    headers: {Origin: "https://example.com"},
  }), {});
  assert.equal(response.status, 403);
  assert.equal(response.headers.get("Access-Control-Allow-Origin"), null);
});

test("popular worksheets endpoint handles exact-origin preflight", async () => {
  const response = await worker.fetch(new Request("https://worker.example/popular-worksheets", {
    method: "OPTIONS",
    headers: {Origin: origin},
  }), {});
  assert.equal(response.status, 204);
  assert.equal(response.headers.get("Access-Control-Allow-Origin"), origin);
  assert.equal(response.headers.get("Access-Control-Allow-Methods"), "GET, OPTIONS");
});

test("popular worksheets query failures retain CORS without caching the error", async () => {
  const response = await worker.fetch(new Request("https://worker.example/popular-worksheets", {
    headers: {Origin: origin},
  }), {
    CATALOG_METADATA_URL: null,
    ANALYTICS_SQL: {query: async () => { throw new Error("query unavailable"); }},
  });
  assert.equal(response.status, 503);
  assert.equal(response.headers.get("Access-Control-Allow-Origin"), origin);
  assert.equal(response.headers.get("Cache-Control"), "no-store");
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

test("game dashboard aggregates only starts and completions", async () => {
  let queryRequest;
  const rows = [
    {index1: "game--big-or-small", blob1: "game-start", eventCount: 3, value1: 0, value2: 0},
    {index1: "game--big-or-small", blob1: "game-complete", eventCount: 2, value1: 0, value2: 0},
    {index1: "game--number-chomp", blob1: "game-start-v2", blob2: "easy", eventCount: 4, value1: 1, value2: 0},
    {index1: "game--number-chomp", blob1: "game-complete-v2", blob2: "easy", eventCount: 3, value1: 60, value2: 51},
    {index1: "game--number-chomp", blob1: "game-mistakes", blob2: "easy", blob3: "symbol-equal", eventCount: 2, value1: 4, value2: 0},
    {index1: "game--math-bubble-pop", blob1: "game-start", eventCount: 6, value1: 0, value2: 0},
    {index1: "game--word-builder", blob1: "game-start", eventCount: 2, value1: 0, value2: 0},
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
  assert.equal(data.totals.starts, 15);
  assert.equal(data.totals.completions, 5);
  assert.equal(data.totals.activeGames, 4);
  assert.equal(data.totals.completionRate, 33);
  assert.deepEqual(Object.keys(data.totals).sort(), ["activeGames", "completionRate", "completions", "starts"]);
  assert.equal(data.metadataGameCount, 6);
  assert.equal(data.games.length, 6);
  const bigOrSmall = data.games.find(game => game.id === "big-or-small");
  assert.equal(bigOrSmall.starts, 3);
  assert.equal(bigOrSmall.completions, 2);
  const numberChomp = data.games.find(game => game.id === "number-chomp");
  assert.equal(numberChomp.starts, 4);
  assert.equal(numberChomp.completions, 3);
  assert.deepEqual(Object.keys(numberChomp).sort(), ["completionRate", "completions", "id", "starts", "title"]);
  assert.equal(data.games.find(game => game.id === "shape-safari").title, "Shape Safari!");
  const mathBubblePop = data.games.find(game => game.id === "math-bubble-pop");
  assert.equal(mathBubblePop.title, "Math Bubble Pop");
  assert.equal(mathBubblePop.starts, 6);
  assert.equal(mathBubblePop.completions, 0);
  assert.equal(mathBubblePop.completionRate, 0);
  const wordBuilder = data.games.find(game => game.id === "word-builder");
  assert.equal(wordBuilder.title, "Word Builder: Phonics Adventure");
  assert.equal(wordBuilder.starts, 2);
  assert.equal(wordBuilder.completions, 0);
  assert.equal(queryRequest.params.controlledId, "game--analytics-deployment-check");
  assert.match(queryRequest.query, /index1 != \$controlledId/);
  assert.match(queryRequest.query, /blob1 IN \('game-start', 'game-complete', 'game-start-v2', 'game-complete-v2'\)/);
  assert.doesNotMatch(queryRequest.query, /game-view|game-mistakes/);
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
  assert.match(html, /Rocket Rescue!/);
  assert.match(html, /Math Bubble Pop/);
  assert.match(html, /Word Builder: Phonics Adventure/);
  assert.match(html, /Active games/);
  assert.match(html, /Completion rate/);
  assert.match(html, /class="game-table"/);
  assert.match(html, /<span>Starts<\/span><span>Completions<\/span><span>Rate<\/span>/);
  assert.match(html, /\.game\{display:grid;grid-template-columns:minmax\(0,1fr\) repeat\(3,minmax\(5rem,auto\)\)/);
  assert.doesNotMatch(html, /\.game\{display:flex/);
  assert.doesNotMatch(html, /Difficulty|Mistake categories|First-try|Replay clicks/);
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
  assert.equal(data.games[0].starts, 1);
  assert.equal(data.games[0].completions, 0);
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
  assert.match(html, /Intentional download clicks<\/span><strong>0<\/strong>/);
  assert.match(html, /Ambiguous legacy PDF-link clicks<\/span><strong>0<\/strong>/);
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
  assert.deepEqual(data.totals, {totalClicks: 7, downloadClicks: 4, fullPackClicks: 4, individualPageClicks: 0, supportingPdfClicks: 0, legacyPdfLinkClicks: 3});
  assert.equal(data.resources[0].id, "follow-directions");
  assert.equal(data.resources[0].pages[1].clicks, 0);
  assert.equal(data.resources[0].pages[1].legacyClicks, 3);
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
  assert.deepEqual(data.totals, {totalClicks: 6, downloadClicks: 3, fullPackClicks: 2, individualPageClicks: 0, supportingPdfClicks: 1, legacyPdfLinkClicks: 3});
  assert.equal(data.resources[0].id, "future-resource");
  assert.equal(data.resources[0].title, "Uncataloged resource: future-resource");
  assert.deepEqual(data.resources[0].pages, [{number: 4, label: "Page 4", clicks: 0, legacyClicks: 3}]);
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
          "long-ago": {title: "Long Ago & Me", taxonomy: {grade: "kindergarten", subject: "social-studies", topic: "history"}, pages: ["Then and Now"]},
          "future-resource": {title: "Future Resource", taxonomy: {grade: "grade-1", subject: "math", topic: "future-topic"}, pages: ["New Activity"]},
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

test("high-frequency words resolves after moving to its dedicated catalog category", () => {
  assert.equal(RESOURCE_METADATA["high-frequency-words"].title, "High-Frequency Words: Read, Spell & Use");
  assert.deepEqual(RESOURCE_METADATA["high-frequency-words"].pages, [
    "Meet the Words",
    "Meet More Words",
    "Spell the Words",
    "Use the Words in Sentences",
    "Read and Write on Your Own",
  ]);
  const data = buildDashboardData([
    {index1: "high-frequency-words", blob1: "supporting", double1: 0, clicks: 1},
  ], "7");
  const resource = data.resources.find(item => item.id === "high-frequency-words");
  assert.equal(resource.title, "High-Frequency Words: Read, Spell & Use");
  assert.equal(resource.supportingPdfClicks, 1);
  assert.equal(resource.totalClicks, 1);
});

test("coins and money resolves with six pages and preserves historical clicks", () => {
  assert.equal(RESOURCE_METADATA["coins-and-money"].title, "Coins and Money: Identify, Count and Add");
  assert.deepEqual(RESOURCE_METADATA["coins-and-money"].pages, [
    "Meet the Coins",
    "Match the Coins",
    "Count the Coins",
    "Add Mixed Coins",
    "Make the Amount",
    "Money Word Problems",
  ]);
  const data = buildDashboardData([
    {index1: "coins-and-money", blob1: "page", double1: 3, clicks: 1},
  ], "7");
  const resource = data.resources.find(item => item.id === "coins-and-money");
  assert.equal(resource.title, "Coins and Money: Identify, Count and Add");
  assert.equal(resource.pages.length, 6);
  assert.equal(resource.pages[2].clicks, 0);
  assert.equal(resource.pages[2].legacyClicks, 1);
  assert.equal(resource.individualPageClicks, 0);
  assert.equal(resource.legacyPdfLinkClicks, 1);
  assert.equal(resource.totalClicks, 1);
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
          prepositions: {title: "Prepositions", taxonomy: {grade: "grade-1", subject: "reading-language", topic: "grammar-and-sentences"}, pages: ["Circle the Right Word"]},
        },
      });
    },
    12345,
  );
  assert.deepEqual(requests, [DEFAULT_CATALOG_METADATA_URL, DEFAULT_CATALOG_METADATA_FALLBACK_URL]);
  assert.equal(catalog.source, "repository");
  assert.equal(catalog.resources.prepositions.title, "Prepositions");
});

test("transient website metadata failures are retried once before fallback", async () => {
  const requests = [];
  const catalog = await loadCatalogMetadata(
    [DEFAULT_CATALOG_METADATA_URL, DEFAULT_CATALOG_METADATA_FALLBACK_URL],
    async (url) => {
      requests.push(url.origin + url.pathname);
      if (requests.length === 1) throw new TypeError("temporary network failure");
      return Response.json({
        version: "current-catalog",
        resourceCount: 1,
        resources: {
          "coins-and-money": {title: "Coins and Money: Identify, Count and Add", taxonomy: {grade: "grade-1", subject: "math", topic: "money"}, pages: ["Meet the Coins"]},
        },
      });
    },
    12345,
  );
  assert.deepEqual(requests, [DEFAULT_CATALOG_METADATA_URL, DEFAULT_CATALOG_METADATA_URL]);
  assert.equal(catalog.source, "website");
  assert.equal(catalog.resources["coins-and-money"].title, "Coins and Money: Identify, Count and Add");
});

test("transient HTTP metadata failures are retried once", async () => {
  let requests = 0;
  const catalog = await loadCatalogMetadata(
    DEFAULT_CATALOG_METADATA_URL,
    async () => {
      requests += 1;
      if (requests === 1) return new Response("temporarily unavailable", {status: 503});
      return Response.json({
        version: "current-catalog",
        resourceCount: 1,
        resources: {
          "coins-and-money": {title: "Coins and Money: Identify, Count and Add", taxonomy: {grade: "grade-1", subject: "math", topic: "money"}, pages: ["Meet the Coins"]},
        },
      });
    },
    12345,
  );
  assert.equal(requests, 2);
  assert.equal(catalog.source, "website");
});

test("non-transient HTTP metadata failures are not retried", async () => {
  let requests = 0;
  const catalog = await loadCatalogMetadata(
    DEFAULT_CATALOG_METADATA_URL,
    async () => {
      requests += 1;
      return new Response("not found", {status: 404});
    },
    12345,
  );
  assert.equal(requests, 1);
  assert.equal(catalog.source, "bundled");
});

test("invalid catalog metadata is not retried before repository fallback", async () => {
  const requests = [];
  const catalog = await loadCatalogMetadata(
    [DEFAULT_CATALOG_METADATA_URL, DEFAULT_CATALOG_METADATA_FALLBACK_URL],
    async (url) => {
      requests.push(url.origin + url.pathname);
      if (requests.length === 1) {
        return Response.json({version: "invalid", resourceCount: 1, resources: {}});
      }
      return Response.json({
        version: "repository-catalog",
        resourceCount: 1,
        resources: {
          "coins-and-money": {title: "Coins and Money: Identify, Count and Add", taxonomy: {grade: "grade-1", subject: "math", topic: "money"}, pages: ["Meet the Coins"]},
        },
      });
    },
    12345,
  );
  assert.deepEqual(requests, [DEFAULT_CATALOG_METADATA_URL, DEFAULT_CATALOG_METADATA_FALLBACK_URL]);
  assert.equal(catalog.source, "repository");
});

test("dashboard fetches hosted catalog metadata when the environment variable is absent", async (context) => {
  let requestedUrl;
  context.mock.method(globalThis, "fetch", async (url) => {
    requestedUrl = url;
    return Response.json({
      version: "current-catalog",
      resourceCount: 1,
      resources: {
        "adding-tens-and-ones": {title: "Adding Tens and Ones Within 100", taxonomy: {grade: "grade-1", subject: "math", topic: "addition-and-subtraction"}, pages: ["Add Tens"]},
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

test("current bundled fallback recognizes a newly published resource when both external metadata sources fail", async () => {
  const catalog = await loadCatalogMetadata(
    [DEFAULT_CATALOG_METADATA_URL, DEFAULT_CATALOG_METADATA_FALLBACK_URL],
    async () => { throw new TypeError("network unavailable"); },
  );
  assert.equal(catalog.source, "bundled");
  assert.equal(catalog.resources.pronouns.title, "Pronouns");
  const data = buildDashboardData([
    {index1: "pronouns", blob1: "page-download", double1: 5, clicks: 2},
  ], "7", new Date("2026-11-24T12:00:00Z"), catalog);
  const pronouns = data.resources.find(resource => resource.id === "pronouns");
  assert.equal(pronouns.title, "Pronouns");
  assert.equal(pronouns.pages.length, 5);
  assert.equal(pronouns.individualPageClicks, 2);
});
