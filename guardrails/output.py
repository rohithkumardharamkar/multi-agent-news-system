import re

def validate_output(content: str):
    if not content:
        raise ValueError("Empty response generated")
    suspicious_patterns = [r"gsk_[a-zA-Z0-9]{30,}",  r"tvly-[a-zA-Z0-9]{30,}",]
    for pattern in suspicious_patterns:
        if re.search(pattern, content):
            raise ValueError("Potential API key leaked in output")
    return True