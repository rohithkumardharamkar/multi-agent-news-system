from langgraph.types import interrupt

def human_review_node(state):
    logs = state.get("logs", [])
    response = interrupt({"magazine_report": state.get("magazine_report", ""),"critique": state.get("critique", "")})
    approved = response.get("status") == "approve"
    action = "Approved ✓" if approved else "Rejected ✗"
    return {"human_approved": approved,"review_comments": response.get("comments", ""),"logs": logs}