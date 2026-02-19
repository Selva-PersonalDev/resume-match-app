import re
from spellchecker import SpellChecker
from text_utils import extract_keywords, split_sentences

spell = SpellChecker()

WEAK_PHRASES = [
    "responsible for",
    "worked on",
    "helped with",
    "involved in",
    "assisted with"
]

def calculate_match_score(resume_text: str, jd_text: str):
    resume_keywords = extract_keywords(resume_text)
    jd_keywords = extract_keywords(jd_text)

    if not jd_keywords:
        return 0, [], []

    matched = resume_keywords.intersection(jd_keywords)
    missing = jd_keywords - resume_keywords

    score = round((len(matched) / len(jd_keywords)) * 100)

    return score, list(matched)[:20], list(missing)[:20]

def find_spelling_issues(text: str):
    words = re.findall(r'\b[a-zA-Z]{4,}\b', text.lower())
    misspelled = spell.unknown(words)
    return list(misspelled)[:20]

def detect_weak_sentences(text: str):
    sentences = split_sentences(text)
    weak = []

    for sentence in sentences:
        for phrase in WEAK_PHRASES:
            if phrase in sentence.lower():
                weak.append(sentence)
                break

    return weak[:10]

def improvement_suggestions(resume_text: str):
    suggestions = []

    if not re.search(r"\d+%", resume_text):
        suggestions.append(
            "Consider adding measurable achievements (e.g., increased performance by 30%)."
        )

    if "summary" not in resume_text.lower():
        suggestions.append(
            "Add a professional summary section at the top of your resume."
        )

    return suggestions

def analyze_resume(resume_text: str, jd_text: str):
    score, matched, missing = calculate_match_score(resume_text, jd_text)
    spell_issues = find_spelling_issues(resume_text)
    weak_sentences = detect_weak_sentences(resume_text)
    suggestions = improvement_suggestions(resume_text)

    return {
        "match_score": score,
        "matched_keywords": matched,
        "missing_keywords": missing,
        "spell_issues": spell_issues,
        "weak_sentences": weak_sentences,
        "improvement_suggestions": suggestions
    }
