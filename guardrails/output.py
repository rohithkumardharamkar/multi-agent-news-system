import re


def validate_output(content: str):

    if not content:
        raise ValueError(
            "Empty response generated"
        )

    suspicious_patterns = [
        r"gsk_[a-zA-Z0-9]{30,}",  # Groq API key pattern
        r"tvly-[a-zA-Z0-9]{30,}", # Tavily API key pattern
    ]

    for pattern in suspicious_patterns:
        if re.search(pattern, content):
            raise ValueError("Potential API key leaked in output")

    return True