
from tools.context7 import client

async def context7_agent(state):
    query = state["query"]

    tools = await client.get_tools()

    result = await tools[0].ainvoke({
        "query": query
    })

    logs = state.get("logs", [])

    return {
        "latest_context": str(result),
        "logs": logs
    }