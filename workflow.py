from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import MemorySaver

from agents.state import NewsState
from agents.planner import planner_agent
from agents.sports import sports_agent
from agents.business import business_agent
from agents.national import national_agent
from agents.international import international_agent
from agents.relevance import relevance_agent
from agents.fact_check import factcheck_agent
from agents.summary import summary_agent
from agents.reflection import reflection_agent
from agents.critic import critic_agent
from agents.magazine import magazine_agent
from agents.email import email_agent
from agents.loader import loader_agent

from human_review import human_review_node

from agents.guardrail_nodes import (
    input_guardrail_node,
    output_guardrail_node,
    guardrail_condition,
    error_node
)


def review_condition(state):
    return "email" if state.get("human_approved") else END


def category_router(state):
    categories = state.get("categories_required", [])

    routes = []

    if "sports" in categories:
        routes.append("sports")

    if "business" in categories:
        routes.append("business")

    if "national" in categories:
        routes.append("national")

    if "international" in categories:
        routes.append("international")

    if not routes:
        routes = [
            "sports",
            "business",
            "national",
            "international"
        ]

    return routes


def build_graph():
    workflow = StateGraph(NewsState)

    # Core Nodes
    workflow.add_node("input_guardrail", input_guardrail_node)
    workflow.add_node("planner", planner_agent)

    workflow.add_node("sports", sports_agent)
    workflow.add_node("business", business_agent)
    workflow.add_node("national", national_agent)
    workflow.add_node("international", international_agent)

    workflow.add_node("relevance", relevance_agent)
    workflow.add_node("loader", loader_agent)
    workflow.add_node("factcheck", factcheck_agent)
    workflow.add_node("summary", summary_agent)
    workflow.add_node("reflection", reflection_agent)
    workflow.add_node("critic", critic_agent)
    workflow.add_node("magazine", magazine_agent)

    workflow.add_node("human_review", human_review_node)
    workflow.add_node("email", email_agent)

    workflow.add_node("output_guardrail", output_guardrail_node)
    workflow.add_node("error_node", error_node)

    # Start
    workflow.add_edge(START, "input_guardrail")

    # Input Guardrail
    workflow.add_conditional_edges(
        "input_guardrail",
        guardrail_condition,
        {
            "error_node": "error_node",
            "next_node": "planner"
        }
    )

    # Planner Routing
    workflow.add_conditional_edges(
        "planner",
        category_router,
        {
            "sports": "sports",
            "business": "business",
            "national": "national",
            "international": "international",
        }
    )

    # Category Agents
    workflow.add_edge("sports", "relevance")
    workflow.add_edge("business", "relevance")
    workflow.add_edge("national", "relevance")
    workflow.add_edge("international", "relevance")

    # Processing Pipeline
    workflow.add_edge("relevance", "loader")
    workflow.add_edge("loader", "factcheck")
    workflow.add_edge("factcheck", "summary")
    workflow.add_edge("summary", "reflection")
    workflow.add_edge("reflection", "critic")
    workflow.add_edge("critic", "magazine")

    # Human Review
    workflow.add_edge("magazine", "human_review")

    workflow.add_conditional_edges(
        "human_review",
        review_condition,
        {
            "email": "email",
            END: END
        }
    )

    # Email + Output Guardrail
    workflow.add_edge("email", "output_guardrail")

    workflow.add_conditional_edges(
        "output_guardrail",
        guardrail_condition,
        {
            "error_node": "error_node",
            "next_node": END
        }
    )

    workflow.add_edge("error_node", END)

    memory = MemorySaver()

    return workflow.compile(
        checkpointer=memory
    )


graph = build_graph()