from guardrails.input import validate_input
from guardrails.output import validate_output

def input_guardrail_node(state):
    logs = state.get("logs", [])
    query = state.get("query", "")
    try:
        validate_input(query)
        result = dict(state)
        result["logs"] = logs
        return result
    except ValueError as e:
        return {"error": str(e), "logs": logs}

def output_guardrail_node(state):
    logs = state.get("logs", [])
    report = state.get("magazine_report", "")
    try:
        validate_output(report)
        result = dict(state)
        result["logs"] = logs
        return result
    except ValueError as e:
        return {"error": str(e), "logs": logs}

def guardrail_condition(state):
    if state.get("error"):
        return "error_node"
    return "next_node"

def error_node(state):
    logs = state.get("logs", [])
    return {"logs": logs}
