from tools.web_loader import get_links_from_web

def national_agent(state):
    logs = state.get("logs", [])
    plan = state.get("categories_required", [])
    if "national" not in plan:
        return {"national_news": [], "logs": logs}
    hub_url = "https://www.thehindu.com/news/national/"
    news = get_links_from_web(hub_url)
    return {"national_news": news, "logs": logs}