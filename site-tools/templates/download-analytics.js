const DOWNLOAD_ANALYTICS_ENDPOINT = "https://lms-download-analytics.rukhsana1409.workers.dev/download";

const downloadAnalyticsResourceId = () => {
    const cleanResourceMatch = window.location.pathname.match(/^\/resources\/([a-z0-9]+(?:-[a-z0-9]+)*)\/?$/);
    if (cleanResourceMatch) return cleanResourceMatch[1];
    if (window.location.pathname.endsWith("/resource-preview.html") || window.location.pathname === "/resource-preview.html") {
        return new URLSearchParams(window.location.search).get("resource") || "";
    }
    return "";
};

const downloadAnalyticsEvent = (link) => {
    const resourceId = downloadAnalyticsResourceId();
    if (!resourceId) return null;
    const url = new URL(link.href, window.location.href);
    if (!url.pathname.toLowerCase().endsWith(".pdf")) return null;
    if (![window.location.origin, "https://assets.simplelearningresources.com"].includes(url.origin)) return null;
    const pageMatch = url.pathname.match(/\/page-(\d{2})\.pdf$/i);
    if (!pageMatch) {
        const resource = window.worksheetResourcesById?.[resourceId];
        if (
            (resource && url.pathname === new URL(resource.pdfUrl, window.location.href).pathname)
            || link.matches(".resource-primary-action, #download-complete")
        ) {
            return {version: 1, resourceId, downloadType: "pack", pageNumber: null};
        }
        return {version: 1, resourceId, downloadType: "supporting", pageNumber: null};
    }
    return {version: 1, resourceId, downloadType: "page", pageNumber: Number(pageMatch[1])};
};

const sendDownloadAnalytics = (analyticsEvent) => {
    if (!DOWNLOAD_ANALYTICS_ENDPOINT) return;
    const body = JSON.stringify(analyticsEvent);
    try {
        if (navigator.sendBeacon?.(DOWNLOAD_ANALYTICS_ENDPOINT, new Blob([body], {type: "text/plain;charset=UTF-8"}))) return;
        fetch(DOWNLOAD_ANALYTICS_ENDPOINT, {
            method: "POST",
            body,
            headers: {"Content-Type": "text/plain;charset=UTF-8"},
            keepalive: true,
            mode: "cors",
            credentials: "omit"
        }).catch(() => {});
    } catch (_) {
        // Download analytics is best-effort and must never interrupt the download.
    }
};

document.addEventListener("click", (event) => {
    const link = event.target.closest?.("a");
    if (!link) return;
    const analyticsEvent = downloadAnalyticsEvent(link);
    if (analyticsEvent) sendDownloadAnalytics(analyticsEvent);
});
