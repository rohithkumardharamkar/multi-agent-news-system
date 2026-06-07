from llm import invoke_llm

def summary_agent(state):
    logs = state.get("logs", [])

    news = state.get("extracted_content") or state.get("verified_news", "")
    if not news or "No news found" in news:
        return {"summary": "Nothing to summarize.", "logs": logs}

    is_exam_prep = state.get("is_exam_prep", True)
    if is_exam_prep:
        summary_instructions = """
        Format this as an EXAM-PREP DIGEST. For each major point:
        1. Context/Background.
        2. Key Facts/Stats.
        3. Significance for Exam/Policy Impact.
        
        Keep it highly informative and data-rich. Avoid fluff.
        """
    else:
        summary_instructions = "Maintain a professional tone and highlight key takeaways."

    prompt = f"""
    Summarize the following verified news into a concise digest:
    {news[:4000]}
    
    {summary_instructions}
    """
    
    result_text = invoke_llm(prompt, role="balanced")
    return {"summary": result_text, "logs": logs}