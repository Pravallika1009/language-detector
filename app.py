from fastapi import FastAPI
from pydantic import BaseModel
import requests

app = FastAPI()

# =====================================
# REQUEST MODEL
# =====================================
class Track(BaseModel):
    title: str
    artist: str
    album: str = ""

# =====================================
# GLOBAL LANGUAGE KEYWORDS
# =====================================
LANGUAGE_KEYWORDS = {

    "English": [
        "english"
    ],

    "Hindi": [
        "hindi",
        "bollywood"
    ],

    "Telugu": [
        "telugu",
        "tollywood"
    ],

    "Tamil": [
        "tamil",
        "kollywood"
    ],

    "Malayalam": [
        "malayalam"
    ],

    "Kannada": [
        "kannada"
    ],

    "Punjabi": [
        "punjabi"
    ],

    "Spanish": [
        "spanish",
        "español",
        "latin"
    ],

    "French": [
        "french"
    ],

    "Japanese": [
        "japanese",
        "anime"
    ],

    "Korean": [
        "korean",
        "k-pop"
    ]
}

# =====================================
# HOME ROUTE
# =====================================
@app.get("/")
def home():

    return {
        "message": "Language Detector Running"
    }

# =====================================
# SEARCH HELPER
# =====================================
def fetch_page(url):

    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    try:

        response = requests.get(
            url,
            headers=headers,
            timeout=10
        )

        return response.text.lower()

    except:

        return ""

# =====================================
# DETECT ROUTE
# =====================================
@app.post("/detect")
def detect(track: Track):

    title = track.title
    artist = track.artist
    album = track.album

    print("\n====================")
    print("TRACK INFO")
    print("====================")
    print(title)
    print(artist)
    print(album)

    # =================================
    # SEARCH URLs
    # =================================
    search_urls = [

        f"https://genius.com/search?q={title}%20{artist}",

        f"https://www.jiosaavn.com/search/{title}",

        f"https://gaana.com/search/{title}",

        f"https://music.apple.com/us/search?term={title}",

        f"https://open.spotify.com/search/{title}"
    ]

    combined_html = ""

    # =================================
    # FETCH ALL PAGES
    # =================================
    for url in search_urls:

        print("\nFetching:", url)

        html = fetch_page(url)

        combined_html += html

    # =================================
    # DEBUG
    # =================================
    print("\n====================")
    print("HTML LENGTH")
    print("====================")
    print(len(combined_html))

    # =================================
    # LANGUAGE SCORING
    # =================================
    scores = {}

    for language, keywords in LANGUAGE_KEYWORDS.items():

        score = 0

        for keyword in keywords:

            occurrences = combined_html.count(keyword)

            score += occurrences

        scores[language] = score

    print("\n====================")
    print("SCORES")
    print("====================")
    print(scores)

    # =================================
    # DETECT LANGUAGE
    # =================================
    max_score = max(scores.values())

    if max_score == 0:

        detected_language = "Unknown"

    else:

        detected_language = max(
            scores,
            key=scores.get
        )

    # =================================
    # CONFIDENCE
    # =================================
    total = sum(scores.values())

    if total == 0:

        confidence = 0

    else:

        confidence = round(
            (max_score / total) * 100,
            2
        )

    print("\n====================")
    print("FINAL RESULT")
    print("====================")
    print(detected_language)

    # =================================
    # RETURN
    # =================================
    return {

        "track": title,

        "artist": artist,

        "album": album,

        "language": detected_language,

        "confidence": confidence,

        "scores": scores
    }