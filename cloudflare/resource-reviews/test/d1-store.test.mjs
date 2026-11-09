import assert from "node:assert/strict";
import {readFile} from "node:fs/promises";
import {DatabaseSync} from "node:sqlite";
import {test} from "node:test";
import {D1ReviewStore} from "../src/worker.mjs";

class StatementAdapter {
  constructor(database, sql, parameters = []) {
    this.database = database;
    this.sql = sql;
    this.parameters = parameters;
  }

  bind(...parameters) {
    return new StatementAdapter(this.database, this.sql, parameters);
  }

  first() {
    return this.database.prepare(this.sql).get(...this.parameters) ?? null;
  }

  all() {
    return {results: this.database.prepare(this.sql).all(...this.parameters)};
  }

  run() {
    const result = this.database.prepare(this.sql).run(...this.parameters);
    return {meta: {changes: Number(result.changes)}};
  }

  execute() {
    return /^\s*SELECT\b/i.test(this.sql) ? this.all() : this.run();
  }
}

class D1Adapter {
  constructor(database) {
    this.database = database;
  }

  prepare(sql) {
    return new StatementAdapter(this.database, sql);
  }

  batch(statements) {
    this.database.exec("BEGIN IMMEDIATE");
    try {
      const results = statements.map((statement) => statement.execute());
      this.database.exec("COMMIT");
      return results;
    } catch (error) {
      this.database.exec("ROLLBACK");
      throw error;
    }
  }
}

test("D1 store keeps moderation state, public aggregates, and audit rows consistent", async () => {
  const database = new DatabaseSync(":memory:");
  database.exec(await readFile(new URL("../migrations/0001_initial.sql", import.meta.url), "utf8"));
  const store = new D1ReviewStore(new D1Adapter(database));
  const review = {
    id: "550e8400-e29b-41d4-a716-446655440000",
    resourceId: "adding-tens-and-ones",
    rating: 5,
    displayName: null,
    reviewText: "Useful practice.",
    contentHash: "hash-one",
    duplicateDay: "2026-11-09",
    createdAt: "2026-11-09T15:00:00.000Z",
  };

  assert.equal(await store.insertPending(review), "created");
  assert.equal(await store.insertPending(review), "idempotent-replay");
  assert.equal((await store.publicReviews(review.resourceId, 0)).ratingCount, 0);

  assert.equal(await store.transition(review.id, "approve", "2026-11-09T16:00:00.000Z"), "approved");
  const visible = await store.publicReviews(review.resourceId, 0);
  assert.equal(visible.ratingCount, 1);
  assert.equal(visible.ratingAverage, 5);
  assert.equal(visible.reviews[0].display_name, "Anonymous");

  assert.equal(await store.transition(review.id, "hide", "2026-11-09T17:00:00.000Z"), "hidden");
  assert.equal((await store.publicReviews(review.resourceId, 0)).ratingCount, 0);
  assert.equal(await store.transition(review.id, "restore", "2026-11-09T18:00:00.000Z"), "approved");
  assert.deepEqual(
    database.prepare("SELECT action, moderator FROM moderation_events ORDER BY id").all().map((row) => ({...row})),
    [
      {action: "approve", moderator: "owner"},
      {action: "hide", moderator: "owner"},
      {action: "restore", moderator: "owner"},
    ],
  );

  await store.permanentlyDelete(review.id, "2026-11-09T19:00:00.000Z");
  assert.equal(database.prepare("SELECT COUNT(*) AS count FROM reviews").get().count, 0);
  assert.equal(database.prepare("SELECT action FROM moderation_events ORDER BY id DESC LIMIT 1").get().action, "delete");
  database.close();
});

test("D1 rejected-review cleanup preserves pending and hidden rows", async () => {
  const database = new DatabaseSync(":memory:");
  database.exec(await readFile(new URL("../migrations/0001_initial.sql", import.meta.url), "utf8"));
  for (const [id, status, moderatedAt] of [
    ["old", "rejected", "2026-01-01T00:00:00Z"],
    ["new", "rejected", "2026-11-01T00:00:00Z"],
    ["pending", "pending", null],
    ["hidden", "hidden", "2026-01-01T00:00:00Z"],
  ]) {
    database.prepare(
      "INSERT INTO reviews (id, resource_id, rating, status, content_hash, duplicate_day, created_at, updated_at, moderated_at) VALUES (?, 'resource', 5, ?, ?, '2026-01-01', '2026-01-01T00:00:00Z', '2026-01-01T00:00:00Z', ?)"
    ).run(id, status, `hash-${id}`, moderatedAt);
  }
  const store = new D1ReviewStore(new D1Adapter(database));
  assert.equal(await store.expireRejected("2026-08-11T00:00:00Z", "2026-11-09T15:00:00Z"), 1);
  assert.deepEqual(
    database.prepare("SELECT id FROM reviews ORDER BY id").all().map((row) => row.id),
    ["hidden", "new", "pending"],
  );
  assert.equal(database.prepare("SELECT action FROM moderation_events").get().action, "expire_rejected");
  database.close();
});
