from tools.web_loader import get_links_from_web

def national_agent(state):
    logs = state.get("logs", [])
    plan = state.get("categories_required", [])
    if "national" not in plan:
        return {"national_news": [], "logs": logs}
    hub_urls = ["https://www.thehindu.com/news/national/","https://www.indiatoday.in/india","https://www.republicworld.com/india-news","https://www.timesnownews.com/india"]
    
    all_news = []
    for url in hub_urls:
        try:
            news = get_links_from_web(url)
            all_news.extend(news)
        except Exception as e:
            logs.append(f"Error fetching from {url}: {e}")
            
    return {"national_news": all_news, "logs": logs}