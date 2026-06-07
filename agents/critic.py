from llm import invoke_llm

def critic_agent(state):
    logs = state.get("logs", [])
    summary = state.get("summary", "")
    reflection = state.get("reflection", "")
    prompt = f"""
    Review the news summary and its reflection:
    Summary: {summary}
    Reflection: {reflection}
    Act as a sharp editor for a UPSC news magazine. 
    Point out any bias, verbosity, or missing key facts.
    Provide constructive criticism to improve academic rigor.
    """
    result_text = invoke_llm(prompt, role="reasoning")
    return {"critique": result_text, "logs": logs}