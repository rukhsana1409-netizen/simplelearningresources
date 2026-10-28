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

The private dashboard uses `America/Detroit` calendar-day boundaries for Today, Last 7 days, and Last 30 days. The standard `site-tools/generate_production_runtime.py` publishing step writes `download-analytics-catalog.json` from the authoritative resource catalog and fails if the published counts differ. The website deploy therefore refreshes dashboard labels without requiring a separate Worker deploy. Dashboard requests fetch that versioned snapshot without browser or CDN caching; the Worker-bundled metadata remains a read-only fallback. Events with resource ids that are absent from both snapshots remain included with an uncataloged-resource label so catalog drift cannot hide genuine clicks.

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
