from tavily import TavilyClient
from config.settings import TAVILY_API_KEY


def tavily_search(query: str, max_results: int = 10, include_domains: list = None):
    """
    Search news using Tavily with optional domain filtering.
    """
    if not TAVILY_API_KEY or TAVILY_API_KEY.lower().startswith("your_"):
        return []

    try:
        client = TavilyClient(api_key=TAVILY_API_KEY)
        response = client.search(
            query=query,
            max_results=max_results,
            include_domains=include_domains
        )
        return response.get("results", [])
    except Exception as e:
        print(f"[Tavily Error] {e}")
        return []

def tavily_extract_content(urls: list):
    """
    Extract full content from a list of URLs using Tavily.
    """
    if not TAVILY_API_KEY or not urls:
        return []

    try:
        client = TavilyClient(api_key=TAVILY_API_KEY)
        response = client.extract(urls=urls)
        return response.get("results", [])
    except Exception as e:
        print(f"[Tavily Extract Error] {e}")
        return []

def tavily_crawl(url: str):
    """
    Crawl a specific URL to find latest news and content.
    """
    if not TAVILY_API_KEY or not url:
        return {}

    try:
        client = TavilyClient(api_key=TAVILY_API_KEY)
        # Crawl returns a structured response of the page
        response = client.crawl(url=url)
        return response
    except Exception as e:
        print(f"[Tavily Crawl Error] {e}")
        return {}
