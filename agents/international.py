from tools.web_loader import get_links_from_web

def international_agent(state):
    logs = state.get("logs", [])
    plan = state.get("categories_required", [])
    if "international" not in plan:
        return {"international_news": [], "logs": logs}
    hub_urls = ["https://www.thehindu.com/news/international/","https://www.indiatoday.in/world","https://www.republicworld.com/world-news","https://www.timesnownews.com/world"]
    all_news = []
    for url in hub_urls:
        try:
            news = get_links_from_web(url)
            all_news.extend(news)
        except Exception as e:
            logs.append(f"Error fetching from {url}: {e}")
            
    return {"international_news": all_news, "logs": logs}