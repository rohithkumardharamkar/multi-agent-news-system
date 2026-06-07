import re
from llm import invoke_local_first

BLOCKED_PATTERNS = [
    r"ignore previous instructions",
    r"system prompt",
    r"reveal secrets",
    r"api key",
    r"password",
    r"delete database",
    r"drop table",
    r"rm -rf",
]


def validate_input(query: str):

    if not query:
        raise ValueError(
            "Query cannot be empty"
        )

    query_lower = query.lower()

    for pattern in BLOCKED_PATTERNS:

        if re.search(
            pattern,
            query_lower
        ):
            raise ValueError(
                f"Blocked input detected: {pattern}"
            )
            
    # Restrict to News and Current Affairs
    prompt = f"""
    Analyze the following user query for a news application:
    "{query}"
    
    Is this query asking for news, journalism, current affairs, government schemes, policies, or exam preparation?
    Note: The user might also ask to send the results to their email or perform other app-related actions within the query. This is completely okay.
    
    If the core topic is about news, current affairs, national/international/business/sports news, or government schemes, reply ONLY with 'ACCEPT'.
    If the user is asking strictly about non-news stuff (like writing code, recipes, personal tasks unrelated to the app), reply ONLY with 'REJECT'.
    """
    res = invoke_local_first(prompt, role="speed")
    if "REJECT" in res.upper() and "ACCEPT" not in res.upper():
        raise ValueError("Query restricted: the system handles only news, current affairs, and government schemes.")

    return True