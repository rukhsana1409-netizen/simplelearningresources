import {GAME_METADATA} from "./game-metadata.mjs";
import {SITE_TIME_ZONE, rangeStart} from "./dashboard.mjs";

const RANGE_DAYS = new Set(["today", "7", "30"]);
const CONTROLLED_TEST_GAME_ID = "game--analytics-deployment-check";
export const DEFAULT_GAME_METADATA_URL = "https://simplelearningresources.com/game-analytics-catalog.json";
export const DEFAULT_GAME_METADATA_FALLBACK_URL = "https://raw.githubusercontent.com/rukhsana1409-netizen/simplelearningresources/main/game-analytics-catalog.json";

const validGameMetadata = (value) => (
  value && typeof value === "object" && !Array.isArray(value)
  && typeof value.title === "string" && value.title.length > 0
  && value.difficulties && typeof value.difficulties === "object" && !Array.isArray(value.difficulties)
  && value.categories && typeof value.categories === "object" && !Array.isArray(value.categories)
);

export const loadGameMetadata = async (urls, fetcher = fetch, now = Date.now()) => {
  const candidates = (Array.isArray(urls) ? urls : [urls]).filter(Boolean);
  if (!candidates.length) return {games: GAME_METADATA, version: "bundled", source: "bundled"};
  const failures = [];
  for (const [index, url] of candidates.entries()) {
    const requestUrl = new URL(url);
    requestUrl.searchParams.set("catalog-version-check", String(now));
    try {
      const response = await fetcher(requestUrl, {
        headers: {Accept: "application/json", "Cache-Control": "no-cache"},
        cache: "no-store",
        cf: {cacheTtl: 0, cacheEverything: false},
      });
      if (!response.ok) throw new Error(`game metadata returned HTTP ${response.status}`);
      const payload = await response.json();
      const games = payload?.games;
      const entries = games && typeof games === "object" && !Array.isArray(games) ? Object.entries(games) : [];
      if (!entries.length || entries.some(([id, metadata]) => !id || !validGameMetadata(metadata))) {
        throw new Error("game metadata contains an invalid game");
      }
      if (payload.gameCount !== entries.length) throw new Error("game metadata count does not match games");
      return {games, version: String(payload.version || "unversioned"), source: index === 0 ? "website" : "repository"};
    } catch (error) {
      failures.push(`${requestUrl.origin}: ${error?.message || "unknown error"}`);
    }
  }
  console.warn("game metadata unavailable; using bundled fallback", failures.join("; "));
  return {games: GAME_METADATA, version: "bundled", source: "bundled"};
};

const countQuery = (samplingAware) => `
  SELECT index1, blob1, blob2, blob3,
    ${samplingAware ? "SUM(_sample_interval)" : "COUNT(*)"} AS eventCount,
    ${samplingAware ? "SUM(_sample_interval * double1)" : "SUM(double1)"} AS value1,
    ${samplingAware ? "SUM(_sample_interval * double2)" : "SUM(double2)"} AS value2
  FROM events.analyticsEngine."lms_download_clicks"
  WHERE timestamp >= $start
    AND index1 LIKE 'game--%'
    AND index1 != $controlledId
    AND blob1 IN ('game-view', 'game-start', 'game-complete', 'game-start-v2', 'game-complete-v2', 'game-mistakes')
  GROUP BY index1, blob1, blob2, blob3
`;

export const queryGameDashboardData = async (analytics, requestedRange, now = new Date(), catalog = {}) => {
  const range = RANGE_DAYS.has(requestedRange) ? requestedRange : "7";
  const params = {start: rangeStart(range, now).toISOString(), controlledId: CONTROLLED_TEST_GAME_ID};
  let result;
  try {
    result = await analytics.query({query: countQuery(true), params});
  } catch (error) {
    const compatibleFallback = error?.retryable === false && /_sample_interval/i.test(error?.message || "");
    if (!compatibleFallback) throw error;
    console.warn("sampling-aware game query was rejected; using binding-compatible count", error?.message || "unknown error");
    result = await analytics.query({query: countQuery(false), params});
  }
  return buildGameDashboardData(result.data || [], range, now, catalog);
};

const emptyGame = (id, metadata = null) => ({
  id,
  title: metadata?.title || `Uncataloged game: ${id}`,
  views: 0,
  starts: 0,
  completions: 0,
  replayClicks: 0,
  questionsAnswered: 0,
  firstTryCorrect: 0,
  difficulties: new Map(),
  mistakes: new Map(),
  metadata,
});

export const buildGameDashboardData = (rows, range, now = new Date(), catalog = {}) => {
  const metadata = catalog.games || GAME_METADATA;
  const games = new Map(Object.entries(metadata).map(([id, value]) => [id, emptyGame(id, value)]));
  for (const row of rows) {
    const rawId = String(row.index1 || "");
    if (!rawId.startsWith("game--")) continue;
    const id = rawId.slice(6);
    const game = games.get(id) || emptyGame(id);
    const eventType = row.blob1 || "";
    const difficulty = row.blob2 || "unrecorded";
    const category = row.blob3 || "";
    const events = Math.max(0, Number(row.eventCount) || 0);
    const value1 = Math.max(0, Number(row.value1) || 0);
    const value2 = Math.max(0, Number(row.value2) || 0);
    if (eventType === "game-view") game.views += events;
    if (eventType === "game-start" || eventType === "game-start-v2") game.starts += events;
    if (eventType === "game-complete" || eventType === "game-complete-v2") game.completions += events;
    if (eventType === "game-start-v2") {
      game.replayClicks += value1;
      const values = game.difficulties.get(difficulty) || {starts: 0, completions: 0};
      values.starts += events;
      game.difficulties.set(difficulty, values);
    }
    if (eventType === "game-complete-v2") {
      game.questionsAnswered += value1;
      game.firstTryCorrect += value2;
      const values = game.difficulties.get(difficulty) || {starts: 0, completions: 0};
      values.completions += events;
      game.difficulties.set(difficulty, values);
    }
    if (eventType === "game-mistakes" && category) {
      game.mistakes.set(category, (game.mistakes.get(category) || 0) + value1);
    }
    games.set(id, game);
  }
  const serialized = [...games.values()].map(game => {
    const tracksCompletion = game.metadata?.tracksCompletion !== false;
    return {
    id: game.id,
    title: game.title,
    views: game.views,
    starts: game.starts,
    completions: game.completions,
    completionRate: tracksCompletion ? (game.starts ? game.completions / game.starts : 0) : null,
    replayClicks: game.replayClicks,
    questionsAnswered: game.questionsAnswered,
    firstTryCorrect: game.firstTryCorrect,
    firstTryAccuracy: tracksCompletion ? (game.questionsAnswered ? game.firstTryCorrect / game.questionsAnswered : 0) : null,
    tracksCompletion,
    difficulties: [...game.difficulties.entries()].map(([id, values]) => ({
      id,
      label: game.metadata?.difficulties?.[id] || (id === "unrecorded" ? "Not recorded" : id),
      ...values,
    })),
    mistakes: [...game.mistakes.entries()]
      .map(([id, count]) => ({id, label: game.metadata?.categories?.[id] || id, count}))
      .sort((left, right) => right.count - left.count || left.label.localeCompare(right.label)),
    };
  }).sort((left, right) => right.starts - left.starts || left.title.localeCompare(right.title));
  const totals = serialized.reduce((value, game) => ({
    views: value.views + game.views,
    starts: value.starts + game.starts,
    completions: value.completions + game.completions,
    replayClicks: value.replayClicks + game.replayClicks,
    questionsAnswered: value.questionsAnswered + game.questionsAnswered,
    firstTryCorrect: value.firstTryCorrect + game.firstTryCorrect,
  }), {views: 0, starts: 0, completions: 0, replayClicks: 0, questionsAnswered: 0, firstTryCorrect: 0});
  const trackingGames = serialized.filter(game => game.tracksCompletion !== false);
  const trackingStarts = trackingGames.reduce((sum, game) => sum + game.starts, 0);
  const trackingCompletions = trackingGames.reduce((sum, game) => sum + game.completions, 0);
  const trackingQuestions = trackingGames.reduce((sum, game) => sum + game.questionsAnswered, 0);
  const trackingFirstTry = trackingGames.reduce((sum, game) => sum + game.firstTryCorrect, 0);
  return {
    range,
    generatedAt: now.toISOString(),
    timeZone: SITE_TIME_ZONE,
    metadataGameCount: Object.keys(metadata).length,
    metadataVersion: catalog.version || "bundled",
    metadataSource: catalog.source || "bundled",
    totals: {
      ...totals,
      completionRate: trackingGames.length ? (trackingStarts ? trackingCompletions / trackingStarts : 0) : null,
      firstTryAccuracy: trackingGames.length ? (trackingQuestions ? trackingFirstTry / trackingQuestions : 0) : null,
    },
    games: serialized,
  };
};

const escapeHtml = value => String(value).replace(/[&<>"']/g, character => ({
  "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;",
}[character]));
const percent = value => `${(value * 100).toFixed(1)}%`;
const percentOrNotTracked = value => value === null ? "Not tracked" : percent(value);

export const renderGameDashboard = (data, errorMessage = null) => {
  const nonce = crypto.randomUUID().replaceAll("-", "");
  const ranges = [["today", "Today"], ["7", "Last 7 days"], ["30", "Last 30 days"]];
  const range = data?.range || "7";
  const rows = (data?.games || []).map(game => `
    <details class="game">
      <summary><span><strong>${escapeHtml(game.title)}</strong><small>${game.starts.toLocaleString()} starts, ${game.completions.toLocaleString()} completions</small></span><b>${percentOrNotTracked(game.completionRate)}</b></summary>
      <div class="details">
        <p><strong>Replay clicks:</strong> ${game.replayClicks.toLocaleString()} &nbsp; <strong>First-try accuracy:</strong> ${percentOrNotTracked(game.firstTryAccuracy)}</p>
        <h3>Difficulty</h3>
        ${game.difficulties.length ? game.difficulties.map(item => `<div><span>${escapeHtml(item.label)}</span><strong>${item.starts.toLocaleString()} starts, ${item.completions.toLocaleString()} completions</strong></div>`).join("") : "<p>Detailed difficulty data starts after the game-side bridge is added.</p>"}
        <h3>Mistake categories</h3>
        ${game.mistakes.length ? game.mistakes.map(item => `<div><span>${escapeHtml(item.label)}</span><strong>${item.count.toLocaleString()}</strong></div>`).join("") : "<p>Detailed mistake data starts after the game-side bridge is added.</p>"}
      </div>
    </details>`).join("");
  const metadataLabel = !data ? "unavailable" : data.metadataSource === "bundled" ? "bundled fallback" : `${data.metadataSource} ${data.metadataVersion}`;
  return new Response(`<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Game analytics | Learning Made Simple</title><style nonce="${nonce}">${GAME_DASHBOARD_CSS}</style></head>
<body><main><header><p class="eyebrow">Learning Made Simple</p><h1>Game analytics</h1><p>Private, anonymous aggregate learning-game activity.</p></header>
<nav>${ranges.map(([value, label]) => `<a${range === value ? ' class="active"' : ""} href="/game-dashboard?range=${value}">${label}</a>`).join("")}</nav>
<section class="totals" aria-label="Game totals">
<article><span>Starts</span><strong>${data ? data.totals.starts.toLocaleString() : "-"}</strong></article>
<article><span>Completions</span><strong>${data ? data.totals.completions.toLocaleString() : "-"}</strong></article>
<article><span>Completion rate</span><strong>${data ? percentOrNotTracked(data.totals.completionRate) : "-"}</strong></article>
<article><span>First-try accuracy</span><strong>${data ? percentOrNotTracked(data.totals.firstTryAccuracy) : "-"}</strong></article>
<article><span>Replay clicks</span><strong>${data ? data.totals.replayClicks.toLocaleString() : "-"}</strong></article>
</section>
<p role="status"${errorMessage ? ' class="error"' : ""}>${errorMessage ? escapeHtml(errorMessage) : `Updated ${new Date(data.generatedAt).toLocaleString("en-US")}`}</p>
<p class="metadata">Game metadata: ${data ? data.metadataGameCount : "-"} games, ${escapeHtml(metadataLabel || "unavailable")}, dates use ${data?.timeZone || SITE_TIME_ZONE}</p>
<section><h2>Games</h2>${rows || "<p>No game activity in this period.</p>"}</section>
</main></body></html>`, {headers: gameDashboardHeaders("text/html; charset=utf-8", `default-src 'none'; style-src 'nonce-${nonce}'; img-src 'none'; base-uri 'none'; form-action 'none'; frame-ancestors 'none'`)});
};

export const gameDashboardHeaders = (contentType = "text/html; charset=utf-8", contentSecurityPolicy = "default-src 'none'; frame-ancestors 'none'") => ({
  "Content-Type": contentType,
  "Cache-Control": "no-store",
  "Content-Security-Policy": contentSecurityPolicy,
  "Referrer-Policy": "no-referrer",
  "X-Content-Type-Options": "nosniff",
  "X-Frame-Options": "DENY",
  "X-Robots-Tag": "noindex, nofollow, noarchive",
});

export const GAME_DASHBOARD_CSS = `
:root{font-family:system-ui,-apple-system,"Segoe UI",sans-serif;color:#183044;background:#f5f9f8}*{box-sizing:border-box}body{margin:0}main{width:min(100% - 2rem,72rem);margin:auto;padding:2rem 0 4rem}.eyebrow{color:#167d78;font-weight:800;margin:0}h1{font-size:clamp(2rem,5vw,3.25rem);margin:.3rem 0}header p:last-child,.metadata,[role=status],small{color:#607681}nav{display:flex;gap:.5rem;flex-wrap:wrap;margin:1.5rem 0}nav a{padding:.7rem 1rem;border:1px solid #bed7d4;border-radius:999px;color:#183044;background:#fff;text-decoration:none;font-weight:700}nav a.active{color:#fff;background:#167d78}.totals{display:grid;grid-template-columns:repeat(5,1fr);gap:.8rem}.totals article,.game{background:#fff;border:1px solid #dbe8e6;border-radius:1rem;box-shadow:0 4px 18px rgba(21,61,72,.06)}.totals article{padding:1rem}.totals span,small{display:block}.totals strong{font-size:1.8rem}.game{margin:.75rem 0;overflow:hidden}.game summary{display:flex;justify-content:space-between;align-items:center;gap:1rem;padding:1rem 1.2rem;cursor:pointer}.game summary b{font-size:1.2rem}.details{border-top:1px solid #e4eeec;padding:.8rem 1.2rem}.details div{display:flex;justify-content:space-between;gap:1rem;padding:.5rem 0;border-bottom:1px solid #edf3f2}.details h3{margin:1rem 0 .25rem}.error{color:#a52a2a;font-weight:700}@media(max-width:760px){main{width:min(100% - 1.2rem,72rem);padding-top:1.2rem}.totals{grid-template-columns:1fr 1fr}.game summary{padding:.9rem}}@media(max-width:420px){.totals{grid-template-columns:1fr}}
`;
