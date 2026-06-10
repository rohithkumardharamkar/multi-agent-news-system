from llm import invoke_llm
import json
import re

def extract_email(text):
    match = re.search(r'[\w\.-]+@[\w\.-]+\.\w+',text)
    return match.group(0) if match else ""
def planner_agent(state):
    logs = state.get("logs", [])
    logs.append("Planner Agent: Analyzing query to determine categories...")
    if state.get("categories_required"):
        return {
            "plan": f"User explicitly selected: {', '.join(state['categories_required'])}",
            "categories_required": state["categories_required"],
            "logs": logs,
        }

    query = state["query"]
    target_email = extract_email(query)

    prompt = f"""
            You are a News Planning Agent.
            User Query:
            {query}
            Determine which news categories are relevant.
            Available Categories:
            - International
            - National
            - Sports
            - Business
            Rules:
            1. Return ONLY a JSON array.
            2. Do not return explanations.
            3. Use exact category names.

            Examples:

            ["Sports"]

            ["Business","International"]

            ["National","Business"]

            JSON:
            """
    content = invoke_llm(prompt, role="reasoning")
    try:
        if "```json" in content:
            content = content.split("```json")[-1].split("```")[0].strip()
        elif "```" in content:
            content = content.split("```")[-1].split("```")[0].strip()
        categories = json.loads(content)
        if not isinstance(categories, list):
            categories = []
    except Exception:
        categories = []
        for cat in ["International","National","Sports","Business"]:
            if cat.lower() in content.lower():
                categories.append(cat)
    if not categories:
        categories = ["International","National","Sports","Business"]
    cats = [c.lower() for c in categories]
    logs.append(f"Planner Agent: Identified categories → {cats}")

    return {"plan": content,"categories_required": cats,"target_email": target_email,
        "logs": logs,
    }