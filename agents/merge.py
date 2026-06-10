
def merge_agent(state):
    logs = state.get("logs", [])
    all_news = []
    all_news.extend(state.get("sports_news", []))
    all_news.extend(state.get("business_news", []))
    all_news.extend(state.get("national_news", []))
    all_news.extend(state.get("international_news", []))
    return {"all_news": all_news,"logs": logs}