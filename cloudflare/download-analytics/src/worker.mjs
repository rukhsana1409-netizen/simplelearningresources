const ALLOWED_ORIGIN = "https://simplelearningresources.com";
const MAX_BODY_BYTES = 1024;
const RESOURCE_ID = /^[a-z0-9]+(?:-[a-z0-9]+)*$/;

import {renderDashboard, queryDashboardData} from "./dashboard.mjs";

const corsHeaders = (origin) => ({
  "Access-Control-Allow-Origin": origin,
  "Access-Control-Allow-Methods": "POST, OPTIONS",
  "Access-Control-Allow-Headers": "Content-Type",
  "Access-Control-Max-Age": "86400",
  "Vary": "Origin",
});

const response = (status, message, origin = null) => new Response(message, {
  status,
  headers: {
    "Content-Type": "text/plain; charset=utf-8",
    "Cache-Control": "no-store",
    ...(origin ? corsHeaders(origin) : {}),
  },
});

const parseEvent = (value) => {
  if (!value || typeof value !== "object" || Array.isArray(value)) throw new Error("invalid payload");
  const allowedKeys = new Set(["version", "resourceId", "downloadType", "pageNumber"]);
  if (Object.keys(value).some((key) => !allowedKeys.has(key))) throw new Error("unexpected field");
  if (value.version !== 1) throw new Error("invalid version");
  if (typeof value.resourceId !== "string" || value.resourceId.length > 96 || !RESOURCE_ID.test(value.resourceId)) {
    throw new Error("invalid resourceId");
  }
  if (value.downloadType === "pack") {
    if (value.pageNumber !== null && value.pageNumber !== undefined) throw new Error("pack pageNumber must be null");
    return {resourceId: value.resourceId, downloadType: "pack", pageNumber: 0};
  }
  if (value.downloadType === "supporting") {
    if (value.pageNumber !== null && value.pageNumber !== undefined) throw new Error("supporting pageNumber must be null");
    return {resourceId: value.resourceId, downloadType: "supporting", pageNumber: 0};
  }
  if (value.downloadType === "page" && Number.isInteger(value.pageNumber) && value.pageNumber >= 1 && value.pageNumber <= 100) {
    return {resourceId: value.resourceId, downloadType: "page", pageNumber: value.pageNumber};
  }
  throw new Error("invalid download event");
};

export default {
  async fetch(request, env) {
    const url = new URL(request.url);
    if (url.pathname === "/health" && request.method === "GET") return response(200, "ok\n");
    if (url.pathname === "/dashboard" || url.pathname.startsWith("/dashboard/")) {
      if (env.DASHBOARD_ENABLED !== "true") return response(404, "not found\n");
      if (request.method !== "GET") return response(405, "method not allowed\n");
      if (url.pathname === "/dashboard" || url.pathname === "/dashboard/") {
        try {
          return renderDashboard(await queryDashboardData(
            env.ANALYTICS_SQL,
            url.searchParams.get("range"),
          ));
        } catch (error) {
          console.error("dashboard analytics query failed", error?.message || "unknown error");
          return renderDashboard(null, "Analytics are temporarily unavailable. Please try again.");
        }
      }
      if (url.pathname === "/dashboard/data") {
        try {
          return Response.json(await queryDashboardData(
            env.ANALYTICS_SQL,
            url.searchParams.get("range"),
          ), {
            headers: dashboardHeaders("application/json; charset=utf-8"),
          });
        } catch (error) {
          console.error("dashboard analytics query failed", error?.message || "unknown error");
          return Response.json({error: "Analytics are temporarily unavailable."}, {
            status: 503,
            headers: dashboardHeaders("application/json; charset=utf-8"),
          });
        }
      }
      return response(404, "not found\n");
    }
    if (url.pathname !== "/download") return response(404, "not found\n");

    const origin = request.headers.get("Origin");
    if (origin !== ALLOWED_ORIGIN) return response(403, "forbidden\n");
    if (request.method === "OPTIONS") return new Response(null, {status: 204, headers: corsHeaders(origin)});
    if (request.method !== "POST") return response(405, "method not allowed\n", origin);

    const declaredLength = Number(request.headers.get("Content-Length") || 0);
    if (declaredLength > MAX_BODY_BYTES) return response(413, "payload too large\n", origin);
    const contentType = request.headers.get("Content-Type") || "";
    if (!contentType.startsWith("text/plain") && !contentType.startsWith("application/json")) {
      return response(415, "unsupported media type\n", origin);
    }

    const body = await request.text();
    if (new TextEncoder().encode(body).byteLength > MAX_BODY_BYTES) return response(413, "payload too large\n", origin);

    let analyticsEvent;
    try {
      analyticsEvent = parseEvent(JSON.parse(body));
    } catch (_) {
      return response(400, "invalid event\n", origin);
    }

    env.DOWNLOAD_ANALYTICS.writeDataPoint({
      indexes: [analyticsEvent.resourceId],
      blobs: [analyticsEvent.downloadType],
      doubles: [analyticsEvent.pageNumber],
    });
    return new Response(null, {status: 204, headers: {...corsHeaders(origin), "Cache-Control": "no-store"}});
  },
};

function dashboardHeaders(contentType) {
  return {
    "Content-Type": contentType,
    "Cache-Control": "no-store",
    "Content-Security-Policy": "default-src 'none'; script-src 'self'; style-src 'self'; connect-src 'self'; img-src 'none'; base-uri 'none'; form-action 'none'; frame-ancestors 'none'",
    "Referrer-Policy": "no-referrer",
    "X-Content-Type-Options": "nosniff",
    "X-Frame-Options": "DENY",
    "X-Robots-Tag": "noindex, nofollow, noarchive",
  };
}
