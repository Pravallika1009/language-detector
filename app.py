from fastapi import FastAPI
from pydantic import BaseModel
import requests

app = FastAPI()

# ============================
# REQUEST MODEL
# ============================
class Track(BaseModel):
    title: str
    artist: str
    album: str = ""

# ============================
# SIMPLE MUSIC METADATA MAP (SAFE FALLBACK)
# ============================
ARTIST_LANGUAGE_HINTS = {
    "armaan malik": ["Hindi", "English"],
    "shreya ghoshal": ["Hindi"],
    "arijit singh": ["Hindi"],
    "justin bieber": ["English"],
    "ed sheeran": ["English"],
    "bad bunny": ["Spanish"],
    "bts": ["Korean", "English"],
    "blackpink": ["Korean", "English"],
    "hanumankind": ["Malayalam", "English"]
}

# ============================
# FETCH (GENIUS PAGE ONLY)
# ============================
def fetch(url):
    try:
        return requests.get(
            url,
            headers={"User-Agent": "Mozilla/5.0"},
            timeout=10
        ).text.lower()
    except:
        return ""

# ============================
# CORE DETECTION LOGIC
# ============================
@app.post("/detect")
def detect(track: Track):

    title = track.title.lower().strip()
    artist = track.artist.lower().strip()
    album = track.album.lower().strip()

    # ---------------------------------
    # STEP 1: GET GENIUS PAGE (METADATA ONLY)
    # ---------------------------------
    url = f"https://genius.com/search?q={title} {artist}"
    html = fetch(url)

    # ---------------------------------
    # STEP 2: DETECT LANGUAGE FROM ARTIST PROFILE
    # ---------------------------------
    languages = []

    if artist in ARTIST_LANGUAGE_HINTS:
        languages.extend(ARTIST_LANGUAGE_HINTS[artist])

    # ---------------------------------
    # STEP 3: ALBUM / CONTEXT CHECK
    # ---------------------------------
    if "bollywood" in album:
        languages.append("Hindi")

    if "tollywood" in album:
        languages.append("Telugu")

    if "kollywood" in album:
        languages.append("Tamil")

    # ---------------------------------
    # STEP 4: FALLBACK LOGIC
    # ---------------------------------
    if not languages:

        # If no known metadata → default assumption
        # Most global songs default to English unless known otherwise
        languages = ["English"]

    # ---------------------------------
    # STEP 5: HANDLE MIXED LANGUAGE CLEANLY
    # ---------------------------------
    languages = list(set(languages))

    # If English + other language exists → keep both
    # (this is what you requested)

    # ---------------------------------
    # STEP 6: CONFIDENCE (RULE-BASED)
    # ---------------------------------
    confidence = 70

    if len(languages) == 1:
        confidence = 90

    if "English" in languages and len(languages) > 1:
        confidence = 80

    # ---------------------------------
    # FINAL RESPONSE
    # ---------------------------------
    return {
        "track": track.title,
        "artist": track.artist,
        "album": track.album,
        "languages": languages,
        "confidence": confidence,
        "method": "metadata + artist inference (no text analysis)"
    }