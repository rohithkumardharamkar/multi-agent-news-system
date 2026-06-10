from tools.web_loader import get_links_from_web

def business_agent(state):
    logs = state.get("logs", [])
    plan = state.get("categories_required", [])
    if "business" not in plan:
        return {"business_news": [], "logs": logs}
    
    hub_urls = ["https://www.indiatoday.in/business","https://www.republicworld.com/business-news","https://www.timesnownews.com/business-economy"]
    all_news = []
    for url in hub_urls:
        try:
            news = get_links_from_web(url)
            all_news.extend(news)
        except Exception as e:
            logs.append(f"Error fetching from {url}: {e}")
            
    return {"business_news": all_news, "logs": logs}