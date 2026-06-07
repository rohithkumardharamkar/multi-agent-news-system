from tools.web_loader import get_links_from_web

def business_agent(state):
    logs = state.get("logs", [])
    plan = state.get("categories_required", [])
    if "business" not in plan:
        return {"business_news": [], "logs": logs}
    hub_url = "https://www.indiatoday.in/business"
    news = get_links_from_web(hub_url)
    return {"business_news": news, "logs": logs}