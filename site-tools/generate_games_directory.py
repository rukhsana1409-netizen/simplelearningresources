"""Generate the Free Learning Games directory from its small catalog."""

from __future__ import annotations

import json
from html import escape
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CATALOG = ROOT / "catalog" / "games.json"
OUTPUT = ROOT / "games.html"


def load_games() -> list[dict]:
    data = json.loads(CATALOG.read_text(encoding="utf-8"))
    if data.get("schemaVersion") != 1 or not isinstance(data.get("games"), list):
        raise ValueError("catalog/games.json must contain schemaVersion 1 and a games array")
    required = {"id", "title", "description", "ageRange", "skills", "playHref"}
    seen: set[str] = set()
    for game in data["games"]:
        if set(game) != required or not all(isinstance(game[field], str) and game[field] for field in required):
            raise ValueError("Every game must define the complete non-empty game contract")
        if game["id"] in seen:
            raise ValueError(f"Duplicate game id: {game['id']}")
        if game["playHref"] != f"/games/{game['id']}/":
            raise ValueError(f"Game {game['id']} must use its clean game URL")
        seen.add(game["id"])
    return data["games"]


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


def generate() -> int:
    games = load_games()
    OUTPUT.write_text(render(games), encoding="utf-8", newline="\n")
    return len(games)


if __name__ == "__main__":
    print(f"GENERATED games={generate()} path={OUTPUT.relative_to(ROOT)}")
