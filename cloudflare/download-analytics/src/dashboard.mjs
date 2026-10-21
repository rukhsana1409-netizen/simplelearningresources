import {RESOURCE_METADATA} from "./resource-metadata.mjs";

const CONTROLLED_TEST_RESOURCE_ID = "analytics-deployment-check";
const RANGE_DAYS = Object.freeze({today: 0, "7": 7, "30": 30});
export const SITE_TIME_ZONE = "America/Detroit";

const zonedParts = (date, timeZone) => Object.fromEntries(
  new Intl.DateTimeFormat("en-US", {
    timeZone,
    year: "numeric",
    month: "2-digit",
    day: "2-digit",
    hour: "2-digit",
    minute: "2-digit",
    second: "2-digit",
    hourCycle: "h23",
  }).formatToParts(date)
    .filter(part => part.type !== "literal")
    .map(part => [part.type, Number(part.value)]),
);

export const startOfLocalDay = (year, month, day, timeZone = SITE_TIME_ZONE) => {
  const target = Date.UTC(year, month - 1, day);
  let instant = target;
  for (let attempt = 0; attempt < 3; attempt += 1) {
    const parts = zonedParts(new Date(instant), timeZone);
    const represented = Date.UTC(parts.year, parts.month - 1, parts.day, parts.hour, parts.minute, parts.second);
    instant -= represented - target;
  }
  return new Date(instant);
};

export const rangeStart = (requestedRange, now = new Date()) => {
  const range = Object.hasOwn(RANGE_DAYS, requestedRange) ? requestedRange : "7";
  const local = zonedParts(now, SITE_TIME_ZONE);
  const daysBack = range === "today" ? 0 : RANGE_DAYS[range] - 1;
  const targetDate = new Date(Date.UTC(local.year, local.month - 1, local.day - daysBack));
  return startOfLocalDay(
    targetDate.getUTCFullYear(),
    targetDate.getUTCMonth() + 1,
    targetDate.getUTCDate(),
  );
};

export const queryDashboardData = async (analytics, requestedRange, now = new Date()) => {
  const range = Object.hasOwn(RANGE_DAYS, requestedRange) ? requestedRange : "7";
  const start = rangeStart(range, now);
  const result = await analytics.query({
    query: `
      SELECT index1, blob1, double1, SUM(_sample_interval) AS clicks
      FROM events.analyticsEngine."lms_download_clicks"
      WHERE timestamp >= $start AND index1 != $controlledId
      GROUP BY index1, blob1, double1
    `,
    params: {start: start.toISOString(), controlledId: CONTROLLED_TEST_RESOURCE_ID},
  });
  return buildDashboardData(result.data || [], range, now);
};

export const buildDashboardData = (rows, range, now = new Date()) => {
  const counts = new Map();
  for (const row of rows) {
    const resourceId = String(row.index1 ?? row.resource_id);
    if (resourceId === CONTROLLED_TEST_RESOURCE_ID) continue;
    const item = counts.get(resourceId) || {pack: 0, supporting: 0, pages: new Map()};
    const clicks = Math.max(0, Number(row.clicks) || 0);
    const pageNumber = Number(row.double1 ?? row.page_number);
    const downloadType = row.blob1 ?? row.download_type;
    if (downloadType === "pack" && pageNumber === 0) item.pack += clicks;
    if (downloadType === "supporting" && pageNumber === 0) item.supporting += clicks;
    if (downloadType === "page" && Number.isInteger(pageNumber) && pageNumber >= 1) {
      item.pages.set(pageNumber, (item.pages.get(pageNumber) || 0) + clicks);
    }
    counts.set(resourceId, item);
  }

  const knownResources = Object.entries(RESOURCE_METADATA).map(([id, metadata]) => {
    const item = counts.get(id) || {pack: 0, supporting: 0, pages: new Map()};
    const pages = metadata.pages.map((label, index) => ({
      number: index + 1,
      label,
      clicks: item.pages.get(index + 1) || 0,
    }));
    const individualPageClicks = pages.reduce((total, page) => total + page.clicks, 0);
    return {
      id,
      title: metadata.title,
      fullPackClicks: item.pack,
      individualPageClicks,
      supportingPdfClicks: item.supporting,
      totalClicks: item.pack + individualPageClicks + item.supporting,
      pages,
    };
  });
  const unknownResources = [...counts.entries()]
    .filter(([id]) => !Object.hasOwn(RESOURCE_METADATA, id))
    .map(([id, item]) => {
      const pages = [...item.pages.entries()]
        .sort(([left], [right]) => left - right)
        .map(([number, clicks]) => ({number, label: `Page ${number}`, clicks}));
      const individualPageClicks = pages.reduce((total, page) => total + page.clicks, 0);
      return {
        id,
        title: `Uncataloged resource: ${id}`,
        fullPackClicks: item.pack,
        individualPageClicks,
        supportingPdfClicks: item.supporting,
        totalClicks: item.pack + individualPageClicks + item.supporting,
        pages,
      };
    });
  const resources = [...knownResources, ...unknownResources]
    .sort((left, right) => right.totalClicks - left.totalClicks || left.title.localeCompare(right.title));

  return {
    range,
    generatedAt: now.toISOString(),
    timeZone: SITE_TIME_ZONE,
    metadataResourceCount: Object.keys(RESOURCE_METADATA).length,
    totals: resources.reduce((totals, resource) => ({
      totalClicks: totals.totalClicks + resource.totalClicks,
      fullPackClicks: totals.fullPackClicks + resource.fullPackClicks,
      individualPageClicks: totals.individualPageClicks + resource.individualPageClicks,
      supportingPdfClicks: totals.supportingPdfClicks + resource.supportingPdfClicks,
    }), {totalClicks: 0, fullPackClicks: 0, individualPageClicks: 0, supportingPdfClicks: 0}),
    resources,
  };
};

const escapeHtml = (value) => String(value).replace(/[&<>"']/g, character => ({
  "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;",
})[character]);

export const renderDashboard = (data, errorMessage = null) => {
  const nonce = crypto.randomUUID().replaceAll("-", "");
  const resources = data?.resources || [];
  const activeResources = resources.filter(resource => resource.totalClicks > 0);
  const displayedResources = activeResources.length ? activeResources : resources;
  const range = data?.range || "7";
  const worksheetRows = displayedResources.map(resource => `
      <details class="worksheet">
        <summary><span><strong>${escapeHtml(resource.title)}</strong><small>${resource.fullPackClicks.toLocaleString()} packs · ${resource.individualPageClicks.toLocaleString()} pages · ${resource.supportingPdfClicks.toLocaleString()} supporting PDFs</small></span><b>${resource.totalClicks.toLocaleString()}</b></summary>
        <div class="pages"><div><span>Complete pack</span><strong>${resource.fullPackClicks.toLocaleString()}</strong></div><div><span>Supporting PDFs</span><strong>${resource.supportingPdfClicks.toLocaleString()}</strong></div>${resource.pages.map(page => `<div><span>Page ${page.number}: ${escapeHtml(page.label)}</span><strong>${page.clicks.toLocaleString()}</strong></div>`).join("")}</div>
      </details>`).join("");
  const statusMessage = errorMessage
    ? escapeHtml(errorMessage)
    : activeResources.length
      ? `Updated ${new Date(data.generatedAt).toLocaleString("en-US")}`
      : "No genuine worksheet downloads in this period.";
  return new Response(`<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="robots" content="noindex,nofollow,noarchive">
  <title>Download Analytics | Learning Made Simple</title>
  <style nonce="${nonce}">${DASHBOARD_CSS}</style>
</head>
<body>
  <main>
    <header><p class="eyebrow">Learning Made Simple</p><h1>PDF link analytics</h1><p>Private, aggregate clicks on worksheet PDF links from the Learning Made Simple website.</p></header>
    <nav aria-label="Date range">
      <a href="/dashboard?range=today"${range === "today" ? ' class="active" aria-current="page"' : ""}>Today</a><a href="/dashboard?range=7"${range === "7" ? ' class="active" aria-current="page"' : ""}>Last 7 days</a><a href="/dashboard?range=30"${range === "30" ? ' class="active" aria-current="page"' : ""}>Last 30 days</a>
    </nav>
    <section class="totals" aria-label="Download totals">
      <article><span>Total PDF clicks</span><strong>${data ? data.totals.totalClicks.toLocaleString() : "—"}</strong></article>
      <article><span>Full-pack clicks</span><strong>${data ? data.totals.fullPackClicks.toLocaleString() : "—"}</strong></article>
      <article><span>Individual-page clicks</span><strong>${data ? data.totals.individualPageClicks.toLocaleString() : "—"}</strong></article>
      <article><span>Supporting-PDF clicks</span><strong>${data ? data.totals.supportingPdfClicks.toLocaleString() : "—"}</strong></article>
    </section>
    <p id="status" role="status"${errorMessage ? ' class="error"' : ""}>${statusMessage}</p>
    <p class="metadata-status">Catalog metadata: ${data ? data.metadataResourceCount.toLocaleString() : "—"} resources · Dates use ${data ? escapeHtml(data.timeZone) : SITE_TIME_ZONE}</p>
    <section aria-labelledby="worksheet-heading"><h2 id="worksheet-heading">Worksheets</h2><div id="worksheets">${worksheetRows}</div></section>
  </main>
</body>
</html>`, {headers: dashboardHeadersForDocument(nonce)});
};

const dashboardHeadersForDocument = (nonce) => ({
  "Content-Type": "text/html; charset=utf-8",
  "Cache-Control": "no-store",
  "Content-Security-Policy": `default-src 'none'; style-src 'nonce-${nonce}'; img-src 'none'; base-uri 'none'; form-action 'none'; frame-ancestors 'none'`,
  "Referrer-Policy": "no-referrer",
  "X-Content-Type-Options": "nosniff",
  "X-Frame-Options": "DENY",
  "X-Robots-Tag": "noindex, nofollow, noarchive",
});

export const DASHBOARD_CSS = `
:root{color-scheme:light;font-family:system-ui,-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif;color:#183044;background:#f5f9f8}*{box-sizing:border-box}body{margin:0}main{width:min(100% - 2rem,72rem);margin:0 auto;padding:2rem 0 4rem}header{margin-bottom:1.5rem}.eyebrow{margin:0;color:#167d78;font-weight:800}h1{font-size:clamp(2rem,5vw,3.25rem);line-height:1.05;margin:.3rem 0}header p:last-child{color:#587080;margin:.5rem 0}nav{display:flex;gap:.5rem;flex-wrap:wrap;margin:1rem 0 1.5rem}nav a{border:1px solid #bed7d4;background:#fff;color:#183044;border-radius:999px;padding:.7rem 1rem;font:inherit;font-weight:700;text-decoration:none}nav a.active{background:#167d78;border-color:#167d78;color:#fff}.totals{display:grid;grid-template-columns:repeat(4,1fr);gap:1rem}.totals article,.worksheet{background:#fff;border:1px solid #dbe8e6;border-radius:1rem;box-shadow:0 4px 18px rgba(21,61,72,.06)}.totals article{padding:1.1rem}.totals span,.worksheet small{display:block;color:#607681}.totals strong{display:block;font-size:2rem;margin-top:.25rem}#status{color:#607681;min-height:1.5rem}#status.error{color:#a52a2a;font-weight:700}h2{margin-top:2rem}.worksheet{margin:.75rem 0;overflow:hidden}.worksheet summary{display:flex;align-items:center;justify-content:space-between;gap:1rem;padding:1rem 1.2rem;cursor:pointer}.worksheet summary b{font-size:1.35rem}.pages{border-top:1px solid #e4eeec;padding:.35rem 1.2rem .8rem}.pages div{display:flex;justify-content:space-between;gap:1rem;padding:.55rem 0;border-bottom:1px solid #edf3f2}.pages div:last-child{border-bottom:0}@media(max-width:640px){main{width:min(100% - 1.2rem,72rem);padding-top:1.2rem}.totals{grid-template-columns:1fr}.totals article{display:flex;align-items:center;justify-content:space-between}.totals strong{font-size:1.6rem;margin:0}.worksheet summary{padding:.9rem}.pages{padding-left:.9rem;padding-right:.9rem}}
`;
