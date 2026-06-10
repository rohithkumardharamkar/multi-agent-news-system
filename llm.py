import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
load_dotenv()
TEMPERATURE = float(os.getenv("TEMPERATURE", "0.3"))
_GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")
GROQ_MODELS = {"speed": "llama-3.1-8b-instant","balanced": "llama-3.1-8b-instant","reasoning": "llama-3.3-70b-versatile",}
def _get_groq(role: str = "balanced") -> ChatGroq:
    if not _GROQ_API_KEY:
        raise RuntimeError("GROQ_API_KEY is not configured in .env")
    model = GROQ_MODELS.get(role,GROQ_MODELS["balanced"])
    return ChatGroq(groq_api_key=_GROQ_API_KEY,model_name=model,temperature=TEMPERATURE,)


def invoke_llm(prompt: str,role: str = "balanced") -> str:
    try:
        llm = _get_groq(role)
        response = llm.invoke(prompt)
        return str(getattr(response, "content", response)).strip()
    except Exception as e:
        print(f"[Groq/{role}] Error: {e}")
        return f"Error: {e}"


def get_primary_llm():
    return _get_groq("balanced")


def get_groq_llm(role: str = "balanced"):
    return _get_groq(role)


def invoke_local_first(prompt: str,role: str = "balanced") -> str:
    return invoke_llm(prompt, role)


def invoke_with_fallback(prompt: str,fallback_text: str = "",role: str = "balanced") -> str:
    text = invoke_llm(prompt,role=role)
    if text and not text.startswith("Error:"):
        return text
    return fallback_text