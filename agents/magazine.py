from llm import invoke_llm
from prompts import build_magazine_prompt

def magazine_agent(state):
    logs = state.get("logs", [])
    summary = state.get("summary", "")
    critique = state.get("critique", "")
    is_exam_prep = state.get("is_exam_prep", True)
    prompt = build_magazine_prompt(summary=summary,critique=critique,is_exam_prep=is_exam_prep,)
    result_text = invoke_llm(prompt, role="reasoning")
    return {"magazine_report": result_text, "logs": logs}
