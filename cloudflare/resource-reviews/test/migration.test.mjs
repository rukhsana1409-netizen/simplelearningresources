import assert from "node:assert/strict";
import {readFile} from "node:fs/promises";
import {DatabaseSync} from "node:sqlite";
import {test} from "node:test";

const migrationUrl = new URL("../migrations/0001_initial.sql", import.meta.url);

test("initial migration constrains review states, lengths, ratings, and duplicate submissions", async () => {
  const sql = await readFile(migrationUrl, "utf8");
  assert.match(sql, /rating BETWEEN 1 AND 5/);
  assert.match(sql, /length\(display_name\) BETWEEN 1 AND 50/);
  assert.match(sql, /length\(review_text\) BETWEEN 1 AND 500/);
  assert.match(sql, /pending.*approved.*rejected.*hidden/);
  assert.match(sql, /UNIQUE \(resource_id, content_hash, duplicate_day\)/);
  assert.match(sql, /reviews_public_idx/);
  assert.match(sql, /moderation_events/);
  const database = new DatabaseSync(":memory:");
  assert.doesNotThrow(() => database.exec(sql));
  const tables = database.prepare("SELECT name FROM sqlite_master WHERE type = 'table' ORDER BY name").all();
  assert.deepEqual(tables.map((row) => row.name).filter((name) => !name.startsWith("sqlite_")), ["moderation_events", "reviews"]);
  database.close();
});
