const GAME_ANALYTICS_ENDPOINT = "https://lms-download-analytics.rukhsana1409.workers.dev/game-event";
const GAME_EVENTS = new Set(["view", "start", "complete"]);

const sendGameAnalytics = (gameId, eventType) => {
    if (!GAME_ANALYTICS_ENDPOINT || !GAME_EVENTS.has(eventType)) return;
    const body = JSON.stringify({version: 1, gameId, eventType});
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

document.addEventListener("DOMContentLoaded", () => {
    const gameId = document.body.dataset.gameId || "";
    const frame = document.getElementById("gameFrame");
    if (!/^[a-z0-9]+(?:-[a-z0-9]+)*$/.test(gameId) || !frame) return;
    sendGameAnalytics(gameId, "view");
    frame.addEventListener("load", () => {
        const gameDocument = frame.contentDocument;
        if (!gameDocument) return;
        let completionRecorded = false;
        const markStart = () => {
            completionRecorded = false;
            sendGameAnalytics(gameId, "start");
        };
        ["go", "again", "restart"].forEach((id) => gameDocument.getElementById(id)?.addEventListener("click", markStart));
        const done = gameDocument.getElementById("done");
        if (!done) return;
        new MutationObserver(() => {
            if (!done.hidden && !completionRecorded) {
                completionRecorded = true;
                sendGameAnalytics(gameId, "complete");
            }
        }).observe(done, {attributes: true, attributeFilter: ["hidden"]});
    });
});
