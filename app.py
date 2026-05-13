from fastapi import FastAPI
from pydantic import BaseModel
import requests

app = FastAPI()

class Track(BaseModel):
    title: str
    artist: str
    album: str = ""

def fetch(url):
    try:
        return requests.get(
            url,
            headers={"User-Agent": "Mozilla/5.0"},
            timeout=10
        ).text.lower()
    except:
        return ""

@app.post("/detect")
def detect(track: Track):

    title = track.title
    artist = track.artist

    # =========================
    # DATA SOURCES
    # =========================
    genius_url = f"https://genius.com/search?q={title} {artist}"
    spotify_url = f"https://open.spotify.com/search/{title}"

    genius_html = fetch(genius_url)
    spotify_html = fetch(spotify_url)

    combined = genius_html + spotify_html

    # =========================
    # STRONG SIGNAL RULES
    # =========================
    languages = []

    if "spanish" in combined or "español" in combined:
        languages.append("Spanish")

    if "k-pop" in combined:
        languages.append("Korean")

    if "j-pop" in combined:
        languages.append("Japanese")

    if "bollywood" in combined:
        languages.append("Hindi")

    if "tollywood" in combined:
        languages.append("Telugu")

    if "kollywood" in combined:
        languages.append("Tamil")

    # =========================
    # DEFAULT FALLBACK
    # =========================
    if not languages:
        languages = ["Unknown"]

    # =========================
    # CONFIDENCE (simple heuristic)
    # =========================
    confidence = 70 if languages != ["Unknown"] else 0

    return {
        "track": title,
        "artist": artist,
        "languages": languages,
        "confidence": confidence,
        "source": "metadata-based inference"
    }