import re
from collections import Counter
from spellchecker import SpellChecker
from text_utils import extract_keywords, split_sentences, word_frequency

spell = SpellChecker()

TECH_WEIGHT = 0.5
TOOLS_WEIGHT = 0.2
EXPERIENCE_WEIGHT = 0.15
SOFT_WEIGHT = 0.05
METRIC_WEIGHT = 0.1

TECH_SKILLS = {
    "python","java","docker","kubernetes","terraform","aws",
    "azure","gcp","devops","mlops","aiops","fastapi",
    "react","node","sql","bigquery","xgboost","grafana"
}

SOFT_SKILLS = {
    "communication","leadership","collaboration",
    "problem-solving","teamwork","analytical"
}

TOOLS = {
    "github","gitlab","jenkins","servicenow","linux",
    "bash","powershell"
}

def is_technical_word(word):
    return (
        any(char.isdigit() for char in word)
        or any(char.isupper() for char in word[1:])
        or word.isupper()
        or "-" in word
        or "/" in word
        or len(word) > 15
    )

def weighted_score(resume_text, jd_text):
    resume_words = extract_keywords(resume_text)
    jd_words = extract_keywords(jd_text)

    tech_match = len((resume_words & jd_words) & TECH_SKILLS)
    tool_match = len((resume_words & jd_words) & TOOLS)
    soft_match = len((resume_words & jd_words) & SOFT_SKILLS)

    tech_total = len(jd_words & TECH_SKILLS) or 1
    tool_total = len(jd_words & TOOLS) or 1
    soft_total = len(jd_words & SOFT_SKILLS) or 1

    tech_score = (tech_match / tech_total) * TECH_WEIGHT
    tool_score = (tool_match / tool_total) * TOOLS_WEIGHT
    soft_score = (soft_match / soft_total) * SOFT_WEIGHT

    experience_score = EXPERIENCE_WEIGHT if re.search(r"\b(years|experience)\b", resume_text.lower()) else 0
    metric_score = METRIC_WEIGHT if re.search(r"\d+%", resume_text) else 0

    total_score = (tech_score + tool_score + soft_score + experience_score + metric_score) * 100

    return round(min(total_score, 100))

def highlight_keywords(text, matched_keywords):
    highlighted = text
    for word in matched_keywords:
        pattern = re.compile(rf"\b({re.escape(word)})\b", re.IGNORECASE)
        highlighted = pattern.sub(
            r'<span class="bg-green-200 text-green-900 font-semibold px-1 rounded">\1</span>',
            highlighted
        )
    return highlighted

def find_spelling_issues(text):
    words = re.findall(r'\b[a-zA-Z]{4,}\b', text)
    word_counts = word_frequency(text)

    filtered_words = [
        w for w in words
        if word_counts[w.lower()] == 1
        and not is_technical_word(w)
    ]

    misspelled = spell.unknown(filtered_words)
    return list(misspelled)[:8]

def detect_weak_sentences(text):
    sentences = split_sentences(text)
    weak = []

    for sentence in sentences:
        if len(sentence.split()) > 30:
            weak.append("Long sentence detected: " + sentence)
            continue

        if re.search(r"\b(was|were|been|being)\b", sentence.lower()):
            weak.append("Possible passive voice: " + sentence)
            continue

        if re.search(r"\b(responsible for|worked on|involved in)\b", sentence.lower()):
            weak.append("Weak phrasing: " + sentence)

    return weak[:5]

def improvement_suggestions(resume_text, weak_sentences):
    suggestions = []

    if not re.search(r"\d+%", resume_text):
        suggestions.append("Add measurable achievements (e.g., increased performance by 30%).")

    if not weak_sentences:
        suggestions.append("Strengthen impact using strong action verbs.")

    if "summary" not in resume_text.lower():
        suggestions.append("Consider adding a professional summary section.")

    return suggestions

def analyze_resume(resume_text, jd_text):

    resume_keywords = extract_keywords(resume_text)
    jd_keywords = extract_keywords(jd_text)

    matched = list(resume_keywords & jd_keywords)
    missing = list(jd_keywords - resume_keywords)

    score = weighted_score(resume_text, jd_text)

    spell_issues = find_spelling_issues(resume_text)
    weak_sentences = detect_weak_sentences(resume_text)
    suggestions = improvement_suggestions(resume_text, weak_sentences)

    highlighted_resume = highlight_keywords(resume_text, matched)

    return {
        "match_score": score,
        "matched_keywords": matched[:20],
        "missing_keywords": missing[:15],
        "spell_issues": spell_issues,
        "weak_sentences": weak_sentences,
        "improvement_suggestions": suggestions,
        "highlighted_resume": highlighted_resume
    }
