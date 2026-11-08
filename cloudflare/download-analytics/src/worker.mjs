const ALLOWED_ORIGIN = "https://simplelearningresources.com";
const MAX_BODY_BYTES = 1024;
const RESOURCE_ID = /^[a-z0-9]+(?:-[a-z0-9]+)*$/;
const GAME_EVENT_TYPES = new Set(["view", "start", "complete"]);

import {DEFAULT_CATALOG_METADATA_FALLBACK_URL, DEFAULT_CATALOG_METADATA_URL, loadCatalogMetadata, renderDashboard, queryDashboardData} from "./dashboard.mjs";
import {DEFAULT_GAME_METADATA_FALLBACK_URL, DEFAULT_GAME_METADATA_URL, gameDashboardHeaders, loadGameMetadata, queryGameDashboardData, renderGameDashboard} from "./game-dashboard.mjs";

export const catalogMetadataUrls = (env) => {
  if (env.CATALOG_METADATA_URL === null) return [];
  return [
    env.CATALOG_METADATA_URL === undefined ? DEFAULT_CATALOG_METADATA_URL : env.CATALOG_METADATA_URL,
    env.CATALOG_METADATA_FALLBACK_URL === undefined
      ? DEFAULT_CATALOG_METADATA_FALLBACK_URL
      : env.CATALOG_METADATA_FALLBACK_URL,
  ].filter(Boolean);
};

export const gameMetadataUrls = (env) => {
  if (env.GAME_METADATA_URL === null) return [];
  return [
    env.GAME_METADATA_URL === undefined ? DEFAULT_GAME_METADATA_URL : env.GAME_METADATA_URL,
    env.GAME_METADATA_FALLBACK_URL === undefined
      ? DEFAULT_GAME_METADATA_FALLBACK_URL
      : env.GAME_METADATA_FALLBACK_URL,
  ].filter(Boolean);
};

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

const parseGameEvent = (value) => {
  if (!value || typeof value !== "object" || Array.isArray(value)) throw new Error("invalid payload");
  if (typeof value.gameId !== "string" || value.gameId.length > 96 || !RESOURCE_ID.test(value.gameId)) {
    throw new Error("invalid gameId");
  }
  if (value.version === 1) {
    const allowedKeys = new Set(["version", "gameId", "eventType"]);
    if (Object.keys(value).some(key => !allowedKeys.has(key)) || !GAME_EVENT_TYPES.has(value.eventType)) {
      throw new Error("invalid legacy game event");
    }
    return {gameId: value.gameId, points: [{blobs: [`game-${value.eventType}`], doubles: [0]}]};
  }
  if (value.version !== 2 || typeof value.difficulty !== "string" || value.difficulty.length > 48 || !RESOURCE_ID.test(value.difficulty)) {
    throw new Error("invalid detailed game event");
  }
  if (value.eventType === "start") {
    const allowedKeys = new Set(["version", "gameId", "eventType", "difficulty", "replay"]);
    if (Object.keys(value).some(key => !allowedKeys.has(key)) || typeof value.replay !== "boolean") {
      throw new Error("invalid game start");
    }
    return {gameId: value.gameId, points: [{blobs: ["game-start-v2", value.difficulty], doubles: [value.replay ? 1 : 0, 0]}]};
  }
  if (value.eventType === "complete") {
    const allowedKeys = new Set(["version", "gameId", "eventType", "difficulty", "questionsAnswered", "firstTryCorrect", "mistakeCategories"]);
    const categories = value.mistakeCategories;
    if (
      Object.keys(value).some(key => !allowedKeys.has(key))
      || !Number.isInteger(value.questionsAnswered) || value.questionsAnswered < 1 || value.questionsAnswered > 100
      || !Number.isInteger(value.firstTryCorrect) || value.firstTryCorrect < 0 || value.firstTryCorrect > value.questionsAnswered
      || !categories || typeof categories !== "object" || Array.isArray(categories)
      || Object.keys(categories).length > 10
      || Object.entries(categories).some(([category, count]) => !RESOURCE_ID.test(category) || !Number.isInteger(count) || count < 0 || count > 100)
    ) {
      throw new Error("invalid game completion");
    }
    return {
      gameId: value.gameId,
      points: [
        {blobs: ["game-complete-v2", value.difficulty], doubles: [value.questionsAnswered, value.firstTryCorrect]},
        ...Object.entries(categories)
          .filter(([, count]) => count > 0)
          .map(([category, count]) => ({blobs: ["game-mistakes", value.difficulty, category], doubles: [count, 0]})),
      ],
    };
  }
  throw new Error("invalid detailed game event");
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
          const catalog = await loadCatalogMetadata(catalogMetadataUrls(env));
          return renderDashboard(await queryDashboardData(
            env.ANALYTICS_SQL,
            url.searchParams.get("range"),
            new Date(),
            catalog,
          ));
        } catch (error) {
          console.error("dashboard analytics query failed", error?.message || "unknown error");
          return renderDashboard(null, "Analytics are temporarily unavailable. Please try again.");
        }
      }
      if (url.pathname === "/dashboard/data") {
        try {
          const catalog = await loadCatalogMetadata(catalogMetadataUrls(env));
          return Response.json(await queryDashboardData(
            env.ANALYTICS_SQL,
            url.searchParams.get("range"),
            new Date(),
            catalog,
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
    if (url.pathname === "/game-dashboard" || url.pathname.startsWith("/game-dashboard/")) {
      if (env.GAME_DASHBOARD_ENABLED !== "true") return response(404, "not found\n");
      if (request.method !== "GET") return response(405, "method not allowed\n");
      const isDocument = url.pathname === "/game-dashboard" || url.pathname === "/game-dashboard/";
      const isData = url.pathname === "/game-dashboard/data";
      if (!isDocument && !isData) return response(404, "not found\n");
      try {
        const catalog = await loadGameMetadata(gameMetadataUrls(env));
        const data = await queryGameDashboardData(env.ANALYTICS_SQL, url.searchParams.get("range"), new Date(), catalog);
        if (isDocument) return renderGameDashboard(data);
        if (isData) {
          return Response.json(data, {headers: gameDashboardHeaders("application/json; charset=utf-8")});
        }
      } catch (error) {
        console.error("game dashboard analytics query failed", error?.message || "unknown error");
        if (isData) {
          return Response.json({error: "Game analytics are temporarily unavailable."}, {
            status: 503,
            headers: gameDashboardHeaders("application/json; charset=utf-8"),
          });
        }
        return renderGameDashboard(null, "Game analytics are temporarily unavailable. Please try again.");
      }
    }
    if (url.pathname !== "/download" && url.pathname !== "/game-event") return response(404, "not found\n");

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

    try {
      const value = JSON.parse(body);
      if (url.pathname === "/game-event") {
        const gameEvent = parseGameEvent(value);
        gameEvent.points.forEach(point => env.DOWNLOAD_ANALYTICS.writeDataPoint({
          indexes: [`game--${gameEvent.gameId}`],
          ...point,
        }));
      } else {
        const analyticsEvent = parseEvent(value);
        env.DOWNLOAD_ANALYTICS.writeDataPoint({
          indexes: [analyticsEvent.resourceId],
          blobs: [analyticsEvent.downloadType],
          doubles: [analyticsEvent.pageNumber],
        });
      }
    } catch (_) {
      return response(400, "invalid event\n", origin);
    }
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
