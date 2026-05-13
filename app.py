from fastapi import FastAPI
from pydantic import BaseModel
import requests

app = FastAPI()

# ==========================================
# REQUEST MODEL
# ==========================================
class Track(BaseModel):
    title: str
    artist: str
    album: str = ""

# ==========================================
# GLOBAL LANGUAGE KEYWORDS
# ==========================================
LANGUAGE_KEYWORDS = {

    "English": [
        "english",
        "english song",
        "english lyrics"
    ],

    "Spanish": [
        "spanish",
        "español",
        "latin pop",
        "reggaeton"
    ],

    "French": [
        "french",
        "français",
        "french song"
    ],

    "German": [
        "german",
        "deutsch"
    ],

    "Italian": [
        "italian",
        "italiano"
    ],

    "Portuguese": [
        "portuguese",
        "português",
        "brazilian music"
    ],

    "Russian": [
        "russian",
        "русский"
    ],

    "Japanese": [
        "japanese",
        "j-pop",
        "anime song"
    ],

    "Korean": [
        "korean",
        "k-pop"
    ],

    "Chinese": [
        "chinese",
        "mandarin",
        "c-pop"
    ],

    "Arabic": [
        "arabic",
        "arab music"
    ],

    "Turkish": [
        "turkish",
        "türkçe"
    ],

    "Indonesian": [
        "indonesian",
        "bahasa indonesia"
    ],

    "Thai": [
        "thai",
        "thai song"
    ],

    "Vietnamese": [
        "vietnamese"
    ],

    "Punjabi": [
        "punjabi"
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

    "Bengali": [
        "bengali"
    ],

    "Marathi": [
        "marathi"
    ],

    "Gujarati": [
        "gujarati"
    ],

    "Urdu": [
        "urdu"
    ],

    "Nepali": [
        "nepali"
    ],

    "Sinhala": [
        "sinhala"
    ],

    "African": [
        "afrobeats",
        "nigerian music",
        "african song"
    ]
}

# ==========================================
# HOME ROUTE
# ==========================================
@app.get("/")
def home():

    return {
        "message": "Global Language Detector API Running"
    }

# ==========================================
# DETECT LANGUAGE ROUTE
# ==========================================
@app.post("/detect")
def detect(track: Track):

    # --------------------------------------
    # CREATE SEARCH QUERY
    # --------------------------------------
    query = f"""
    {track.title}
    {track.artist}
    {track.album}
    song language
    """

    print("\n==========================")
    print("SEARCH QUERY")
    print("==========================")
    print(query)

    # --------------------------------------
    # DUCKDUCKGO SEARCH
    # --------------------------------------
    url = f"https://html.duckduckgo.com/html/?q={query}"

    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    try:

        response = requests.get(
            url,
            headers=headers,
            timeout=10
        )

        html = response.text.lower()

        print("\n==========================")
        print("HTML PREVIEW")
        print("==========================")
        print(html[:1500])

        # --------------------------------------
        # LANGUAGE SCORING
        # --------------------------------------
        scores = {}

        for language, keywords in LANGUAGE_KEYWORDS.items():

            score = 0

            for keyword in keywords:

                occurrences = html.count(keyword)

                score += occurrences

            scores[language] = score

        print("\n==========================")
        print("LANGUAGE SCORES")
        print("==========================")
        print(scores)

        # --------------------------------------
        # FIND BEST MATCH
        # --------------------------------------
        max_score = max(scores.values())

        if max_score == 0:

            detected_language = "Unknown"

        else:

            detected_language = max(
                scores,
                key=scores.get
            )

        # --------------------------------------
        # CONFIDENCE CALCULATION
        # --------------------------------------
        total_score = sum(scores.values())

        if total_score == 0:

            confidence = 0

        else:

            confidence = round(
                (max_score / total_score) * 100,
                2
            )

        print("\n==========================")
        print("FINAL RESULT")
        print("==========================")
        print("Language:", detected_language)
        print("Confidence:", confidence)

        # --------------------------------------
        # RETURN RESPONSE
        # --------------------------------------
        return {

            "track": track.title,

            "artist": track.artist,

            "album": track.album,

            "language": detected_language,

            "confidence": confidence,

            "scores": scores
        }

    except Exception as e:

        print("\n==========================")
        print("ERROR")
        print("==========================")
        print(str(e))

        return {

            "language": "Error",

            "message": str(e)
        }