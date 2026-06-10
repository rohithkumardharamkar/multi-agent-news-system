from llm import invoke_llm
from prompts import build_summary_prompt

def summary_agent(state):
    logs = state.get("logs", [])
    news = state.get("extracted_content") or state.get("verified_news", "")
    if not news or "No news found" in news:
        return {"summary": "Nothing to summarize.", "logs": logs}
    is_exam_prep = state.get("is_exam_prep", True)
    prompt = build_summary_prompt(news, is_exam_prep)
    result_text = invoke_llm(prompt, role="balanced")
    return {"summary": result_text, "logs": logs}
