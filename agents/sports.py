from tools.web_loader import get_links_from_web

def sports_agent(state):
    logs = state.get("logs", [])
    plan = state.get("categories_required", [])
    if "sports" not in plan:
        return {"sports_news": [], "logs": logs}
    
    hub_urls = ["https://www.indiatoday.in/sports","https://www.republicworld.com/sports-news","https://www.timesnownews.com/sports"]
    all_news = []
    for url in hub_urls:
        try:
            news = get_links_from_web(url)
            all_news.extend(news)
        except Exception as e:
            logs.append(f"Error fetching from {url}: {e}")
            
    return {"sports_news": all_news, "logs": logs}