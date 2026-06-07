from tools.rss import get_all_feeds
from config.constants import BUSINESS, INTERNATIONAL, NATIONAL, SPORTS
from config.settings import MAX_ARTICLES
from tools.utils import dedupe_articles, normalize_article, rank_articles


CATEGORY_QUERIES = {
    SPORTS: "latest sports news in India",
    BUSINESS: "latest business and market news in India",
    NATIONAL: "latest India national news",
    INTERNATIONAL: "latest international and world news",
}


def collect_rss_news():
    """
    Collect RSS articles.
    """
    rss_news = get_all_feeds()
    articles = []
    for item in rss_news:
        articles.append(normalize_article(title=item.get("title"),summary=item.get("summary"),source="rss",url=item.get("link")))
    return articles


def collect_news(query: str):
    """
    Collect news from all sources (currently only RSS as per WebBaseLoader only policy).
    """
    rss_news = collect_rss_news()
    return {
        "rss": rss_news,
        "total_articles": len(rss_news)
    }


def collect_category_news(category: str, user_query: str = "", limit: int = MAX_ARTICLES):
    """
    Collect and rank news for a specific category.
    """
    base_query = CATEGORY_QUERIES.get(category, "latest news")
    search_query = f"{base_query} {user_query}".strip()
    collected = collect_news(search_query)
    articles = []

    for source_name in ("rss",):
        for article in collected.get(source_name, []):
            normalized = normalize_article(
                title=article.get("title", ""),
                summary=article.get("summary", ""),
                source=article.get("source", source_name),
                url=article.get("url", ""),
                category=category,
            )
            articles.append(normalized)

    return rank_articles(dedupe_articles(articles), search_query, top_n=limit)
