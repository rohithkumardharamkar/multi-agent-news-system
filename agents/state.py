from typing import TypedDict, List, Dict, Optional, Annotated
import operator


class NewsState(TypedDict):
    query: str
    target_email: str
    is_exam_prep: bool
    plan: str
    categories_required: List[str]
    latest_context: str
    sports_news: List[Dict]
    business_news: List[Dict]
    national_news: List[Dict]
    international_news: List[Dict]
    all_news: List[Dict]
    relevant_news: str
    extracted_content: str
    summary: str
    sources: List[str]
    confidence_score: float
    human_approved: Optional[bool]
    review_comments: Optional[str]
    magazine_report: str
    email_status: str
    error: str
    logs: Annotated[List[str], operator.add]