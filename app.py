from fastapi import FastAPI
from pydantic import BaseModel
import requests

app = FastAPI()

class Track(BaseModel):
    title: str
    artist: str
    album: str = ""

LANGUAGE_KEYWORDS = {
    "Telugu": ["telugu", "tollywood"],
    "Hindi": ["hindi", "bollywood"],
    "Tamil": ["tamil", "kollywood"],
    "Malayalam": ["malayalam"],
    "Kannada": ["kannada"],
    "Punjabi": ["punjabi"],
    "English": ["english"]
}

@app.get("/")
def home():
    return {"message": "Running"}

@app.post("/detect")
def detect(track: Track):

    query = f"{track.title} {track.artist} {track.album} song language"

    url = f"https://www.google.com/search?q={query}"

    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    html = requests.get(url, headers=headers).text.lower()

    scores = {}

    for lang, words in LANGUAGE_KEYWORDS.items():

        score = 0

        for word in words:
            score += html.count(word)

        scores[lang] = score

    detected = max(scores, key=scores.get)

    return {
        "language": detected,
        "scores": scores
    }