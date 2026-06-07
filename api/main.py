from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from workflow import graph
import uvicorn
import os

app = FastAPI(title="Multi-Agent News System API")

class QueryRequest(BaseModel):
    query: str

@app.post("/generate-news")
async def generate_news(request: QueryRequest):
    if not request.query:
        raise HTTPException(status_code=400, detail="Query cannot be empty")
    
    try:
        initial_state = {
            "query": request.query,
            "error": "",
            "sports_news": [],
            "business_news": [],
            "national_news": [],
            "international_news": []
        }
        
        # Run the workflow
        final_state = graph.invoke(initial_state)
        
        if final_state.get("error"):
            return {
                "status": "error",
                "message": final_state["error"]
            }
            
        return {
            "status": "success",
            "magazine_report": final_state.get("magazine_report", ""),
            "email_status": final_state.get("email_status", ""),
            "categories_covered": final_state.get("categories_required", [])
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
def health_check():
    return {"status": "ok"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
