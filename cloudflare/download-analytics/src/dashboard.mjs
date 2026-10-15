import {RESOURCE_METADATA} from "./resource-metadata.mjs";

const CONTROLLED_TEST_RESOURCE_ID = "analytics-deployment-check";
const RANGE_DAYS = Object.freeze({today: 0, "7": 7, "30": 30});

export const queryDashboardData = async (analytics, requestedRange, requestedOffset = "0", now = new Date()) => {
  const range = Object.hasOwn(RANGE_DAYS, requestedRange) ? requestedRange : "7";
  const parsedOffset = Number(requestedOffset);
  const offset = Number.isInteger(parsedOffset) && parsedOffset >= -840 && parsedOffset <= 840 ? parsedOffset : 0;
  const localNow = new Date(now.getTime() - offset * 60000);
  const start = range === "today"
    ? new Date(Date.UTC(localNow.getUTCFullYear(), localNow.getUTCMonth(), localNow.getUTCDate()) + offset * 60000)
    : new Date(now.getTime() - RANGE_DAYS[range] * 86400000);
  const result = await analytics.query({
    query: `
      SELECT index1, blob1, double1, COUNT(*) AS clicks
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
    if (resourceId === CONTROLLED_TEST_RESOURCE_ID || !Object.hasOwn(RESOURCE_METADATA, resourceId)) continue;
    const item = counts.get(resourceId) || {pack: 0, pages: new Map()};
    const clicks = Math.max(0, Number(row.clicks) || 0);
    const pageNumber = Number(row.double1 ?? row.page_number);
    const downloadType = row.blob1 ?? row.download_type;
    if (downloadType === "pack" && pageNumber === 0) item.pack += clicks;
    if (downloadType === "page" && Number.isInteger(pageNumber) && pageNumber >= 1) {
      item.pages.set(pageNumber, (item.pages.get(pageNumber) || 0) + clicks);
    }
    counts.set(resourceId, item);
  }

  const resources = Object.entries(RESOURCE_METADATA).map(([id, metadata]) => {
    const item = counts.get(id) || {pack: 0, pages: new Map()};
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
      totalClicks: item.pack + individualPageClicks,
      pages,
    };
  }).sort((left, right) => right.totalClicks - left.totalClicks || left.title.localeCompare(right.title));

  return {
    range,
    generatedAt: now.toISOString(),
    totals: resources.reduce((totals, resource) => ({
      totalClicks: totals.totalClicks + resource.totalClicks,
      fullPackClicks: totals.fullPackClicks + resource.fullPackClicks,
      individualPageClicks: totals.individualPageClicks + resource.individualPageClicks,
    }), {totalClicks: 0, fullPackClicks: 0, individualPageClicks: 0}),
    resources,
  };
};

export const renderDashboard = () => new Response(`<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="robots" content="noindex,nofollow,noarchive">
  <title>Download Analytics | Learning Made Simple</title>
  <link rel="stylesheet" href="/dashboard/styles.css">
</head>
<body>
  <main>
    <header><p class="eyebrow">Learning Made Simple</p><h1>PDF download analytics</h1><p>Private, aggregate worksheet download clicks.</p></header>
    <nav aria-label="Date range">
      <button data-range="today">Today</button><button data-range="7" class="active">Last 7 days</button><button data-range="30">Last 30 days</button>
    </nav>
    <section class="totals" aria-label="Download totals">
      <article><span>Total PDF clicks</span><strong id="total-clicks">—</strong></article>
      <article><span>Full-pack clicks</span><strong id="pack-clicks">—</strong></article>
      <article><span>Individual-page clicks</span><strong id="page-clicks">—</strong></article>
    </section>
    <p id="status" role="status">Loading analytics…</p>
    <section aria-labelledby="worksheet-heading"><h2 id="worksheet-heading">Worksheets</h2><div id="worksheets"></div></section>
  </main>
  <script src="/dashboard/app.js" defer></script>
</body>
</html>`, {headers: dashboardHeadersForDocument()});

const dashboardHeadersForDocument = () => ({
  "Content-Type": "text/html; charset=utf-8",
  "Cache-Control": "no-store",
  "Content-Security-Policy": "default-src 'none'; script-src 'self'; style-src 'self'; connect-src 'self'; img-src 'none'; base-uri 'none'; form-action 'none'; frame-ancestors 'none'",
  "Referrer-Policy": "no-referrer",
  "X-Content-Type-Options": "nosniff",
  "X-Frame-Options": "DENY",
  "X-Robots-Tag": "noindex, nofollow, noarchive",
});

const dashboardClient = () => {
  const number = new Intl.NumberFormat();
  const status = document.getElementById("status");
  const worksheets = document.getElementById("worksheets");
  const escape = (value) => String(value).replace(/[&<>\"']/g, character => ({"&":"&amp;","<":"&lt;",">":"&gt;",'\"':"&quot;","'":"&#39;"}[character]));
  const render = data => {
    document.getElementById("total-clicks").textContent = number.format(data.totals.totalClicks);
    document.getElementById("pack-clicks").textContent = number.format(data.totals.fullPackClicks);
    document.getElementById("page-clicks").textContent = number.format(data.totals.individualPageClicks);
    const active = data.resources.filter(resource => resource.totalClicks > 0);
    worksheets.innerHTML = (active.length ? active : data.resources).map(resource => `
      <details class="worksheet">
        <summary><span><strong>${escape(resource.title)}</strong><small>${number.format(resource.fullPackClicks)} packs · ${number.format(resource.individualPageClicks)} pages</small></span><b>${number.format(resource.totalClicks)}</b></summary>
        <div class="pages"><div><span>Complete pack</span><strong>${number.format(resource.fullPackClicks)}</strong></div>${resource.pages.map(page => `<div><span>Page ${page.number}: ${escape(page.label)}</span><strong>${number.format(page.clicks)}</strong></div>`).join("")}</div>
      </details>`).join("");
    status.textContent = active.length ? `Updated ${new Date(data.generatedAt).toLocaleString()}` : "No genuine worksheet downloads in this period.";
  };
  const load = async range => {
    status.textContent = "Loading analytics…";
    try {
      const offset = new Date().getTimezoneOffset();
      const response = await fetch(`/dashboard/data?range=${encodeURIComponent(range)}&offset=${offset}`, {credentials: "same-origin"});
      if (!response.ok) throw new Error("request failed");
      render(await response.json());
    } catch (_) { status.textContent = "Analytics are temporarily unavailable. Please try again."; }
  };
  document.querySelectorAll("[data-range]").forEach(button => button.addEventListener("click", () => {
    document.querySelectorAll("[data-range]").forEach(item => item.classList.toggle("active", item === button));
    load(button.dataset.range);
  }));
  load("7");
};

export const DASHBOARD_APP_JS = `(${dashboardClient.toString()})();`;

export const DASHBOARD_CSS = `
:root{color-scheme:light;font-family:system-ui,-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif;color:#183044;background:#f5f9f8}*{box-sizing:border-box}body{margin:0}main{width:min(100% - 2rem,72rem);margin:0 auto;padding:2rem 0 4rem}header{margin-bottom:1.5rem}.eyebrow{margin:0;color:#167d78;font-weight:800}h1{font-size:clamp(2rem,5vw,3.25rem);line-height:1.05;margin:.3rem 0}header p:last-child{color:#587080;margin:.5rem 0}nav{display:flex;gap:.5rem;flex-wrap:wrap;margin:1rem 0 1.5rem}button{border:1px solid #bed7d4;background:#fff;color:#183044;border-radius:999px;padding:.7rem 1rem;font:inherit;font-weight:700;cursor:pointer}button.active{background:#167d78;border-color:#167d78;color:#fff}.totals{display:grid;grid-template-columns:repeat(3,1fr);gap:1rem}.totals article,.worksheet{background:#fff;border:1px solid #dbe8e6;border-radius:1rem;box-shadow:0 4px 18px rgba(21,61,72,.06)}.totals article{padding:1.1rem}.totals span,.worksheet small{display:block;color:#607681}.totals strong{display:block;font-size:2rem;margin-top:.25rem}#status{color:#607681;min-height:1.5rem}h2{margin-top:2rem}.worksheet{margin:.75rem 0;overflow:hidden}.worksheet summary{display:flex;align-items:center;justify-content:space-between;gap:1rem;padding:1rem 1.2rem;cursor:pointer}.worksheet summary b{font-size:1.35rem}.pages{border-top:1px solid #e4eeec;padding:.35rem 1.2rem .8rem}.pages div{display:flex;justify-content:space-between;gap:1rem;padding:.55rem 0;border-bottom:1px solid #edf3f2}.pages div:last-child{border-bottom:0}@media(max-width:640px){main{width:min(100% - 1.2rem,72rem);padding-top:1.2rem}.totals{grid-template-columns:1fr}.totals article{display:flex;align-items:center;justify-content:space-between}.totals strong{font-size:1.6rem;margin:0}.worksheet summary{padding:.9rem}.pages{padding-left:.9rem;padding-right:.9rem}}
`;
