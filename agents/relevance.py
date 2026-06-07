from llm import invoke_llm
import re


def relevance_agent(state):
    logs = state.get("logs", [])
    logs.append("🎯 Relevance Agent: Ranking articles by relevance...")

    query = state.get("query", "")
    is_exam_prep = state.get("is_exam_prep", True)

    all_news = (
        state.get("sports_news", [])[:5]
        + state.get("business_news", [])[:5]
        + state.get("national_news", [])[:5]
        + state.get("international_news", [])[:5]
    )

    if not all_news:
        logs.append("⚠️ Relevance Agent: No articles found.")
        return {
            "relevant_news": "",
            "logs": logs
        }

    article_list = []

    for idx, article in enumerate(all_news):
        title = article.get("title", "No Title")
        url = article.get("url", "")

        article_list.append(
            f"[{idx}] {title}\nURL: {url}"
        )

    prompt = f"""
You are a News Ranking Agent.

User Query:
{query}

UPSC Mode:
{is_exam_prep}

Articles:
{chr(10).join(article_list)}

Task:
1. Score each article for:
   - Query Relevance (1-10)
   - Educational Value (1-10)

2. Select the best 5 articles.

3. Return ONLY the URLs.

Example:

https://example1.com
https://example2.com
https://example3.com

No explanations.
"""

    response = invoke_llm(prompt, role="balanced")

    urls = re.findall(
        r'https?://[^\s]+',
        response
    )

    selected_urls = urls[:5]


    return {
        "relevant_news": "\n".join(selected_urls),
        "logs": logs
    }