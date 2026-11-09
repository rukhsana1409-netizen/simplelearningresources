import assert from "node:assert/strict";
import {test} from "node:test";
import {renderAdminDashboard} from "../src/admin-dashboard.mjs";

test("dashboard renders accessible tabs, states, moderation actions, and mobile rules", () => {
  const html = renderAdminDashboard("test-nonce");
  assert.match(html, /<style nonce="test-nonce">/);
  assert.match(html, /<script nonce="test-nonce">/);
  assert.equal((html.match(/data-status="(pending|approved|rejected|hidden)"/g) || []).length, 4);
  assert.match(html, /aria-live="polite"/);
  assert.match(html, /Loading reviews/);
  assert.match(html, /No ' \+ status \+ ' reviews/);
  assert.match(html, /Reviews could not be loaded/);
  assert.match(html, /Review updated/);
  assert.match(html, /ArrowRight/);
  assert.match(html, /ArrowLeft/);
  assert.match(html, /@media \(max-width:700px\)/);
  assert.match(html, /window\.confirm\('Permanently delete this review/);
  assert.match(html, /Load more reviews/);
  assert.match(html, /\.load-more\[hidden\] \{ display: none; \}/);
  assert.match(html, /nextOffset/);
  assert.match(html, /function setState\(message\)[\s\S]*?loadMore\.hidden = true;/);
  assert.match(html, /Number\.isInteger\(data\.nextOffset\) && data\.nextOffset >= 0/);
});

test("dashboard uses text nodes for review content and authenticated same-origin APIs", () => {
  const html = renderAdminDashboard("safe");
  assert.match(html, /title\.textContent = review\.resource_title/);
  assert.match(html, /comment\.textContent = review\.review_text/);
  assert.match(html, /credentials:'same-origin'/);
  assert.match(html, /\/admin\/api\/reviews/);
  assert.doesNotMatch(html, /innerHTML/);
  assert.doesNotMatch(html, /mock review/i);
});
