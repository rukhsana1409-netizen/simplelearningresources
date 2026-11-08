const GAME_ANALYTICS_ENDPOINT = "https://lms-download-analytics.rukhsana1409.workers.dev/game-event";
const GAME_EVENTS = new Set(["view", "start", "complete"]);
const GAME_ANALYTICS_MESSAGE_SOURCE = "lms-game-analytics";
const SLUG = /^[a-z0-9]+(?:-[a-z0-9]+)*$/;

const sendGameAnalyticsPayload = (payload) => {
    if (!GAME_ANALYTICS_ENDPOINT) return;
    const body = JSON.stringify(payload);
    try {
        if (navigator.sendBeacon?.(GAME_ANALYTICS_ENDPOINT, new Blob([body], {type: "text/plain;charset=UTF-8"}))) return;
        fetch(GAME_ANALYTICS_ENDPOINT, {
            method: "POST",
            body,
            headers: {"Content-Type": "text/plain;charset=UTF-8"},
            keepalive: true,
            mode: "cors",
            credentials: "omit"
        }).catch(() => {});
    } catch (_) {
        // Analytics is best-effort and must never interrupt the game.
    }
};

const sendLegacyGameAnalytics = (gameId, eventType) => {
    if (GAME_EVENTS.has(eventType)) sendGameAnalyticsPayload({version: 1, gameId, eventType});
};

const validMistakeCategories = (value) => (
    value && typeof value === "object" && !Array.isArray(value)
    && Object.keys(value).length <= 10
    && Object.entries(value).every(([category, count]) => SLUG.test(category) && Number.isInteger(count) && count >= 0 && count <= 100)
);

const detailedGamePayload = (gameId, message) => {
    if (!message || message.source !== GAME_ANALYTICS_MESSAGE_SOURCE || message.version !== 1) return null;
    if (message.eventType === "ready") return {ready: true};
    if (!SLUG.test(message.difficulty || "")) return null;
    if (message.eventType === "start" && typeof message.replay === "boolean") {
        return {version: 2, gameId, eventType: "start", difficulty: message.difficulty, replay: message.replay};
    }
    if (
        message.eventType === "complete"
        && Number.isInteger(message.questionsAnswered) && message.questionsAnswered >= 1 && message.questionsAnswered <= 100
        && Number.isInteger(message.firstTryCorrect) && message.firstTryCorrect >= 0 && message.firstTryCorrect <= message.questionsAnswered
        && validMistakeCategories(message.mistakeCategories)
    ) {
        return {
            version: 2,
            gameId,
            eventType: "complete",
            difficulty: message.difficulty,
            questionsAnswered: message.questionsAnswered,
            firstTryCorrect: message.firstTryCorrect,
            mistakeCategories: message.mistakeCategories
        };
    }
    return null;
};

document.addEventListener("DOMContentLoaded", () => {
    const gameId = document.body.dataset.gameId || "";
    const frame = document.getElementById("gameFrame");
    if (!SLUG.test(gameId) || !frame) return;
    sendLegacyGameAnalytics(gameId, "view");
    let completionRecorded = false;
    let bridgeReady = false;
    let bridgeCompletionRecorded = false;
    let trackedDocument = null;
    window.addEventListener("message", (event) => {
        if (event.source !== frame.contentWindow || event.origin !== window.location.origin) return;
        const payload = detailedGamePayload(gameId, event.data);
        if (!payload) return;
        if (payload.ready) {
            bridgeReady = true;
            return;
        }
        if (!bridgeReady) return;
        if (payload.eventType === "start") bridgeCompletionRecorded = false;
        if (payload.eventType === "complete") {
            if (bridgeCompletionRecorded) return;
            bridgeCompletionRecorded = true;
        }
        sendGameAnalyticsPayload(payload);
    });
    const setupFrameTracking = () => {
        const gameDocument = frame.contentDocument;
        if (!gameDocument || gameDocument === trackedDocument) return;
        trackedDocument = gameDocument;
        completionRecorded = false;
        bridgeReady = false;
        bridgeCompletionRecorded = false;
        const markStart = () => {
            completionRecorded = false;
            if (!bridgeReady) sendLegacyGameAnalytics(gameId, "start");
        };
        ["go", "again", "restart"].forEach((id) => gameDocument.getElementById(id)?.addEventListener("click", markStart));
        gameDocument.querySelectorAll("[data-lv]").forEach((button) => button.addEventListener("click", markStart));
        frame.contentWindow.postMessage({source: "lms-game-analytics-parent", version: 1, eventType: "initialize"}, window.location.origin);
        const done = gameDocument.getElementById("done");
        if (!done) return;
        new MutationObserver(() => {
            if (!done.hidden && !completionRecorded) {
                completionRecorded = true;
                if (!bridgeReady) sendLegacyGameAnalytics(gameId, "complete");
            }
        }).observe(done, {attributes: true, attributeFilter: ["hidden"]});
    };
    frame.addEventListener("load", setupFrameTracking);
    if (frame.contentDocument?.readyState === "complete") setupFrameTracking();
});
