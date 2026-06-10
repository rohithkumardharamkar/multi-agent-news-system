from llm import invoke_llm
import re
from prompts import build_relevance_prompt


def relevance_agent(state):
    logs = state.get("logs", [])
    query = state.get("query", "")
    is_exam_prep = state.get("is_exam_prep", True)
    all_news = (
        state.get("sports_news", [])[:5]
        + state.get("business_news", [])[:5]
        + state.get("national_news", [])[:5]
        + state.get("international_news", [])[:5]
    )

    if not all_news:
        return {"relevant_news": "","logs": logs}

    article_list = []

    for idx, article in enumerate(all_news):
        title = article.get("title", "No Title")
        url = article.get("url", "")

        article_list.append(f"[{idx}] {title}\nURL: {url}")

    prompt = build_relevance_prompt(query=query,is_exam_prep=is_exam_prep,article_list=article_list,)
    response = invoke_llm(prompt, role="balanced")
    urls = re.findall(r'https?://[^\s]+',response)
    selected_urls = urls[:5]

    return {
        "relevant_news": "\n".join(selected_urls),
        "logs": logs
    }
