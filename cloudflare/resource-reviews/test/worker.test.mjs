import assert from "node:assert/strict";
import {test} from "node:test";
import {createWorker, validateSubmission} from "../src/worker.mjs";

const NOW = new Date("2026-11-09T15:00:00.000Z");
const RESOURCE_ID = "adding-tens-and-ones";
const SUBMISSION_ID = "550e8400-e29b-41d4-a716-446655440000";

class MemoryStore {
  constructor() {
    this.reviews = new Map();
    this.events = [];
  }

  async publicReviews(resourceId, offset) {
    const approved = [...this.reviews.values()]
      .filter((review) => review.resourceId === resourceId && review.status === "approved")
      .sort((left, right) => right.createdAt.localeCompare(left.createdAt));
    const ratings = approved.map((review) => review.rating);
    return {
      ratingCount: ratings.length,
      ratingAverage: ratings.length ? ratings.reduce((sum, value) => sum + value, 0) / ratings.length : null,
      reviews: approved.slice(offset, offset + 10).map((review) => ({
        id: review.id,
        rating: review.rating,
        display_name: review.displayName || "Anonymous",
        review_text: review.reviewText,
        created_at: review.createdAt,
      })),
      nextOffset: approved.length > offset + 10 ? offset + 10 : null,
    };
  }

  async insertPending(review) {
    const existing = this.reviews.get(review.id);
    if (existing) {
      const same = existing.resourceId === review.resourceId && existing.rating === review.rating &&
        existing.displayName === review.displayName && existing.reviewText === review.reviewText;
      if (!same) throw Object.assign(new Error("submissionId was already used"), {status: 409});
      return "idempotent-replay";
    }
    const duplicate = [...this.reviews.values()].some((candidate) =>
      candidate.resourceId === review.resourceId && candidate.contentHash === review.contentHash &&
      candidate.duplicateDay === review.duplicateDay
    );
    if (duplicate) return "duplicate-content";
    this.reviews.set(review.id, {...review, status: "pending", updatedAt: review.createdAt, moderatedAt: null});
    return "created";
  }

  async adminReviews(status, offset) {
    const reviews = [...this.reviews.values()].filter((review) => review.status === status).slice(offset, offset + 50);
    const counts = {pending: 0, approved: 0, rejected: 0, hidden: 0};
    for (const review of this.reviews.values()) counts[review.status] += 1;
    return {counts, reviews, nextOffset: null};
  }

  async transition(id, action, timestamp) {
    const transitions = {
      approve: {from: ["pending", "rejected"], to: "approved"}, reject: {from: ["pending"], to: "rejected"},
      hide: {from: ["approved"], to: "hidden"}, restore: {from: ["hidden"], to: "approved"},
    };
    const review = this.reviews.get(id);
    if (!review) throw Object.assign(new Error("review not found"), {status: 404});
    const transition = transitions[action];
    if (!transition.from.includes(review.status)) throw Object.assign(new Error("invalid transition"), {status: 409});
    const previous = review.status;
    review.status = transition.to;
    review.updatedAt = timestamp;
    review.moderatedAt = timestamp;
    this.events.push({id, action, previous, resulting: transition.to, moderator: "owner"});
    return transition.to;
  }

  async permanentlyDelete(id) {
    if (!this.reviews.delete(id)) throw Object.assign(new Error("review not found"), {status: 404});
    this.events.push({id, action: "delete", moderator: "owner"});
  }

  async expireRejected(cutoff) {
    let expired = 0;
    for (const [id, review] of this.reviews) {
      if (review.status === "rejected" && review.moderatedAt < cutoff) {
        this.reviews.delete(id);
        this.events.push({id, action: "expire_rejected", moderator: "owner"});
        expired += 1;
      }
    }
    return expired;
  }
}

function environment(store, overrides = {}) {
  return {
    PUBLIC_API_ENABLED: "true", ADMIN_API_ENABLED: "true",
    PUBLIC_ORIGIN: "https://simplelearningresources.com",
    ADMIN_ORIGIN: "https://lms-resource-reviews.rukhsana1409.workers.dev",
    ADMIN_EMAIL: "owner@example.com",
    RESOURCE_CATALOG_URL: "https://simplelearningresources.com/download-analytics-catalog.json",
    TURNSTILE_ACTION: "submit-resource-review", TURNSTILE_HOSTNAME: "simplelearningresources.com",
    TURNSTILE_SECRET: "test-secret", REVIEW_STORE: store,
    REVIEW_RATE_LIMITER: {limit: async () => ({success: true})}, ...overrides,
  };
}

function fetchStub(url, options = {}) {
  if (String(url).includes("download-analytics-catalog.json")) {
    return Promise.resolve(new Response(JSON.stringify({resources: {[RESOURCE_ID]: {title: "Adding Tens and Ones Within 100"}}})));
  }
  if (String(url).includes("siteverify")) {
    assert.equal(options.method, "POST");
    return Promise.resolve(new Response(JSON.stringify({success: true, hostname: "simplelearningresources.com", action: "submit-resource-review"})));
  }
  throw new Error(`unexpected fetch ${url}`);
}

function publicRequest(body, method = "POST") {
  return new Request(`https://reviews.example/v1/resources/${RESOURCE_ID}/reviews`, {
    method,
    headers: {origin: "https://simplelearningresources.com", "content-type": "application/json", "cf-connecting-ip": "192.0.2.1"},
    body: method === "POST" ? JSON.stringify(body) : undefined,
  });
}

function validBody(overrides = {}) {
  return {submissionId: SUBMISSION_ID, rating: 5, name: "", review: "Useful practice.", turnstileToken: "token", website: "", ...overrides};
}

function adminRequest(path, method = "GET", body) {
  return new Request(`https://lms-resource-reviews.rukhsana1409.workers.dev${path}`, {
    method,
    headers: {origin: "https://lms-resource-reviews.rukhsana1409.workers.dev", ...(body ? {"content-type": "application/json"} : {})},
    body: body ? JSON.stringify(body) : undefined,
  });
}

const accessContext = {access: {getIdentity: async () => ({email: "owner@example.com"})}};

test("all APIs remain disabled by default configuration", async () => {
  const worker = createWorker({fetchImpl: fetchStub, now: () => NOW});
  const env = environment(new MemoryStore(), {PUBLIC_API_ENABLED: "false", ADMIN_API_ENABLED: "false"});
  assert.equal((await worker.fetch(publicRequest(validBody()), env, {})).status, 404);
  assert.equal((await worker.fetch(adminRequest("/admin/api/reviews"), env, accessContext)).status, 404);
  const health = await (await worker.fetch(new Request("https://reviews.example/health"), env, {})).json();
  assert.deepEqual(health, {ok: true, publicApiEnabled: false, adminApiEnabled: false});
});

test("submission validation enforces rating, UUID, optional limits, and honeypot", () => {
  assert.equal(validateSubmission(validBody()).displayName, null);
  assert.throws(() => validateSubmission(validBody({rating: 0})), /rating/);
  assert.throws(() => validateSubmission(validBody({rating: 2.5})), /rating/);
  assert.throws(() => validateSubmission(validBody({submissionId: "not-a-uuid"})), /UUID/);
  assert.throws(() => validateSubmission(validBody({name: "n".repeat(51)})), /50/);
  assert.doesNotThrow(() => validateSubmission(validBody({review: "😀".repeat(500)})));
  assert.throws(() => validateSubmission(validBody({review: "😀".repeat(501)})), /500/);
  assert.throws(() => validateSubmission(validBody({website: "spam"})), /invalid/);
});

test("new submissions stay pending and idempotent replay does not duplicate", async () => {
  const store = new MemoryStore();
  const worker = createWorker({fetchImpl: fetchStub, now: () => NOW});
  const first = await worker.fetch(publicRequest(validBody()), environment(store), {});
  const replay = await worker.fetch(publicRequest(validBody()), environment(store), {});
  assert.equal(first.status, 202);
  assert.equal(replay.status, 202);
  assert.equal(store.reviews.size, 1);
  assert.equal(store.reviews.get(SUBMISSION_ID).status, "pending");
});

test("public results include only approved reviews in newest-first pages and use Anonymous", async () => {
  const store = new MemoryStore();
  store.reviews.set("a", {id: "a", resourceId: RESOURCE_ID, rating: 5, displayName: null, reviewText: null, status: "approved", createdAt: "2026-11-08T00:00:00Z"});
  store.reviews.set("b", {id: "b", resourceId: RESOURCE_ID, rating: 3, displayName: "Pat", reviewText: "Okay", status: "approved", createdAt: "2026-11-09T00:00:00Z"});
  store.reviews.set("c", {id: "c", resourceId: RESOURCE_ID, rating: 1, displayName: "Hidden", reviewText: "No", status: "hidden", createdAt: "2026-11-10T00:00:00Z"});
  const worker = createWorker({fetchImpl: fetchStub, now: () => NOW});
  const response = await worker.fetch(publicRequest(null, "GET"), environment(store), {});
  const data = await response.json();
  assert.equal(data.ratingCount, 2);
  assert.equal(data.ratingAverage, 4);
  assert.deepEqual(data.reviews.map((review) => review.id), ["b", "a"]);
  assert.equal(data.reviews[1].display_name, "Anonymous");
});

test("Turnstile and rate limiting fail closed before storage writes", async () => {
  const store = new MemoryStore();
  const worker = createWorker({fetchImpl: fetchStub, now: () => NOW});
  const limited = await worker.fetch(publicRequest(validBody()), environment(store, {REVIEW_RATE_LIMITER: {limit: async () => ({success: false})}}), {});
  assert.equal(limited.status, 429);
  const badTurnstile = createWorker({fetchImpl: async (url) => String(url).includes("catalog")
    ? new Response(JSON.stringify({resources: {[RESOURCE_ID]: {}}}))
    : new Response(JSON.stringify({success: false})), now: () => NOW});
  assert.equal((await badTurnstile.fetch(publicRequest(validBody()), environment(store), {})).status, 403);
  assert.equal(store.reviews.size, 0);
});

test("admin routes require Access context and exact origin", async () => {
  const worker = createWorker({fetchImpl: fetchStub, now: () => NOW});
  const env = environment(new MemoryStore());
  assert.equal((await worker.fetch(adminRequest("/admin/api/reviews"), env, {})).status, 403);
  const wrongOwner = {access: {getIdentity: async () => ({email: "someone-else@example.com"})}};
  assert.equal((await worker.fetch(adminRequest("/admin/api/reviews"), env, wrongOwner)).status, 403);
  const invalidAccessContext = {access: {identity: {email: "owner@example.com"}}};
  assert.equal((await worker.fetch(adminRequest("/admin/api/reviews"), env, invalidAccessContext)).status, 403);
  const wrongOrigin = new Request(`https://reviews.example/admin/api/reviews/${SUBMISSION_ID}/approve`, {
    method: "POST", headers: {origin: "https://evil.example"},
  });
  assert.equal((await worker.fetch(wrongOrigin, env, accessContext)).status, 403);
  const authenticatedReadWithoutOrigin = new Request("https://reviews.example/admin/api/reviews");
  assert.equal((await worker.fetch(authenticatedReadWithoutOrigin, env, accessContext)).status, 200);
});

test("authenticated dashboard is private, nonce-protected, and not cached", async () => {
  const worker = createWorker({fetchImpl: fetchStub, now: () => NOW});
  const env = environment(new MemoryStore());
  const unauthenticated = await worker.fetch(new Request("https://reviews.example/admin"), env, {});
  assert.equal(unauthenticated.status, 403);
  const response = await worker.fetch(new Request("https://reviews.example/admin"), env, accessContext);
  assert.equal(response.status, 200);
  assert.equal(response.headers.get("cache-control"), "no-store");
  assert.match(response.headers.get("content-security-policy"), /default-src 'none'/);
  const html = await response.text();
  assert.match(html, /Review Management/);
  assert.match(html, /role="tablist"/);
  assert.match(html, /data-status="pending"/);
  assert.match(html, /data-status="approved"/);
  assert.match(html, /data-status="rejected"/);
  assert.match(html, /data-status="hidden"/);
  assert.match(html, /Permanently delete/);
  assert.doesNotMatch(html, /owner@example\.com/);
});

test("admin review API returns status counts and catalog worksheet titles", async () => {
  const store = new MemoryStore();
  store.reviews.set("pending-one", {id: "pending-one", resourceId: RESOURCE_ID, resource_id: RESOURCE_ID, rating: 4, displayName: null, display_name: null, reviewText: "Clear pages.", review_text: "Clear pages.", status: "pending", createdAt: NOW.toISOString(), created_at: NOW.toISOString()});
  store.reviews.set("approved-one", {id: "approved-one", resourceId: RESOURCE_ID, resource_id: RESOURCE_ID, rating: 5, displayName: "Pat", display_name: "Pat", reviewText: null, review_text: null, status: "approved", createdAt: NOW.toISOString(), created_at: NOW.toISOString()});
  const worker = createWorker({fetchImpl: fetchStub, now: () => NOW});
  const response = await worker.fetch(new Request("https://reviews.example/admin/api/reviews?status=pending"), environment(store), accessContext);
  const data = await response.json();
  assert.equal(response.status, 200);
  assert.deepEqual(data.counts, {pending: 1, approved: 1, rejected: 0, hidden: 0});
  assert.equal(data.reviews[0].resource_title, "Adding Tens and Ones Within 100");
  assert.equal(data.reviews[0].display_name, "Anonymous");
});

test("CORS preflight rejects untrusted origins without throwing", async () => {
  const worker = createWorker({fetchImpl: fetchStub, now: () => NOW});
  const request = new Request(`https://reviews.example/v1/resources/${RESOURCE_ID}/reviews`, {
    method: "OPTIONS", headers: {origin: "https://evil.example"},
  });
  const response = await worker.fetch(request, environment(new MemoryStore()), {});
  assert.equal(response.status, 403);
  assert.equal(response.headers.get("access-control-allow-origin"), null);
});

test("moderation transitions control public aggregates", async () => {
  const store = new MemoryStore();
  const worker = createWorker({fetchImpl: fetchStub, now: () => NOW});
  const env = environment(store);
  await worker.fetch(publicRequest(validBody()), env, {});
  let publicData = await (await worker.fetch(publicRequest(null, "GET"), env, {})).json();
  assert.equal(publicData.ratingCount, 0);
  assert.equal((await worker.fetch(adminRequest(`/admin/api/reviews/${SUBMISSION_ID}/approve`, "POST"), env, accessContext)).status, 200);
  publicData = await (await worker.fetch(publicRequest(null, "GET"), env, {})).json();
  assert.equal(publicData.ratingCount, 1);
  assert.equal((await worker.fetch(adminRequest(`/admin/api/reviews/${SUBMISSION_ID}/hide`, "POST"), env, accessContext)).status, 200);
  publicData = await (await worker.fetch(publicRequest(null, "GET"), env, {})).json();
  assert.equal(publicData.ratingCount, 0);
  assert.equal((await worker.fetch(adminRequest(`/admin/api/reviews/${SUBMISSION_ID}/restore`, "POST"), env, accessContext)).status, 200);
  assert.equal(store.events.every((event) => event.moderator === "owner"), true);
});

test("rejected reviews never affect public aggregates and can be permanently deleted", async () => {
  const store = new MemoryStore();
  const worker = createWorker({fetchImpl: fetchStub, now: () => NOW});
  const env = environment(store);
  await worker.fetch(publicRequest(validBody()), env, {});
  assert.equal((await worker.fetch(adminRequest(`/admin/api/reviews/${SUBMISSION_ID}/reject`, "POST"), env, accessContext)).status, 200);
  const publicData = await (await worker.fetch(publicRequest(null, "GET"), env, {})).json();
  assert.equal(publicData.ratingCount, 0);
  assert.equal(publicData.ratingAverage, null);
  assert.deepEqual(publicData.reviews, []);
  assert.equal((await worker.fetch(adminRequest(`/admin/api/reviews/${SUBMISSION_ID}`, "DELETE", {confirm: "PERMANENTLY DELETE"}), env, accessContext)).status, 204);
  assert.equal(store.reviews.size, 0);
});

test("permanent delete requires exact confirmation", async () => {
  const store = new MemoryStore();
  const worker = createWorker({fetchImpl: fetchStub, now: () => NOW});
  const env = environment(store);
  await worker.fetch(publicRequest(validBody()), env, {});
  const path = `/admin/api/reviews/${SUBMISSION_ID}`;
  assert.equal((await worker.fetch(adminRequest(path, "DELETE", {confirm: "DELETE"}), env, accessContext)).status, 400);
  assert.equal((await worker.fetch(adminRequest(path, "DELETE", {confirm: "PERMANENTLY DELETE"}), env, accessContext)).status, 204);
  assert.equal(store.reviews.size, 0);
  assert.equal(store.events.at(-1).action, "delete");
});

test("scheduled cleanup deletes only rejected reviews older than 90 days", async () => {
  const store = new MemoryStore();
  store.reviews.set("old", {id: "old", status: "rejected", moderatedAt: "2026-08-01T00:00:00Z"});
  store.reviews.set("new", {id: "new", status: "rejected", moderatedAt: "2026-11-01T00:00:00Z"});
  store.reviews.set("pending", {id: "pending", status: "pending", moderatedAt: null});
  store.reviews.set("hidden", {id: "hidden", status: "hidden", moderatedAt: "2026-01-01T00:00:00Z"});
  const worker = createWorker({fetchImpl: fetchStub, now: () => NOW});
  await worker.scheduled({}, environment(store));
  assert.deepEqual([...store.reviews.keys()].sort(), ["hidden", "new", "pending"]);
  assert.equal(store.events.at(-1).action, "expire_rejected");
});
