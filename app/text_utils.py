import re
import nltk
from nltk.corpus import stopwords
from collections import Counter

try:
    stopwords.words("english")
except LookupError:
    nltk.download("stopwords")

STOP_WORDS = set(stopwords.words("english"))

COMMON_RESUME_WORDS = {
    "experience", "skills", "knowledge", "excellent",
    "understanding", "strong", "ability", "working",
    "good", "team", "work", "responsible", "using"
}

def clean_text(text: str) -> str:
    text = text.lower()
    text = re.sub(r"[^a-zA-Z0-9\s\-]", " ", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()

def extract_keywords(text: str):
    words = clean_text(text).split()
    words = [w for w in words if len(w) > 3]
    words = [w for w in words if w not in STOP_WORDS]
    words = [w for w in words if w not in COMMON_RESUME_WORDS]
    return set(words)

def split_sentences(text: str):
    sentences = re.split(r'(?<=[.!?]) +', text)
    return [s.strip() for s in sentences if len(s.strip()) > 10]

def word_frequency(text: str):
    words = clean_text(text).split()
    return Counter(words)
