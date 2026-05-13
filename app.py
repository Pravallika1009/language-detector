from fastapi import FastAPI
from pydantic import BaseModel
import requests

app = FastAPI()

# =========================================
# REQUEST MODEL
# =========================================
class Track(BaseModel):
    title: str
    artist: str
    album: str = ""

# =========================================
# LANGUAGE KEYWORDS
# =========================================
LANGUAGE_KEYWORDS = {

    "Telugu": [
        "telugu",
        "tollywood",
        "telugu song",
        "telugu lyrics",
        "telugu movie"
    ],

    "Hindi": [
        "hindi",
        "bollywood",
        "hindi song",
        "hindi lyrics"
    ],

    "Tamil": [
        "tamil",
        "kollywood",
        "tamil song"
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

    "English": [
        "english",
        "english song"
    ],

    "Spanish": [
        "spanish",
        "latin"
    ],

    "French": [
        "french"
    ],

    "Japanese": [
        "japanese",
        "anime song"
    ],

    "Korean": [
        "korean",
        "k-pop"
    ]
}

# =========================================
# FETCH PAGE
# =========================================
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

# =========================================
# HOME
# =========================================
@app.get("/")
def home():

    return {
        "message": "AI Language Detector Running"
    }

# =========================================
# DETECT LANGUAGE
# =========================================
@app.post("/detect")
def detect(track: Track):

    title = track.title.lower()
    artist = track.artist.lower()
    album = track.album.lower()

    print("\n====================")
    print("TRACK")
    print("====================")
    print(title, artist, album)

    # =====================================
    # SEARCH URLS
    # =====================================
    urls = [

        f"https://genius.com/search?q={title}+{artist}",

        f"https://www.jiosaavn.com/search/{title}",

        f"https://gaana.com/search/{title}",

        f"https://open.spotify.com/search/{title}",

        f"https://music.apple.com/us/search?term={title}"
    ]

    combined_html = ""

    # =====================================
    # FETCH HTML
    # =====================================
    for url in urls:

        html = fetch_page(url)

        combined_html += html

    # =====================================
    # ADD TRACK CONTEXT
    # =====================================
    combined_html += f"""
    {title}
    {artist}
    {album}
    """

    # =====================================
    # SCORING
    # =====================================
    scores = {}

    for language, keywords in LANGUAGE_KEYWORDS.items():

        score = 0

        for keyword in keywords:

            occurrences = combined_html.count(keyword)

            # weighted scoring
            score += occurrences * 5

        # =================================
        # STRONG ALBUM MATCH BONUS
        # =================================
        if language.lower() in album:
            score += 100

        # =================================
        # STRONG TITLE MATCH BONUS
        # =================================
        if f"{language.lower()} song" in combined_html:
            score += 80

        # =================================
        # MOVIE INDUSTRY BONUS
        # =================================
        if language == "Telugu" and "tollywood" in combined_html:
            score += 60

        if language == "Hindi" and "bollywood" in combined_html:
            score += 60

        if language == "Tamil" and "kollywood" in combined_html:
            score += 60

        scores[language] = score

    print("\n====================")
    print("SCORES")
    print("====================")
    print(scores)

    # =====================================
    # DETECT LANGUAGE
    # =====================================
    detected_language = max(
        scores,
        key=scores.get
    )

    highest_score = scores[detected_language]

    total_score = sum(scores.values())

    # =====================================
    # CONFIDENCE
    # =====================================
    if total_score == 0:

        confidence = 0

    else:

        confidence = round(
            (highest_score / total_score) * 100,
            2
        )

    print("\n====================")
    print("FINAL")
    print("====================")
    print(detected_language)

    # =====================================
    # RETURN
    # =====================================
    return {

        "track": track.title,

        "artist": track.artist,

        "album": track.album,

        "language": detected_language,

        "confidence": confidence,

        "scores": scores
    }