# PDF download analytics Worker

This Worker records aggregate clicks on worksheet PDF links from Learning Made Simple pages in Cloudflare Workers Analytics Engine. It stores only the resource id, download type, and page number. It does not read or store cookies, IP addresses, user agents, referrers, or visitor identifiers. Direct visits to CDN PDF URLs, bookmarks, and downloads initiated inside a browser PDF viewer are outside this client-side metric.

The configuration uses a `workers.dev` route and the `lms_download_clicks` Analytics Engine dataset. It does not enable Workers Paid or any paid Cloudflare service. Confirm that the Cloudflare account remains on the Workers Free plan before deployment.

## Test

```powershell
node --test cloudflare/download-analytics/test/worker.test.mjs
```

## Deploy after approval

```powershell
npx wrangler login
npx wrangler deploy --config cloudflare/download-analytics/wrangler.toml
```

The approved endpoint is `https://lms-download-analytics.rukhsana1409.workers.dev/download`. After deploying the Worker, verify `/health` before deploying the website.

The same Worker accepts aggregate learning-game events at `/game-event`. Game
payloads contain only a game id and one of `view`, `start`, or `complete`.
They use the existing Analytics Engine dataset with `game--` indexes and
`game-` event blobs. Download-dashboard queries explicitly retain only the
three PDF download event types, so game activity cannot change download totals.

## Game analytics contract

The game wrapper accepts same-origin `postMessage` events from the game iframe.
Future games should listen for the parent `initialize` message and answer with a
ready message before the learner can start. They may also send ready once at
load; the handshake prevents a fast iframe load from losing the message:

```javascript
window.parent.postMessage({
  source: "lms-game-analytics",
  version: 1,
  eventType: "ready"
}, window.location.origin);
```

Send a start message for each initial play or replay:

```javascript
window.parent.postMessage({
  source: "lms-game-analytics",
  version: 1,
  eventType: "start",
  difficulty: "easy",
  replay: false
}, window.location.origin);
```

Send one completion summary. Count a category once when a question is missed on
its first attempt so repeated taps do not inflate the mistake totals:

```javascript
window.parent.postMessage({
  source: "lms-game-analytics",
  version: 1,
  eventType: "complete",
  difficulty: "easy",
  questionsAnswered: 20,
  firstTryCorrect: 17,
  mistakeCategories: {"pick-greater": 2, "symbol-equal": 1}
}, window.location.origin);
```

Difficulty and category slugs and labels come from `catalog/games.json` and are
published automatically to `game-analytics-catalog.json`. The wrapper sends no
cookie, profile, persistent visitor id, IP address, user agent, or referrer.
Games without the bridge retain the legacy view, start, and completion totals.

## Private game dashboard deployment gate

The separate dashboard paths are `/game-dashboard` and
`/game-dashboard/data`. `GAME_DASHBOARD_ENABLED` stays `false` until a
Cloudflare Access application protects both `/game-dashboard` and
`/game-dashboard/*`. Verify anonymous requests to both paths receive an Access
login redirect while `/health`, `/download`, and `/game-event` remain public.
Only then set `GAME_DASHBOARD_ENABLED = "true"` and deploy the Worker.

The private dashboard uses `America/Detroit` calendar-day boundaries for Today, Last 7 days, and Last 30 days. The standard `site-tools/generate_production_runtime.py` publishing step writes `download-analytics-catalog.json` from the authoritative resource catalog and fails if the published counts differ. The website deploy therefore refreshes dashboard labels without requiring a separate Worker deploy. Dashboard requests use the hosted catalog URL by default and fetch that versioned snapshot without browser or CDN caching; `CATALOG_METADATA_URL` may override the default. The Worker-bundled metadata remains a read-only availability fallback. Events with resource ids that are absent from both snapshots remain included with an uncataloged-resource label so catalog drift cannot hide genuine clicks.

## Private CSV reports

Create a Cloudflare API token with `Account Analytics: Read`. Keep it in the environment and never commit it.

```powershell
$env:CLOUDFLARE_ACCOUNT_ID = '<account id>'
$env:CLOUDFLARE_API_TOKEN = '<read-only token>'
python site-tools/report_download_analytics.py --days 30
```

The command writes `worksheet-downloads.csv`, `worksheet-page-downloads.csv`, and `download-analytics-validation.csv` beneath `tmp/download-analytics/`. Events using the reserved `analytics-deployment-check` resource id appear only in the validation report and are excluded from worksheet and visitor totals.

## Private dashboard deployment gate

The Worker contains a read-only dashboard at `/dashboard`, backed by the account-scoped `ANALYTICS_SQL` binding. Its catalog labels and public metadata snapshot are generated automatically with the production runtime. To refresh them independently, run:

```powershell
python site-tools/generate_download_analytics_metadata.py
```

`DASHBOARD_ENABLED` remained `false` until a path-specific Cloudflare Access application protected both `/dashboard` and `/dashboard/*`, and anonymous requests to `/dashboard` and `/dashboard/data` were verified to receive Access login redirects. Do not protect the whole Worker because `/download` must remain public.
