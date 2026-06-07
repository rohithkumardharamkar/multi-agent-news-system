from llm import invoke_llm

def magazine_agent(state):
    logs = state.get("logs", [])

    summary = state.get("summary", "")
    critique = state.get("critique", "")
    is_exam_prep = state.get("is_exam_prep", True)
    if is_exam_prep:
        tone_and_style = """
        Use an ANALYTICAL and INFORMATIVE tone. 
        Instead of a 'vibrant' style, use a 'Bureaucratic/Academic' style.
        Ensure sub-headlines correlate to UPSC GS categories (e.g., GS-II: Governance, GS-III: Economy).
        Include a 'Quick Facts for Prelims' section.
        """
    else:
        tone_and_style = "Use a vibrant and engaging tone."
    prompt = f"""
    Create a professional magazine-style report based on the news summary and the editor's critique.
    Summary: {summary}
    Critique: {critique}
    The final report should include:
    1. A catchy headline.
    2. Sectioned content with sub-headlines.
    3. Key takeaways.
    4. A professional conclusion.
    5. A 'Direct Source Links' section at the end for further reading.
    {tone_and_style}
    """
    result_text = invoke_llm(prompt, role="reasoning")
    return {"magazine_report": result_text, "logs": logs}