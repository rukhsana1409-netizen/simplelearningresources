"""Generate the Free Learning Games directory from its small catalog."""

from __future__ import annotations

import json
import hashlib
from html import escape
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CATALOG = ROOT / "catalog" / "games.json"
OUTPUT = ROOT / "games.html"
HOMEPAGE = ROOT / "index.html"
ANALYTICS_OUTPUT = ROOT / "game-analytics-catalog.json"
ANALYTICS_WORKER_OUTPUT = ROOT / "cloudflare" / "download-analytics" / "src" / "game-metadata.mjs"
HOME_START = "    <!-- GENERATED HOME GAMES START -->"
HOME_END = "    <!-- GENERATED HOME GAMES END -->"


def load_games() -> list[dict]:
    data = json.loads(CATALOG.read_text(encoding="utf-8"))
    if data.get("schemaVersion") != 2 or not isinstance(data.get("games"), list):
        raise ValueError("catalog/games.json must contain schemaVersion 2 and a games array")
    required = {"id", "title", "description", "ageRange", "skills", "playHref", "analytics"}
    string_fields = required - {"analytics"}
    seen: set[str] = set()
    for game in data["games"]:
        if set(game) != required or not all(isinstance(game[field], str) and game[field] for field in string_fields):
            raise ValueError("Every game must define the complete non-empty game contract")
        if game["id"] in seen:
            raise ValueError(f"Duplicate game id: {game['id']}")
        if game["playHref"] != f"/games/{game['id']}/":
            raise ValueError(f"Game {game['id']} must use its clean game URL")
        analytics = game["analytics"]
        if not {"difficulties", "categories"} <= set(analytics) <= {"difficulties", "categories", "tracksCompletion"}:
            raise ValueError(f"Game {game['id']} must define analytics difficulties and categories")
        if "tracksCompletion" in analytics and not isinstance(analytics["tracksCompletion"], bool):
            raise ValueError(f"Game {game['id']} analytics tracksCompletion must be a boolean")
        for field in ("difficulties", "categories"):
            values = analytics[field]
            if not isinstance(values, dict) or not values:
                raise ValueError(f"Game {game['id']} analytics {field} must be a non-empty object")
            if any(not isinstance(key, str) or not key or not isinstance(label, str) or not label for key, label in values.items()):
                raise ValueError(f"Game {game['id']} analytics {field} must contain non-empty strings")
        seen.add(game["id"])
    return data["games"]


def build_analytics_payload(games: list[dict]) -> dict:
    metadata = {}
    for game in games:
        entry = {
            "title": game["title"],
            "difficulties": game["analytics"]["difficulties"],
            "categories": game["analytics"]["categories"],
        }
        if "tracksCompletion" in game["analytics"]:
            entry["tracksCompletion"] = game["analytics"]["tracksCompletion"]
        metadata[game["id"]] = entry
    compact = json.dumps(metadata, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    return {
        "version": hashlib.sha256(compact.encode("utf-8")).hexdigest()[:16],
        "gameCount": len(metadata),
        "games": metadata,
    }


def write_analytics_metadata(games: list[dict]) -> None:
    payload = build_analytics_payload(games)
    ANALYTICS_OUTPUT.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")
    worker_metadata = json.dumps(payload["games"], ensure_ascii=False, indent=2)
    ANALYTICS_WORKER_OUTPUT.write_text(
        f"// Generated from catalog/games.json. Do not edit.\nexport const GAME_METADATA = Object.freeze({worker_metadata});\n",
        encoding="utf-8",
        newline="\n",
    )


def render(games: list[dict]) -> str:
    cards = "\n".join(
        f'''        <article class="card game-card">
            <p class="game-age">{escape(game["ageRange"])}</p>
            <h2>{escape(game["title"])}</h2>
            <p>{escape(game["description"])}</p>
            <p class="game-skills"><strong>Practice:</strong> {escape(game["skills"])}</p>
            <a href="{escape(game["playHref"], quote=True)}">Play Game</a>
        </article>'''
        for game in games
    )
    return f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="google-adsense-account" content="ca-pub-7543692368591799">
    <script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-7543692368591799" crossorigin="anonymous"></script>
    <link rel="icon" href="/favicon.ico">
    <link rel="icon" type="image/png" sizes="16x16" href="/favicon-16x16.png">
    <link rel="icon" type="image/png" sizes="32x32" href="/favicon-32x32.png">
    <link rel="icon" type="image/png" sizes="192x192" href="/site-icon-192x192.png">
    <link rel="apple-touch-icon" sizes="180x180" href="/apple-touch-icon.png">
    <link rel="canonical" href="https://simplelearningresources.com/games.html">
    <meta name="description" content="Play free, child-friendly learning games for Preschool and Kindergarten skills.">
    <link rel="stylesheet" href="style.css">
    <script src="nav.js" defer></script>
    <title>Free Learning Games | Learning Made Simple</title>
</head>
<body>
<nav class="main-nav">
    <div class="logo"><img class="logo-mark" src="/site-icon-source.png" alt="" width="34" height="34"><span>Learning Made Simple</span></div>
    <div class="nav-links"><a href="index.html">Home</a><a href="worksheets.html">Resources</a><a href="games.html">Free Learning Games</a><a href="preschool.html">By Grade</a><a href="about.html">About</a><a href="contact.html">Contact</a></div>
</nav>
<main class="library games-directory">
    <div class="library-header">
        <h1>Free Learning Games</h1>
        <p>Simple, playful practice for young learners. No sign-in required.</p>
    </div>
    <div class="card-container">
{cards}
    </div>
</main>
<footer><div class="footer-content"><div class="footer-brand"><h3>Learning Made Simple</h3><p>Simple resources. Meaningful learning.</p></div><div class="footer-links"><div><h4>Explore</h4><a href="index.html">Home</a><a href="worksheets.html">All Resources</a><a href="games.html">Free Learning Games</a><a href="about.html">About</a><a href="contact.html">Contact</a></div><div><h4>Information</h4><a href="privacy.html">Privacy Policy</a><a href="terms.html">Terms of Use</a><a href="disclaimer.html">Disclaimer</a></div></div></div><div class="footer-bottom"><p>&copy; 2026 Learning Made Simple. All rights reserved.</p></div></footer>
<!-- Cloudflare Web Analytics -->
<script type="module" src="https://static.cloudflareinsights.com/beacon.min.js" data-cf-beacon='{{"token":"a6fe9e891acb4cffadbe27263f7ec4bd"}}'></script>
<!-- End Cloudflare Web Analytics -->
</body>
</html>
'''


def render_home_cards(games: list[dict]) -> str:
    return "\n".join(
        f'''    <article class="home-game-card">
        <a class="home-game-preview" href="{escape(game["playHref"], quote=True)}" aria-label="Play {escape(game["title"], quote=True)}">
            <img src="/games/{escape(game["id"], quote=True)}/{escape(game["id"], quote=True)}-preview.png" alt="{escape(game["title"], quote=True)} game preview" width="900" height="600" loading="lazy">
        </a>
        <div class="home-game-copy">
            <p class="home-game-grade">{escape(game["ageRange"])}</p>
            <h3>{escape(game["title"])}</h3>
            <a class="home-game-play" href="{escape(game["playHref"], quote=True)}">Play Now</a>
        </div>
    </article>'''
        for game in games[:4]
    )


def update_homepage(games: list[dict]) -> None:
    source = HOMEPAGE.read_text(encoding="utf-8")
    if source.count(HOME_START) != 1 or source.count(HOME_END) != 1:
        raise ValueError("Homepage must contain exactly one generated games marker pair")
    before, remainder = source.split(HOME_START, 1)
    _, after = remainder.split(HOME_END, 1)
    generated = f"{HOME_START}\n{render_home_cards(games)}\n{HOME_END}"
    HOMEPAGE.write_text(f"{before}{generated}{after}", encoding="utf-8", newline="\n")


def generate() -> int:
    games = load_games()
    OUTPUT.write_text(render(games), encoding="utf-8", newline="\n")
    update_homepage(games)
    write_analytics_metadata(games)
    return len(games)


if __name__ == "__main__":
    print(f"GENERATED games={generate()} path={OUTPUT.relative_to(ROOT)}")
