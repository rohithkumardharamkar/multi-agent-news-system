import feedparser
RSS_FEEDS = {
    "reuters": "https://feeds.reuters.com/reuters/topNews",
    "bbc": "http://feeds.bbci.co.uk/news/rss.xml",
    "espn": "https://www.espn.com/espn/rss/news",
    "thehindu": "https://www.thehindu.com/news/feeder/default.rss"
}

def fetch_feed(feed_url: str, limit: int = 10):
    """
    Fetch articles from a single RSS feed.
    """
    try:
        feed = feedparser.parse(feed_url)
        articles = []
        for entry in feed.entries[:limit]:
            articles.append({
                "title": entry.get("title", ""),
                "link": entry.get("link", ""),
                "summary": entry.get("summary", "")
            })
        return articles
    except Exception as e:
        print(f"[RSS Error] {e}")
        return []


def get_feed(feed_name: str):
    """
    Get articles from a named feed.
    """

    url = RSS_FEEDS.get(feed_name.lower())

    if not url:
        return []

    return fetch_feed(url)


def get_all_feeds():
    """
    Fetch articles from all configured RSS feeds.
    """

    articles = []

    for _, url in RSS_FEEDS.items():
        articles.extend(fetch_feed(url))

    return articles