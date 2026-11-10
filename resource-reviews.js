(() => {
    "use strict";

    const components = [...document.querySelectorAll(".resource-reviews[data-review-resource-id]")];
    if (!components.length) return;

    let turnstileLoader;

    function loadTurnstile() {
        if (window.turnstile) return Promise.resolve(window.turnstile);
        if (turnstileLoader) return turnstileLoader;
        turnstileLoader = new Promise((resolve, reject) => {
            const script = document.createElement("script");
            script.src = "https://challenges.cloudflare.com/turnstile/v0/api.js?render=explicit";
            script.async = true;
            script.defer = true;
            script.addEventListener("load", () => resolve(window.turnstile), {once:true});
            script.addEventListener("error", () => reject(new Error("Spam protection could not be loaded.")), {once:true});
            document.head.append(script);
        });
        return turnstileLoader;
    }

    function stars(rating) {
        return "★".repeat(rating) + "☆".repeat(5 - rating);
    }

    function reviewCard(review) {
        const card = document.createElement("article");
        card.className = "review-card";
        const header = document.createElement("div");
        header.className = "review-card-header";
        const identity = document.createElement("div");
        const name = document.createElement("p");
        name.className = "review-card-name";
        name.textContent = review.display_name || "Anonymous";
        const date = document.createElement("time");
        date.className = "review-card-date";
        date.dateTime = review.created_at;
        date.textContent = new Intl.DateTimeFormat(undefined, {dateStyle:"medium"}).format(new Date(review.created_at));
        identity.append(name, date);
        const rating = document.createElement("span");
        rating.className = "review-card-stars";
        rating.setAttribute("aria-label", review.rating + " out of 5 stars");
        rating.textContent = stars(review.rating);
        header.append(identity, rating);
        card.append(header);
        if (review.review_text) {
            const comment = document.createElement("p");
            comment.className = "review-card-comment";
            comment.textContent = review.review_text;
            card.append(comment);
        }
        return card;
    }

    function renderApproved(component, data) {
        const summary = component.querySelector("[data-review-summary]");
        const list = component.querySelector("[data-review-list]");
        summary.replaceChildren();
        list.replaceChildren();
        if (!Number.isInteger(data.ratingCount) || data.ratingCount <= 0 || typeof data.ratingAverage !== "number") {
            summary.hidden = true;
            list.hidden = true;
            return;
        }
        const starDisplay = document.createElement("span");
        starDisplay.className = "review-average-stars";
        const rounded = Math.round(data.ratingAverage);
        starDisplay.textContent = stars(rounded);
        starDisplay.setAttribute("aria-label", data.ratingAverage.toFixed(1) + " out of 5 stars");
        const average = document.createElement("strong");
        average.className = "review-average-value";
        average.textContent = data.ratingAverage.toFixed(1);
        const count = document.createElement("span");
        count.className = "review-count";
        count.textContent = data.ratingCount + (data.ratingCount === 1 ? " approved rating" : " approved ratings");
        summary.append(starDisplay, average, count);
        summary.hidden = false;
        const approved = Array.isArray(data.reviews) ? data.reviews.slice(0, 10) : [];
        list.append(...approved.map(reviewCard));
        list.hidden = approved.length === 0;
    }

    async function loadApproved(component) {
        const endpoint = component.dataset.reviewApiOrigin;
        const resourceId = component.dataset.reviewResourceId;
        try {
            const response = await fetch(endpoint + "/v1/resources/" + encodeURIComponent(resourceId) + "/reviews", {
                headers:{accept:"application/json"},
            });
            if (!response.ok) throw new Error("Ratings could not be loaded.");
            renderApproved(component, await response.json());
        } catch {
            // The form remains usable. Reviews never affect previews or downloads.
            component.querySelector("[data-review-summary]").hidden = true;
            component.querySelector("[data-review-list]").hidden = true;
        }
    }

    function setupForm(component) {
        const form = component.querySelector("[data-review-form]");
        const textarea = form.elements.review;
        const counter = component.querySelector("[data-review-character-count]");
        const status = component.querySelector("[data-review-form-status]");
        const submit = form.querySelector(".review-submit");
        const turnstileTarget = component.querySelector("[data-review-turnstile]");
        let widgetId = null;
        let token = "";
        let submissionId = crypto.randomUUID();

        const setStatus = (message, kind = "") => {
            status.textContent = message;
            status.dataset.kind = kind;
        };
        const resetTurnstile = () => {
            token = "";
            if (widgetId !== null && window.turnstile) window.turnstile.reset(widgetId);
        };
        const ensureTurnstile = async () => {
            if (widgetId !== null) return;
            try {
                const turnstile = await loadTurnstile();
                widgetId = turnstile.render(turnstileTarget, {
                    sitekey: component.dataset.turnstileSitekey,
                    action: "submit-resource-review",
                    theme: "light",
                    size: "flexible",
                    callback: (value) => { token = value; setStatus(); },
                    "expired-callback": () => { token = ""; setStatus("Verification expired. Please try again.", "error"); },
                    "error-callback": () => { token = ""; setStatus("Verification could not be completed.", "error"); },
                });
            } catch (error) {
                setStatus(error.message, "error");
            }
        };

        textarea.addEventListener("input", () => {
            counter.textContent = Array.from(textarea.value).length + " / 500";
        });
        form.addEventListener("focusin", ensureTurnstile, {once:true});
        form.addEventListener("submit", async (event) => {
            event.preventDefault();
            const rating = form.elements.rating.value;
            const name = form.elements.name.value.trim();
            const review = textarea.value.trim();
            if (!rating) { setStatus("Choose a star rating before submitting.", "error"); return; }
            if (Array.from(name).length > 50 || Array.from(review).length > 500) {
                setStatus("Check the name and comment length before submitting.", "error"); return;
            }
            if (!token) { await ensureTurnstile(); setStatus("Complete the verification before submitting.", "error"); return; }
            submit.disabled = true;
            setStatus("Submitting your rating...");
            try {
                const response = await fetch(component.dataset.reviewApiOrigin + "/v1/resources/" + encodeURIComponent(component.dataset.reviewResourceId) + "/reviews", {
                    method:"POST",
                    headers:{"content-type":"application/json"},
                    body:JSON.stringify({submissionId,rating:Number(rating),name,review,turnstileToken:token,website:""}),
                });
                const body = await response.json().catch(() => ({}));
                if (!response.ok) throw new Error(body.error || "Your rating could not be submitted.");
                form.reset();
                counter.textContent = "0 / 500";
                submissionId = crypto.randomUUID();
                setStatus("Thank you. Your rating was submitted for approval.", "success");
            } catch (error) {
                setStatus(error.message, "error");
            } finally {
                resetTurnstile();
                submit.disabled = false;
            }
        });
    }

    const observer = "IntersectionObserver" in window ? new IntersectionObserver((entries) => {
        for (const entry of entries) {
            if (!entry.isIntersecting) continue;
            observer.unobserve(entry.target);
            loadApproved(entry.target);
            setupForm(entry.target);
        }
    }, {rootMargin:"300px"}) : null;

    for (const component of components) {
        if (observer) observer.observe(component);
        else { loadApproved(component); setupForm(component); }
    }
})();
