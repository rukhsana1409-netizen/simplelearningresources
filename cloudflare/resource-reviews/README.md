# Resource reviews Worker

This isolated Worker stores moderated worksheet ratings and reviews in D1. It is separate from PDF and game analytics. Both public and administrative APIs are disabled in `wrangler.toml` until their security prerequisites are verified.

## Local test

```powershell
node --test cloudflare/resource-reviews/test/*.test.mjs
```

## Required Cloudflare setup before deployment

1. Confirm the account remains on Workers Free.
2. Create a D1 database named `lms_resource_reviews` and add its database ID to the `REVIEWS_DB` binding in `wrangler.toml`.
3. Apply `migrations/0001_initial.sql` to the remote D1 database through Wrangler.
4. Create a managed Turnstile widget restricted to `simplelearningresources.com`.
5. Store its secret with `wrangler secret put TURNSTILE_SECRET`. Never put the secret in Git or frontend code.
6. Add the `REVIEW_RATE_LIMITER` binding after confirming the account supports the Workers Rate Limiting binding on its Free plan.
7. Deploy with `PUBLIC_API_ENABLED = "false"` and `ADMIN_API_ENABLED = "false"` first.
8. Create a Cloudflare Access self-hosted application for the Worker hostname with destinations `/admin` and `/admin/*`. Allow only the owner email.
9. Store that exact authorized email with `wrangler secret put ADMIN_EMAIL`. The Worker verifies the identity returned by `ctx.access.getIdentity()` in addition to the Access policy.
10. Verify anonymous requests to both admin paths are blocked while `/health` remains public.
11. Verify the Worker receives an authenticated identity through `ctx.access.getIdentity()`.
12. Set `ADMIN_API_ENABLED = "true"` only after Access and Worker-side identity checks pass.
13. Set `PUBLIC_API_ENABLED = "true"` only after the pilot page and privacy disclosures are approved for launch.

## API summary

- `GET /health` is always public and reports feature-gate state.
- `GET /v1/resources/:id/reviews` returns approved ratings only.
- `POST /v1/resources/:id/reviews` validates catalog membership, rate limit, Turnstile, and content, then creates a pending review.
- `GET /admin/api/reviews?status=pending` lists private moderation records.
- `POST /admin/api/reviews/:id/{approve|reject|hide|restore}` performs guarded transitions.
- `DELETE /admin/api/reviews/:id` requires `{ "confirm": "PERMANENTLY DELETE" }`.
- A daily cron removes rejected reviews more than 90 days after moderation. Pending and hidden reviews are never expired automatically.

No endpoint stores email addresses, IP addresses, cookies, user agents, or persistent visitor identifiers. Cloudflare may transiently use the request IP as a rate-limit key; it is not written to D1.

When the admin gate is eventually enabled, `GET /admin` serves the private responsive dashboard. It defaults to Pending, retrieves all four status counts with the selected review page, uses only same-origin moderation APIs, and carries a per-response CSP nonce. No review content is embedded in the dashboard HTML.

The Worker reads valid resource IDs from the existing catalog-derived `download-analytics-catalog.json` snapshot and caches only its ID set for five minutes per Worker isolate. New worksheet publications therefore need no hand-maintained review metadata.
