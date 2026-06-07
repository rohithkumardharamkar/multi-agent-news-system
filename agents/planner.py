from llm import invoke_llm
from tools.tavily import tavily_search
import json


def planner_agent(state):
    logs = state.get("logs", [])
    logs.append("📋 Planner Agent: Analyzing query to determine categories...")

    if state.get("categories_required"):

        return {
            "plan": f"User explicitly selected: {', '.join(state['categories_required'])}",
            "categories_required": state["categories_required"],
            "logs": logs,
        }

    query = state["query"]

    try:
        latest_context = tavily_search(
            f"latest news related to {query}"
        )

        logs.append("📋 Planner Agent: Retrieved latest news context.")
    except Exception as e:
        latest_context = ""


    prompt = f"""
You are a News Planning Agent.

User Query:
{query}

Latest News Context:
{latest_context}

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
        # Remove markdown blocks if present
        if "```json" in content:
            content = content.split("```json")[-1].split("```")[0].strip()
        elif "```" in content:
            content = content.split("```")[-1].split("```")[0].strip()

        categories = json.loads(content)

        if not isinstance(categories, list):
            categories = []

    except Exception:
        categories = []

        for cat in [
            "International",
            "National",
            "Sports",
            "Business"
        ]:
            if cat.lower() in content.lower():
                categories.append(cat)

    # Fallback
    if not categories:
        categories = [
            "International",
            "National",
            "Sports",
            "Business"
        ]
        logs.append(
            "⚠️ Planner Agent: No categories detected. Using all categories."
        )

    cats = [c.lower() for c in categories]

    logs.append(
        f"📋 Planner Agent: Identified categories → {cats}"
    )

    return {
        "plan": content,
        "categories_required": cats,
        "latest_context": latest_context,
        "logs": logs,
    }