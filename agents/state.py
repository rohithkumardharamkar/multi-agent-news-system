from typing import TypedDict, List, Dict, Optional, Annotated
import operator


class NewsState(TypedDict):
    # ---------- Input ----------
    query: str
    target_email: str
    is_exam_prep: bool

    # ---------- Planning ----------
    plan: str
    categories_required: List[str]
    latest_context: str

    # ---------- Raw News ----------
    sports_news: List[Dict]
    business_news: List[Dict]
    national_news: List[Dict]
    international_news: List[Dict]

    # Combined News
    all_news: List[Dict]

    # ---------- Processing ----------
    relevant_news: str
    extracted_content: str
    verified_news: str
    summary: str
    reflection: str
    critique: str

    # ---------- Metadata ----------
    sources: List[str]
    confidence_score: float

    # ---------- Human Review ----------
    human_approved: Optional[bool]
    review_comments: Optional[str]

    # ---------- Final Output ----------
    magazine_report: str
    email_status: str
    error: str

    # ---------- Logs ----------
    logs: Annotated[List[str], operator.add]