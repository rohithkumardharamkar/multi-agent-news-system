from tools.web_loader import load_web_content
import re

def loader_agent(state):
    logs = state.get("logs", [])

    relevant_news = state.get("relevant_news", "")
    if not relevant_news or "No news found" in relevant_news:
        return {"extracted_content": "No relevant URLs to load.", "logs": logs}

    urls = re.findall(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', relevant_news)
    top_urls = list(dict.fromkeys(urls))[:5]
    if not top_urls:
        return {"extracted_content": "No valid URLs found in relevant news.", "logs": logs}

    docs = load_web_content(top_urls)
    combined_content = ""
    for doc in docs:
        title = doc.metadata.get("title", "Untitled")
        url = doc.metadata.get("source", "")
        content = doc.page_content
        combined_content += f"\n--- Source: {title} ({url}) ---\n{content}\n"

    return {"extracted_content": combined_content or "Failed to extract content from URLs.", "logs": logs}
