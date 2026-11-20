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
  SELECT index1, blob1,
    ${samplingAware ? "SUM(_sample_interval)" : "COUNT(*)"} AS eventCount
  FROM events.analyticsEngine."lms_download_clicks"
  WHERE timestamp >= $start
    AND index1 LIKE 'game--%'
    AND index1 != $controlledId
    AND blob1 IN ('game-start', 'game-complete', 'game-start-v2', 'game-complete-v2')
  GROUP BY index1, blob1
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
  starts: 0,
  completions: 0,
  metadata,
});

const completionRate = (starts, completions) => starts > 0 ? Math.round((completions / starts) * 100) : 0;

export const buildGameDashboardData = (rows, range, now = new Date(), catalog = {}) => {
  const metadata = catalog.games || GAME_METADATA;
  const games = new Map(Object.entries(metadata).map(([id, value]) => [id, emptyGame(id, value)]));
  for (const row of rows) {
    const rawId = String(row.index1 || "");
    if (!rawId.startsWith("game--")) continue;
    const id = rawId.slice(6);
    const game = games.get(id) || emptyGame(id);
    const eventType = row.blob1 || "";
    const events = Math.max(0, Number(row.eventCount) || 0);
    if (eventType === "game-start" || eventType === "game-start-v2") game.starts += events;
    if (eventType === "game-complete" || eventType === "game-complete-v2") game.completions += events;
    games.set(id, game);
  }
  const serialized = [...games.values()].map(game => ({
    id: game.id,
    title: game.title,
    starts: game.starts,
    completions: game.completions,
    completionRate: completionRate(game.starts, game.completions),
  })).sort((left, right) => right.starts - left.starts || left.title.localeCompare(right.title));
  const totals = serialized.reduce((value, game) => ({
    starts: value.starts + game.starts,
    completions: value.completions + game.completions,
  }), {starts: 0, completions: 0});
  totals.activeGames = serialized.filter(game => game.starts > 0 || game.completions > 0).length;
  totals.completionRate = completionRate(totals.starts, totals.completions);
  return {
    range,
    generatedAt: now.toISOString(),
    timeZone: SITE_TIME_ZONE,
    metadataGameCount: Object.keys(metadata).length,
    metadataVersion: catalog.version || "bundled",
    metadataSource: catalog.source || "bundled",
    totals,
    games: serialized,
  };
};

const escapeHtml = value => String(value).replace(/[&<>"']/g, character => ({
  "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;",
}[character]));

export const renderGameDashboard = (data, errorMessage = null) => {
  const nonce = crypto.randomUUID().replaceAll("-", "");
  const ranges = [["today", "Today"], ["7", "Last 7 days"], ["30", "Last 30 days"]];
  const range = data?.range || "7";
  const rows = (data?.games || []).map(game => `
    <article class="game"><strong>${escapeHtml(game.title)}</strong><span><b>${game.starts.toLocaleString()}</b><small>Starts</small></span><span><b>${game.completions.toLocaleString()}</b><small>Completions</small></span><span><b>${game.completionRate}%</b><small>Rate</small></span></article>`).join("");
  const metadataLabel = !data ? "unavailable" : data.metadataSource === "bundled" ? "bundled fallback" : `${data.metadataSource} ${data.metadataVersion}`;
  return new Response(`<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Game analytics | Learning Made Simple</title><style nonce="${nonce}">${GAME_DASHBOARD_CSS}</style></head>
<body><main><header><p class="eyebrow">Learning Made Simple</p><h1>Game analytics</h1><p>Private, anonymous aggregate learning-game activity.</p></header>
<nav>${ranges.map(([value, label]) => `<a${range === value ? ' class="active"' : ""} href="/game-dashboard?range=${value}">${label}</a>`).join("")}</nav>
<section class="totals" aria-label="Game totals">
<article><span>Starts</span><strong>${data ? data.totals.starts.toLocaleString() : "-"}</strong></article>
<article><span>Completions</span><strong>${data ? data.totals.completions.toLocaleString() : "-"}</strong></article>
<article><span>Completion rate</span><strong>${data ? `${data.totals.completionRate}%` : "-"}</strong></article>
<article><span>Active games</span><strong>${data ? data.totals.activeGames.toLocaleString() : "-"}</strong></article>
</section>
<p role="status"${errorMessage ? ' class="error"' : ""}>${errorMessage ? escapeHtml(errorMessage) : `Updated ${new Date(data.generatedAt).toLocaleString("en-US")}`}</p>
<p class="metadata">Game metadata: ${data ? data.metadataGameCount : "-"} games, ${escapeHtml(metadataLabel || "unavailable")}, dates use ${data?.timeZone || SITE_TIME_ZONE}</p>
<section class="games"><h2>Games</h2><div class="game-table" role="table" aria-label="Activity by game"><div class="game-head" role="row"><span>Game</span><span>Starts</span><span>Completions</span><span>Rate</span></div>${rows || '<p class="empty">No game activity in this period.</p>'}</div></section>
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
:root{font-family:system-ui,-apple-system,"Segoe UI",sans-serif;color:#183044;background:#f5f9f8}*{box-sizing:border-box}body{margin:0}main{width:min(100% - 2rem,68rem);margin:auto;padding:2rem 0 4rem}.eyebrow{color:#167d78;font-weight:800;margin:0}h1{font-size:clamp(2rem,5vw,3.1rem);margin:.25rem 0}h2{margin:1.75rem 0 .65rem}header p:last-child,.metadata,[role=status],small{color:#607681}nav{display:flex;gap:.5rem;flex-wrap:wrap;margin:1.35rem 0}nav a{padding:.6rem .9rem;border:1px solid #bed7d4;border-radius:999px;color:#183044;background:#fff;text-decoration:none;font-weight:700}nav a.active{color:#fff;background:#167d78}.totals{display:grid;grid-template-columns:repeat(4,1fr);gap:.7rem}.totals article,.game-table{background:#fff;border:1px solid #dbe8e6;border-radius:1rem;box-shadow:0 4px 18px rgba(21,61,72,.06)}.totals article{padding:.9rem 1rem}.totals span{display:block;font-size:.85rem;color:#607681}.totals strong{font-size:1.65rem}.game-table{overflow:hidden}.game-head,.game{display:grid;grid-template-columns:minmax(0,1fr) repeat(3,minmax(5rem,auto));align-items:center;gap:1rem}.game-head{padding:.7rem 1rem;background:#eaf5f3;color:#506873;font-size:.78rem;font-weight:800;text-transform:uppercase;letter-spacing:.04em}.game-head span:not(:first-child){text-align:right}.game{padding:.75rem 1rem;border-top:1px solid #e3eeec}.game strong{font-size:.98rem;min-width:0}.game span{text-align:right}.game span b{display:block;color:#183044;font-size:.95rem}.game span small{display:none}.empty{padding:1rem;margin:0}.error{color:#a52a2a;font-weight:700}@media(max-width:760px){main{width:min(100% - 1.2rem,68rem);padding-top:1.2rem}.totals{grid-template-columns:repeat(2,1fr)}.game-head{display:none}.game{grid-template-columns:minmax(0,1fr) repeat(3,minmax(3.7rem,auto));gap:.55rem;padding:.8rem}.game span small{display:block;font-size:.68rem}.game span b{font-size:.9rem}}@media(max-width:430px){.game{grid-template-columns:1fr repeat(3,minmax(3rem,1fr))}.game strong{grid-column:1/-1}.game span{text-align:left}.totals article{padding:.8rem}}
`;
