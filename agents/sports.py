from tools.web_loader import get_links_from_web

def sports_agent(state):
    logs = state.get("logs", [])
    plan = state.get("categories_required", [])
    if "sports" not in plan:
        return {"sports_news": [], "logs": logs}
    hub_url = "https://www.indiatoday.in/sports"
    news = get_links_from_web(hub_url)
    return {"sports_news": news, "logs": logs}