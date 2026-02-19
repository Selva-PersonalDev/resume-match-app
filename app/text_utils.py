import re
import nltk
from nltk.corpus import stopwords

# Download stopwords once
try:
    stopwords.words("english")
except LookupError:
    nltk.download("stopwords")

STOP_WORDS = set(stopwords.words("english"))

def clean_text(text: str) -> str:
    text = text.lower()
    text = re.sub(r"[^a-zA-Z0-9\s]", " ", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()

def extract_keywords(text: str) -> set:
    words = clean_text(text).split()
    keywords = {w for w in words if w not in STOP_WORDS and len(w) > 3}
    return keywords

def split_sentences(text: str):
    sentences = re.split(r'(?<=[.!?]) +', text)
    return [s.strip() for s in sentences if len(s.strip()) > 10]
