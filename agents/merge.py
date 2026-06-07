
def merge_agent(state):
    logs = state.get("logs", [])
    logs.append("🔗 Merge Agent: Combining category news")

    all_news = []

    all_news.extend(state.get("sports_news", []))
    all_news.extend(state.get("business_news", []))
    all_news.extend(state.get("national_news", []))
    all_news.extend(state.get("international_news", []))

    return {
        "all_news": all_news,
        "logs": logs
    }