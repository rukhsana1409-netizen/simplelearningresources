const STATUSES = ["pending", "approved", "rejected", "hidden"];

function escapeAttribute(value) {
  return value.replaceAll("&", "&amp;").replaceAll('"', "&quot;").replaceAll("<", "&lt;").replaceAll(">", "&gt;");
}

export function renderAdminDashboard(nonce) {
  const safeNonce = escapeAttribute(nonce);
  return `<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="robots" content="noindex,nofollow,noarchive">
  <title>Review Management | Learning Made Simple</title>
  <style nonce="${safeNonce}">
    :root { color-scheme: light; --navy:#17324d; --teal:#178d91; --teal-dark:#0f6d70; --yellow:#f6c84b; --cream:#fffaf0; --line:#dce7e9; --muted:#62727b; --danger:#b42318; --shadow:0 10px 28px rgba(23,50,77,.1); }
    * { box-sizing:border-box; }
    body { margin:0; background:linear-gradient(180deg,#eaf8f7 0,#fff 280px); color:var(--navy); font:16px/1.5 system-ui,-apple-system,"Segoe UI",sans-serif; }
    button { font:inherit; }
    .shell { width:min(1120px,calc(100% - 32px)); margin:0 auto; padding:32px 0 64px; }
    header { display:flex; align-items:flex-start; justify-content:space-between; gap:24px; margin-bottom:26px; }
    .eyebrow { margin:0 0 5px; color:var(--teal-dark); font-size:.78rem; font-weight:800; letter-spacing:.1em; text-transform:uppercase; }
    h1 { margin:0; font-size:clamp(1.75rem,4vw,2.5rem); line-height:1.15; }
    header p:last-child { margin:8px 0 0; color:var(--muted); }
    .brand { flex:0 0 auto; border-radius:999px; background:var(--yellow); padding:8px 14px; font-size:.85rem; font-weight:800; }
    .tabs { display:grid; grid-template-columns:repeat(4,minmax(0,1fr)); gap:8px; margin-bottom:18px; }
    .tab { min-height:52px; border:1px solid var(--line); border-radius:13px; background:#fff; color:var(--navy); cursor:pointer; font-weight:750; box-shadow:0 3px 12px rgba(23,50,77,.05); }
    .tab:hover { border-color:var(--teal); }
    .tab[aria-selected="true"] { border-color:var(--teal); background:var(--teal); color:#fff; }
    .tab:focus-visible,.action:focus-visible { outline:3px solid var(--yellow); outline-offset:2px; }
    .count { display:inline-grid; min-width:25px; min-height:25px; margin-left:5px; place-items:center; border-radius:999px; background:rgba(23,50,77,.09); font-size:.8rem; }
    .tab[aria-selected="true"] .count { background:rgba(255,255,255,.2); }
    .notice { min-height:26px; margin:0 0 12px; font-weight:700; }
    .notice[data-kind="error"] { color:var(--danger); }
    .notice[data-kind="success"] { color:var(--teal-dark); }
    .state { padding:38px 20px; border:1px solid var(--line); border-radius:18px; background:#fff; text-align:center; color:var(--muted); box-shadow:var(--shadow); }
    .reviews { display:grid; gap:16px; }
    .review { border:1px solid var(--line); border-radius:18px; background:#fff; padding:20px; box-shadow:var(--shadow); }
    .review-head { display:flex; align-items:flex-start; justify-content:space-between; gap:16px; }
    .review h2 { margin:0; font-size:1.12rem; line-height:1.35; }
    .meta { display:flex; flex-wrap:wrap; gap:7px 14px; margin:7px 0 0; color:var(--muted); font-size:.88rem; }
    .stars { color:#d28a00; font-size:1.15rem; letter-spacing:.08em; white-space:nowrap; }
    .comment { margin:17px 0; padding:14px 16px; border-radius:12px; background:var(--cream); overflow-wrap:anywhere; white-space:pre-wrap; }
    .comment.empty { color:var(--muted); font-style:italic; }
    .badge { display:inline-block; border-radius:999px; background:#eaf8f7; color:var(--teal-dark); padding:3px 9px; font-size:.75rem; font-weight:800; text-transform:capitalize; }
    .actions { display:flex; flex-wrap:wrap; gap:8px; }
    .action { border:1px solid var(--teal); border-radius:10px; background:#fff; color:var(--teal-dark); cursor:pointer; padding:8px 13px; font-weight:750; }
    .action:hover { background:#eaf8f7; }
    .action.primary { background:var(--teal); color:#fff; }
    .action.danger { border-color:#e3a7a3; color:var(--danger); }
    .action:disabled { cursor:wait; opacity:.55; }
    .load-more { display:block; margin:18px auto 0; }
    .load-more[hidden] { display: none; }
    @media (max-width:700px) { .shell{width:min(100% - 22px,1120px);padding-top:22px} header{display:block}.brand{display:inline-block;margin-top:14px}.tabs{grid-template-columns:repeat(2,1fr)}.review-head{display:block}.stars{display:block;margin-top:8px}.review{padding:16px} }
    @media (max-width:360px) { .tabs{grid-template-columns:1fr}.actions{display:grid}.action{width:100%} }
  </style>
</head>
<body>
  <main class="shell">
    <header>
      <div><p class="eyebrow">Private dashboard</p><h1>Review Management</h1><p>Approve and manage worksheet ratings and comments.</p></div>
      <span class="brand">Learning Made Simple</span>
    </header>
    <div class="tabs" role="tablist" aria-label="Review status">
      ${STATUSES.map((status, index) => `<button class="tab" id="tab-${status}" type="button" role="tab" aria-selected="${index === 0}" aria-controls="reviews-panel" tabindex="${index === 0 ? 0 : -1}" data-status="${status}">${status[0].toUpperCase() + status.slice(1)} <span class="count" data-count="${status}">0</span></button>`).join("")}
    </div>
    <p class="notice" role="status" aria-live="polite"></p>
    <section id="reviews-panel" role="tabpanel" aria-labelledby="tab-pending" tabindex="0">
      <div class="state" data-state>Loading reviews...</div>
      <div class="reviews" data-reviews hidden></div>
      <button class="action load-more" type="button" data-load-more hidden>Load more reviews</button>
    </section>
  </main>
  <script nonce="${safeNonce}">
    (() => {
      "use strict";
      const tabs = [...document.querySelectorAll('[role="tab"]')];
      const panel = document.querySelector('#reviews-panel');
      const stateBox = document.querySelector('[data-state]');
      const list = document.querySelector('[data-reviews]');
      const notice = document.querySelector('.notice');
      const loadMore = document.querySelector('[data-load-more]');
      let activeStatus = 'pending';
      let nextOffset = null;

      function setNotice(message = '', kind = '') {
        notice.textContent = message;
        notice.dataset.kind = kind;
      }

      function setState(message) {
        stateBox.textContent = message;
        stateBox.hidden = false;
        list.hidden = true;
        loadMore.hidden = true;
      }

      function updateCounts(counts) {
        for (const status of ${JSON.stringify(STATUSES)}) {
          const value = Number(counts[status]);
          document.querySelector('[data-count="' + status + '"]').textContent = Number.isFinite(value) ? String(value) : '0';
        }
      }

      function actionButton(label, action, reviewId, kind = '') {
        const button = document.createElement('button');
        button.type = 'button';
        button.className = 'action ' + kind;
        button.textContent = label;
        button.dataset.action = action;
        button.dataset.reviewId = reviewId;
        button.setAttribute('aria-label', label + ' review');
        return button;
      }

      function renderReview(review) {
        const article = document.createElement('article');
        article.className = 'review';
        article.dataset.reviewId = review.id;
        const head = document.createElement('div');
        head.className = 'review-head';
        const titleArea = document.createElement('div');
        const title = document.createElement('h2');
        title.textContent = review.resource_title;
        const meta = document.createElement('p');
        meta.className = 'meta';
        const name = document.createElement('span');
        name.textContent = review.display_name || 'Anonymous';
        const date = document.createElement('time');
        date.dateTime = review.created_at;
        date.textContent = new Intl.DateTimeFormat(undefined, {dateStyle:'medium',timeStyle:'short'}).format(new Date(review.created_at));
        const badge = document.createElement('span');
        badge.className = 'badge';
        badge.textContent = review.status;
        meta.append(name, date, badge);
        titleArea.append(title, meta);
        const stars = document.createElement('span');
        stars.className = 'stars';
        stars.setAttribute('aria-label', review.rating + ' out of 5 stars');
        stars.textContent = '★'.repeat(review.rating) + '☆'.repeat(5 - review.rating);
        head.append(titleArea, stars);
        const comment = document.createElement('p');
        comment.className = 'comment' + (review.review_text ? '' : ' empty');
        comment.textContent = review.review_text || 'Rating only. No written review.';
        const actions = document.createElement('div');
        actions.className = 'actions';
        if (review.status === 'pending') actions.append(actionButton('Approve', 'approve', review.id, 'primary'), actionButton('Reject', 'reject', review.id));
        if (review.status === 'approved') actions.append(actionButton('Hide', 'hide', review.id));
        if (review.status === 'rejected') actions.append(actionButton('Approve', 'approve', review.id, 'primary'));
        if (review.status === 'hidden') actions.append(actionButton('Restore', 'restore', review.id, 'primary'));
        actions.append(actionButton('Permanently delete', 'delete', review.id, 'danger'));
        article.append(head, comment, actions);
        return article;
      }

      async function api(path, options = {}) {
        const response = await fetch(path, {credentials:'same-origin',headers:{accept:'application/json',...(options.headers || {})},...options});
        const type = response.headers.get('content-type') || '';
        if (response.redirected || !type.includes('application/json')) throw new Error('Your secure session may have expired. Refresh and sign in again.');
        const body = response.status === 204 ? null : await response.json();
        if (!response.ok) throw new Error(body?.error || 'The review request failed.');
        return body;
      }

      async function load(status, successMessage = '', append = false, offset = 0) {
        activeStatus = status;
        setNotice(successMessage, successMessage ? 'success' : '');
        loadMore.hidden = true;
        if (!append) setState('Loading ' + status + ' reviews...');
        else setNotice('Loading more reviews...');
        try {
          const data = await api('/admin/api/reviews?status=' + encodeURIComponent(status) + '&offset=' + offset);
          updateCounts(data.counts);
          const cards = data.reviews.map(renderReview);
          if (append) list.append(...cards);
          else list.replaceChildren(...cards);
          nextOffset = Number.isInteger(data.nextOffset) && data.nextOffset >= 0 ? data.nextOffset : null;
          loadMore.hidden = nextOffset === null;
          if (!append && !data.reviews.length) setState('No ' + status + ' reviews.');
          else { stateBox.hidden = true; list.hidden = false; if (append) setNotice(); }
        } catch (error) {
          setState('Reviews could not be loaded.');
          setNotice(error.message, 'error');
        }
      }

      async function moderate(button) {
        const action = button.dataset.action;
        const reviewId = button.dataset.reviewId;
        if (action === 'delete' && !window.confirm('Permanently delete this review? This cannot be undone in the dashboard.')) return;
        document.querySelectorAll('.action').forEach((item) => { item.disabled = true; });
        setNotice(action === 'delete' ? 'Deleting review...' : 'Updating review...');
        try {
          const path = '/admin/api/reviews/' + encodeURIComponent(reviewId) + (action === 'delete' ? '' : '/' + action);
          await api(path, action === 'delete'
            ? {method:'DELETE',headers:{'content-type':'application/json'},body:JSON.stringify({confirm:'PERMANENTLY DELETE'})}
            : {method:'POST'});
          await load(activeStatus, action === 'delete' ? 'Review permanently deleted.' : 'Review updated.');
        } catch (error) {
          setNotice(error.message, 'error');
          document.querySelectorAll('.action').forEach((item) => { item.disabled = false; });
        }
      }

      function selectTab(tab, focus = false) {
        for (const item of tabs) {
          const selected = item === tab;
          item.setAttribute('aria-selected', String(selected));
          item.tabIndex = selected ? 0 : -1;
        }
        panel.setAttribute('aria-labelledby', tab.id);
        if (focus) tab.focus();
        load(tab.dataset.status);
      }

      tabs.forEach((tab, index) => {
        tab.addEventListener('click', () => selectTab(tab));
        tab.addEventListener('keydown', (event) => {
          let target = null;
          if (event.key === 'ArrowRight') target = tabs[(index + 1) % tabs.length];
          if (event.key === 'ArrowLeft') target = tabs[(index - 1 + tabs.length) % tabs.length];
          if (event.key === 'Home') target = tabs[0];
          if (event.key === 'End') target = tabs[tabs.length - 1];
          if (target) { event.preventDefault(); selectTab(target, true); }
        });
      });
      list.addEventListener('click', (event) => {
        const button = event.target.closest('[data-action]');
        if (button) moderate(button);
      });
      loadMore.addEventListener('click', () => {
        if (nextOffset !== null) load(activeStatus, '', true, nextOffset);
      });
      load('pending');
    })();
  </script>
</body>
</html>`;
}
