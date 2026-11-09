PRAGMA foreign_keys = ON;

CREATE TABLE reviews (
  id TEXT PRIMARY KEY,
  resource_id TEXT NOT NULL,
  rating INTEGER NOT NULL CHECK (rating BETWEEN 1 AND 5),
  display_name TEXT CHECK (display_name IS NULL OR length(display_name) BETWEEN 1 AND 50),
  review_text TEXT CHECK (review_text IS NULL OR length(review_text) BETWEEN 1 AND 500),
  status TEXT NOT NULL DEFAULT 'pending' CHECK (status IN ('pending', 'approved', 'rejected', 'hidden')),
  content_hash TEXT NOT NULL,
  duplicate_day TEXT NOT NULL,
  created_at TEXT NOT NULL,
  updated_at TEXT NOT NULL,
  moderated_at TEXT,
  UNIQUE (resource_id, content_hash, duplicate_day)
);

CREATE INDEX reviews_public_idx
  ON reviews (resource_id, status, created_at DESC);

CREATE INDEX reviews_moderation_idx
  ON reviews (status, created_at DESC);

CREATE TABLE moderation_events (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  review_id TEXT NOT NULL,
  action TEXT NOT NULL CHECK (action IN ('approve', 'reject', 'hide', 'restore', 'delete', 'expire_rejected')),
  previous_status TEXT,
  resulting_status TEXT,
  moderator TEXT NOT NULL CHECK (moderator = 'owner'),
  created_at TEXT NOT NULL
);

CREATE INDEX moderation_events_review_idx
  ON moderation_events (review_id, created_at DESC);
