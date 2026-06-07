from llm import invoke_llm

def factcheck_agent(state):
    logs = state.get("logs", [])
    news = state.get("extracted_content") or state.get("relevant_news", "")
    if not news or "No news found" in news:
        return {"verified_news": news, "logs": logs}
    prompt = f"""
    Fact Check the following news summary:
    {news[:3000]}
    Identify any potential misinformation or unverified claims.
    Provide a credibility score (0-10) and a brief justification for each major point.
    Return the verified/cleaned version of the news.
    """
    result_text = invoke_llm(prompt, role="balanced")
    return {"verified_news": result_text, "logs": logs}