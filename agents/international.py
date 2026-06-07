from tools.web_loader import get_links_from_web

def international_agent(state):
    logs = state.get("logs", [])
    plan = state.get("categories_required", [])
    if "international" not in plan:
        return {"international_news": [], "logs": logs}
    hub_url = "https://www.thehindu.com/news/international/"
    news = get_links_from_web(hub_url)
    return {"international_news": news, "logs": logs}