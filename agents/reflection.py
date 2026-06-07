from llm import invoke_llm

def reflection_agent(state):
    logs = state.get("logs", [])

    summary = state.get("summary", "")
    prompt = f"""
    Reflect on the following news summary for quality, tone, and completeness:
    {summary}
    Suggest any improvements or additional context that might be missing for UPSC students.
    """
    result_text = invoke_llm(prompt, role="reasoning")
    return {"reflection": result_text, "logs": logs}