import re
from datetime import datetime, timezone

from config.constants import BUSINESS, INTERNATIONAL, NATIONAL, SPORTS


CATEGORY_KEYWORDS = {
    SPORTS: {"sport", "sports", "cricket", "football", "ipl", "fifa", "nba", "tennis"},
    BUSINESS: {"business", "market", "markets", "economy", "finance", "startup", "stocks"},
    NATIONAL: {"india", "indian", "national", "domestic", "government", "policy"},
    INTERNATIONAL: {"world", "international", "global", "geopolitics", "foreign"},
}


def clean_text(text=""):
    return re.sub(r"\s+", " ", str(text or "")).strip()


def normalize_article(title="", summary="", source="", url="", category="", **extra):
    """
    Normalize article structure across all news providers.
    """
    article = {
        "title": clean_text(title),
        "summary": clean_text(summary),
        "source": clean_text(source),
        "url": clean_text(url),
        "category": clean_text(category),
        "collected_at": datetime.now(timezone.utc).isoformat(),
    }
    for key, value in extra.items():
        if value not in (None, "", [], {}):
            article[key] = value
    return article


def article_text(article):
    return clean_text(
        " ".join(
            [
                article.get("title", ""),
                article.get("summary", ""),
                article.get("source", ""),
                article.get("category", ""),
            ]
        )
    )


def dedupe_articles(articles):
    seen = set()
    unique_articles = []

    for article in articles:
        title = clean_text(article.get("title", "")).lower()
        url = clean_text(article.get("url", "")).lower()
        key = (title, url)

        if key in seen:
            continue

        seen.add(key)
        unique_articles.append(article)

    return unique_articles


def detect_categories(query):
    cleaned_query = clean_text(query).lower()
    selections = {}

    for category, keywords in CATEGORY_KEYWORDS.items():
        selections[category] = any(keyword in cleaned_query for keyword in keywords)

    if any(selections.values()):
        return selections

    return {category: True for category in CATEGORY_KEYWORDS}


def requested_categories(categories):
    if not categories:
        return list(CATEGORY_KEYWORDS)

    selected = [category for category, enabled in categories.items() if enabled]
    return selected or list(CATEGORY_KEYWORDS)


def format_category_label(category):
    return category.replace("_", " ").title()


def format_plan(categories):
    labels = [format_category_label(category) for category in requested_categories(categories)]
    return "Requested categories: " + ", ".join(labels)


def keyword_overlap_score(text, query):
    query_words = {word for word in re.findall(r"[a-z0-9]+", clean_text(query).lower()) if len(word) > 2}
    if not query_words:
        return 0.0

    text_words = set(re.findall(r"[a-z0-9]+", clean_text(text).lower()))
    overlap = query_words.intersection(text_words)
    return float(len(overlap))


def rank_articles(articles, query="", top_n=5):
    ranked_articles = []

    for article in articles:
        score = keyword_overlap_score(article_text(article), query)
        if article.get("summary"):
            score += 0.5
        if article.get("url"):
            score += 0.25
        if article.get("source"):
            score += 0.25

        ranked_article = dict(article)
        ranked_article["score"] = round(score, 2)
        ranked_articles.append(ranked_article)

    ranked_articles.sort(
        key=lambda article: (
            -article.get("score", 0.0),
            article.get("title", "").lower(),
        )
    )
    return ranked_articles[:top_n]


def build_bullets(text, fallback_title="", count=3):
    cleaned = clean_text(text)
    sentences = [sentence.strip(" -") for sentence in re.split(r"(?<=[.!?])\s+", cleaned) if sentence.strip()]

    bullets = sentences[:count]
    if not bullets and fallback_title:
        bullets = [clean_text(fallback_title)]

    while bullets and len(bullets) < count:
        bullets.append(bullets[-1])

    return bullets[:count]
