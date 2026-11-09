import {renderAdminDashboard} from "./admin-dashboard.mjs";

const RESOURCE_ID_PATTERN = /^[a-z0-9]+(?:-[a-z0-9]+)*$/;
const UUID_PATTERN = /^[0-9a-f]{8}-[0-9a-f]{4}-[1-8][0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$/i;
const PUBLIC_PAGE_SIZE = 10;
const ADMIN_PAGE_SIZE = 50;
const MAX_BODY_BYTES = 4096;
const STATUS_VALUES = new Set(["pending", "approved", "rejected", "hidden"]);
const ACTION_TRANSITIONS = Object.freeze({
  approve: Object.freeze({from: new Set(["pending", "rejected"]), to: "approved"}),
  reject: Object.freeze({from: new Set(["pending"]), to: "rejected"}),
  hide: Object.freeze({from: new Set(["approved"]), to: "hidden"}),
  restore: Object.freeze({from: new Set(["hidden"]), to: "approved"}),
});
const catalogCache = new Map();
const CATALOG_CACHE_MILLISECONDS = 5 * 60 * 1000;

function json(data, status = 200, headers = {}) {
  return new Response(JSON.stringify(data), {
    status,
    headers: {"content-type": "application/json; charset=utf-8", ...headers},
  });
}

function enabled(value) {
  return value === "true";
}

function normalizeOptionalText(value, maximum, field) {
  if (value === undefined || value === null) return null;
  if (typeof value !== "string") throw new RequestError(400, `${field} must be text`);
  const normalized = value.replace(/\s+/gu, " ").trim();
  if (!normalized) return null;
  if ([...normalized].length > maximum) {
    throw new RequestError(400, `${field} must be ${maximum} characters or fewer`);
  }
  return normalized;
}

export function validateSubmission(input) {
  if (!input || typeof input !== "object" || Array.isArray(input)) {
    throw new RequestError(400, "request body must be an object");
  }
  const allowed = new Set(["submissionId", "rating", "name", "review", "turnstileToken", "website"]);
  const unsupported = Object.keys(input).filter((key) => !allowed.has(key));
  if (unsupported.length) throw new RequestError(400, "request body has unsupported fields");
  if (!UUID_PATTERN.test(input.submissionId ?? "")) {
    throw new RequestError(400, "submissionId must be a UUID");
  }
  if (!Number.isInteger(input.rating) || input.rating < 1 || input.rating > 5) {
    throw new RequestError(400, "rating must be an integer from 1 through 5");
  }
  if (typeof input.turnstileToken !== "string" || !input.turnstileToken || input.turnstileToken.length > 2048) {
    throw new RequestError(400, "turnstileToken is required");
  }
  if (input.website !== undefined && input.website !== "") {
    throw new RequestError(400, "invalid submission");
  }
  return {
    submissionId: input.submissionId.toLowerCase(),
    rating: input.rating,
    displayName: normalizeOptionalText(input.name, 50, "name"),
    reviewText: normalizeOptionalText(input.review, 500, "review"),
    turnstileToken: input.turnstileToken,
  };
}

class RequestError extends Error {
  constructor(status, message) {
    super(message);
    this.status = status;
  }
}

function requestId(request) {
  return request.headers.get("cf-ray") || crypto.randomUUID();
}

function auditLog(operation, outcome, correlationId, details = {}) {
  console.log(JSON.stringify({service: "resource-reviews", operation, outcome, correlationId, ...details}));
}

function corsHeaders(env) {
  return {
    "access-control-allow-origin": env.PUBLIC_ORIGIN,
    "access-control-allow-methods": "GET, POST, OPTIONS",
    "access-control-allow-headers": "content-type",
    "access-control-max-age": "86400",
    vary: "Origin",
  };
}

function requirePublicOrigin(request, env) {
  if (request.headers.get("origin") !== env.PUBLIC_ORIGIN) {
    throw new RequestError(403, "origin is not allowed");
  }
}

async function requireAdmin(request, env, context, requireOrigin) {
  if (!enabled(env.ADMIN_API_ENABLED)) throw new RequestError(404, "not found");
  if (requireOrigin && request.headers.get("origin") !== env.ADMIN_ORIGIN) {
    throw new RequestError(403, "origin is not allowed");
  }
  if (!context?.access || typeof context.access.getIdentity !== "function") {
    throw new RequestError(403, "Cloudflare Access authentication is required");
  }
  if (typeof env.ADMIN_EMAIL !== "string" || !env.ADMIN_EMAIL.trim()) {
    throw new RequestError(503, "admin identity is not configured");
  }
  let identity;
  try {
    identity = await context.access.getIdentity();
  } catch {
    throw new RequestError(403, "Cloudflare Access authentication is required");
  }
  if (typeof identity?.email !== "string" ||
      identity.email.toLocaleLowerCase("en-US") !== env.ADMIN_EMAIL.trim().toLocaleLowerCase("en-US")) {
    throw new RequestError(403, "Cloudflare Access authentication is required");
  }
}

async function parseJson(request) {
  const contentType = request.headers.get("content-type") || "";
  if (!contentType.toLowerCase().startsWith("application/json")) {
    throw new RequestError(415, "content-type must be application/json");
  }
  const declaredLength = Number(request.headers.get("content-length") || 0);
  if (declaredLength > MAX_BODY_BYTES) throw new RequestError(413, "request body is too large");
  const text = await request.text();
  if (new TextEncoder().encode(text).byteLength > MAX_BODY_BYTES) {
    throw new RequestError(413, "request body is too large");
  }
  try {
    return JSON.parse(text);
  } catch {
    throw new RequestError(400, "request body must be valid JSON");
  }
}

async function catalogResources(env, fetchImpl, timestamp) {
  const cached = catalogCache.get(env.RESOURCE_CATALOG_URL);
  if (cached && cached.expiresAt > timestamp) return cached.resources;
  const response = await fetchImpl(env.RESOURCE_CATALOG_URL, {
    headers: {accept: "application/json", "cache-control": "no-cache"},
  });
  if (!response.ok) throw new RequestError(503, "resource catalog is unavailable");
  const catalog = await response.json();
  if (!catalog?.resources || typeof catalog.resources !== "object" || Array.isArray(catalog.resources)) {
    throw new RequestError(503, "resource catalog is invalid");
  }
  const resources = new Map(Object.entries(catalog.resources).map(([id, resource]) => [id, resource.title]));
  catalogCache.set(env.RESOURCE_CATALOG_URL, {resources, expiresAt: timestamp + CATALOG_CACHE_MILLISECONDS});
  return resources;
}

async function catalogHasResource(resourceId, env, fetchImpl, timestamp) {
  return (await catalogResources(env, fetchImpl, timestamp)).has(resourceId);
}

async function verifyTurnstile(token, env, request, fetchImpl) {
  if (!env.TURNSTILE_SECRET) throw new RequestError(503, "review submissions are not configured");
  const body = new URLSearchParams({secret: env.TURNSTILE_SECRET, response: token});
  const sourceIp = request.headers.get("cf-connecting-ip");
  if (sourceIp) body.set("remoteip", sourceIp);
  let response;
  try {
    response = await fetchImpl("https://challenges.cloudflare.com/turnstile/v0/siteverify", {
      method: "POST",
      headers: {"content-type": "application/x-www-form-urlencoded"},
      body,
      signal: AbortSignal.timeout(10_000),
    });
  } catch {
    throw new RequestError(503, "review verification is temporarily unavailable");
  }
  if (!response.ok) throw new RequestError(503, "review verification is temporarily unavailable");
  const result = await response.json();
  if (!result.success || result.hostname !== env.TURNSTILE_HOSTNAME || result.action !== env.TURNSTILE_ACTION) {
    throw new RequestError(403, "review verification failed");
  }
}

async function contentHash(resourceId, submission) {
  const normalized = JSON.stringify([
    resourceId,
    submission.rating,
    submission.displayName?.toLocaleLowerCase("en-US") ?? "",
    submission.reviewText?.toLocaleLowerCase("en-US") ?? "",
  ]);
  const bytes = await crypto.subtle.digest("SHA-256", new TextEncoder().encode(normalized));
  return [...new Uint8Array(bytes)].map((value) => value.toString(16).padStart(2, "0")).join("");
}

export class D1ReviewStore {
  constructor(database) {
    if (!database) throw new RequestError(503, "review storage is not configured");
    this.database = database;
  }

  async publicReviews(resourceId, offset) {
    const [summary, reviews] = await this.database.batch([
      this.database.prepare(
        "SELECT COUNT(*) AS rating_count, AVG(rating) AS rating_average FROM reviews WHERE resource_id = ? AND status = 'approved'"
      ).bind(resourceId),
      this.database.prepare(
        "SELECT id, rating, COALESCE(display_name, 'Anonymous') AS display_name, review_text, created_at FROM reviews WHERE resource_id = ? AND status = 'approved' ORDER BY created_at DESC, id DESC LIMIT ? OFFSET ?"
      ).bind(resourceId, PUBLIC_PAGE_SIZE, offset),
    ]);
    return {
      ratingCount: Number(summary.results[0]?.rating_count || 0),
      ratingAverage: summary.results[0]?.rating_average === null ? null : Number(summary.results[0].rating_average),
      reviews: reviews.results,
      nextOffset: reviews.results.length === PUBLIC_PAGE_SIZE ? offset + PUBLIC_PAGE_SIZE : null,
    };
  }

  async insertPending(review) {
    const result = await this.database.prepare(
      "INSERT OR IGNORE INTO reviews (id, resource_id, rating, display_name, review_text, status, content_hash, duplicate_day, created_at, updated_at) VALUES (?, ?, ?, ?, ?, 'pending', ?, ?, ?, ?)"
    ).bind(
      review.id, review.resourceId, review.rating, review.displayName, review.reviewText,
      review.contentHash, review.duplicateDay, review.createdAt, review.createdAt
    ).run();
    if (Number(result.meta?.changes || 0) === 1) return "created";
    const existing = await this.database.prepare(
      "SELECT resource_id, rating, display_name, review_text FROM reviews WHERE id = ?"
    ).bind(review.id).first();
    if (!existing) return "duplicate-content";
    const same = existing.resource_id === review.resourceId && existing.rating === review.rating &&
      existing.display_name === review.displayName && existing.review_text === review.reviewText;
    if (!same) throw new RequestError(409, "submissionId was already used");
    return "idempotent-replay";
  }

  async adminReviews(status, offset) {
    const [countResult, reviewResult] = await this.database.batch([
      this.database.prepare("SELECT status, COUNT(*) AS count FROM reviews GROUP BY status"),
      this.database.prepare(
        "SELECT id, resource_id, rating, display_name, review_text, status, created_at, updated_at, moderated_at FROM reviews WHERE status = ? ORDER BY created_at ASC, id ASC LIMIT ? OFFSET ?"
      ).bind(status, ADMIN_PAGE_SIZE, offset),
    ]);
    const counts = Object.fromEntries([...STATUS_VALUES].map((value) => [value, 0]));
    for (const row of countResult.results) counts[row.status] = Number(row.count);
    return {counts, reviews: reviewResult.results, nextOffset: reviewResult.results.length === ADMIN_PAGE_SIZE ? offset + ADMIN_PAGE_SIZE : null};
  }

  async transition(reviewId, action, timestamp) {
    const transition = ACTION_TRANSITIONS[action];
    const current = await this.database.prepare("SELECT status FROM reviews WHERE id = ?").bind(reviewId).first();
    if (!current) throw new RequestError(404, "review not found");
    if (!transition.from.has(current.status)) throw new RequestError(409, `review cannot be ${action}d from ${current.status}`);
    const [result] = await this.database.batch([
      this.database.prepare(
        "UPDATE reviews SET status = ?, updated_at = ?, moderated_at = ? WHERE id = ? AND status = ?"
      ).bind(transition.to, timestamp, timestamp, reviewId, current.status),
      this.database.prepare(
        "INSERT INTO moderation_events (review_id, action, previous_status, resulting_status, moderator, created_at) SELECT ?, ?, ?, ?, 'owner', ? WHERE changes() = 1"
      ).bind(reviewId, action, current.status, transition.to, timestamp),
    ]);
    if (Number(result.meta?.changes || 0) !== 1) throw new RequestError(409, "review changed during moderation");
    return transition.to;
  }

  async permanentlyDelete(reviewId, timestamp) {
    const current = await this.database.prepare("SELECT status FROM reviews WHERE id = ?").bind(reviewId).first();
    if (!current) throw new RequestError(404, "review not found");
    const [result] = await this.database.batch([
      this.database.prepare("DELETE FROM reviews WHERE id = ? AND status = ?").bind(reviewId, current.status),
      this.database.prepare(
        "INSERT INTO moderation_events (review_id, action, previous_status, resulting_status, moderator, created_at) SELECT ?, 'delete', ?, NULL, 'owner', ? WHERE changes() = 1"
      ).bind(reviewId, current.status, timestamp),
    ]);
    if (Number(result.meta?.changes || 0) !== 1) throw new RequestError(409, "review changed during deletion");
  }

  async expireRejected(cutoff, timestamp) {
    const expired = await this.database.prepare(
      "SELECT id, status FROM reviews WHERE status = 'rejected' AND moderated_at < ? ORDER BY id"
    ).bind(cutoff).all();
    let deleted = 0;
    for (const review of expired.results) {
      const [result] = await this.database.batch([
        this.database.prepare(
          "DELETE FROM reviews WHERE id = ? AND status = 'rejected' AND moderated_at < ?"
        ).bind(review.id, cutoff),
        this.database.prepare(
          "INSERT INTO moderation_events (review_id, action, previous_status, resulting_status, moderator, created_at) SELECT ?, 'expire_rejected', 'rejected', NULL, 'owner', ? WHERE changes() = 1"
        ).bind(review.id, timestamp),
      ]);
      if (Number(result.meta?.changes || 0) === 1) {
        // The content-free audit row is written atomically by the batch above.
        deleted += 1;
      }
    }
    return deleted;
  }
}

function storeFrom(env) {
  return env.REVIEW_STORE || new D1ReviewStore(env.REVIEWS_DB);
}

function parseOffset(url) {
  const raw = url.searchParams.get("offset") || "0";
  if (!/^\d+$/.test(raw)) throw new RequestError(400, "offset must be a nonnegative integer");
  return Number(raw);
}

async function handlePublic(request, env, context, fetchImpl, now) {
  if (!enabled(env.PUBLIC_API_ENABLED)) throw new RequestError(404, "not found");
  const url = new URL(request.url);
  const match = url.pathname.match(/^\/v1\/resources\/([^/]+)\/reviews$/);
  if (!match || !RESOURCE_ID_PATTERN.test(match[1])) throw new RequestError(404, "not found");
  const resourceId = match[1];
  if (!(await catalogHasResource(resourceId, env, fetchImpl, now().getTime()))) throw new RequestError(404, "resource not found");
  const store = storeFrom(env);
  if (request.method === "GET") {
    const result = await store.publicReviews(resourceId, parseOffset(url));
    return json(result, 200, {...corsHeaders(env), "cache-control": "public, max-age=60"});
  }
  if (request.method !== "POST") throw new RequestError(405, "method not allowed");
  requirePublicOrigin(request, env);
  if (!env.REVIEW_RATE_LIMITER) throw new RequestError(503, "review rate limiting is not configured");
  const sourceKey = request.headers.get("cf-connecting-ip");
  if (!sourceKey) throw new RequestError(403, "source could not be verified");
  const limit = await env.REVIEW_RATE_LIMITER.limit({key: sourceKey});
  if (!limit.success) throw new RequestError(429, "too many review submissions");
  const submission = validateSubmission(await parseJson(request));
  await verifyTurnstile(submission.turnstileToken, env, request, fetchImpl);
  const timestamp = now().toISOString();
  const outcome = await store.insertPending({
    id: submission.submissionId,
    resourceId,
    rating: submission.rating,
    displayName: submission.displayName,
    reviewText: submission.reviewText,
    contentHash: await contentHash(resourceId, submission),
    duplicateDay: timestamp.slice(0, 10),
    createdAt: timestamp,
  });
  auditLog("submit_review", outcome, requestId(request));
  return json({status: "pending", message: "Thanks. Your rating was submitted for review."}, 202, corsHeaders(env));
}

function dashboardResponse() {
  const nonceBytes = crypto.getRandomValues(new Uint8Array(18));
  const nonce = btoa(String.fromCharCode(...nonceBytes));
  return new Response(renderAdminDashboard(nonce), {
    headers: {
      "content-type": "text/html; charset=utf-8",
      "cache-control": "no-store",
      "content-security-policy": `default-src 'none'; style-src 'nonce-${nonce}'; script-src 'nonce-${nonce}'; connect-src 'self'; base-uri 'none'; form-action 'none'; frame-ancestors 'none'`,
      "referrer-policy": "no-referrer",
      "x-content-type-options": "nosniff",
      "x-frame-options": "DENY",
    },
  });
}

async function handleAdmin(request, env, context, now, fetchImpl) {
  await requireAdmin(request, env, context, request.method !== "GET");
  const url = new URL(request.url);
  const store = storeFrom(env);
  if (request.method === "GET" && (url.pathname === "/admin" || url.pathname === "/admin/")) {
    return dashboardResponse();
  }
  if (request.method === "GET" && url.pathname === "/admin/api/reviews") {
    const status = url.searchParams.get("status") || "pending";
    if (!STATUS_VALUES.has(status)) throw new RequestError(400, "invalid status");
    const result = await store.adminReviews(status, parseOffset(url));
    const resources = await catalogResources(env, fetchImpl, now().getTime());
    result.reviews = result.reviews.map((review) => ({
      ...review,
      display_name: review.display_name || "Anonymous",
      resource_title: resources.get(review.resource_id) || `Uncataloged resource: ${review.resource_id}`,
    }));
    return json(result, 200, {"cache-control": "no-store"});
  }
  const actionMatch = url.pathname.match(/^\/admin\/api\/reviews\/([^/]+)\/(approve|reject|hide|restore)$/);
  if (request.method === "POST" && actionMatch) {
    if (!UUID_PATTERN.test(actionMatch[1])) throw new RequestError(400, "review id must be a UUID");
    const status = await store.transition(actionMatch[1], actionMatch[2], now().toISOString());
    auditLog("moderate_review", actionMatch[2], requestId(request));
    return json({status});
  }
  const deleteMatch = url.pathname.match(/^\/admin\/api\/reviews\/([^/]+)$/);
  if (request.method === "DELETE" && deleteMatch) {
    if (!UUID_PATTERN.test(deleteMatch[1])) throw new RequestError(400, "review id must be a UUID");
    const body = await parseJson(request);
    if (body?.confirm !== "PERMANENTLY DELETE") throw new RequestError(400, "permanent deletion confirmation is required");
    await store.permanentlyDelete(deleteMatch[1], now().toISOString());
    auditLog("delete_review", "succeeded", requestId(request));
    return new Response(null, {status: 204});
  }
  throw new RequestError(404, "not found");
}

export function createWorker({fetchImpl = fetch, now = () => new Date()} = {}) {
  return {
    async fetch(request, env, context) {
      const url = new URL(request.url);
      if (url.pathname === "/health" && request.method === "GET") {
        return json({ok: true, publicApiEnabled: enabled(env.PUBLIC_API_ENABLED), adminApiEnabled: enabled(env.ADMIN_API_ENABLED)});
      }
      try {
        if (request.method === "OPTIONS" && url.pathname.startsWith("/v1/")) {
          if (!enabled(env.PUBLIC_API_ENABLED)) throw new RequestError(404, "not found");
          requirePublicOrigin(request, env);
          return new Response(null, {status: 204, headers: corsHeaders(env)});
        }
        if (url.pathname.startsWith("/v1/")) return await handlePublic(request, env, context, fetchImpl, now);
        if (url.pathname.startsWith("/admin")) return await handleAdmin(request, env, context, now, fetchImpl);
        throw new RequestError(404, "not found");
      } catch (error) {
        if (error instanceof RequestError) return json({error: error.message}, error.status);
        auditLog("request", "failed", requestId(request), {errorClass: error?.constructor?.name || "Error"});
        return json({error: "internal server error"}, 500);
      }
    },
    async scheduled(_event, env) {
      const nowValue = now();
      const cutoff = new Date(nowValue.getTime() - 90 * 24 * 60 * 60 * 1000).toISOString();
      const expired = await storeFrom(env).expireRejected(cutoff, nowValue.toISOString());
      auditLog("expire_rejected_reviews", "succeeded", crypto.randomUUID(), {expired});
    },
  };
}

export default createWorker();
