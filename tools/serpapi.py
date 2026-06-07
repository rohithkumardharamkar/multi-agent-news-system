from serpapi import GoogleSearch
from config.settings import SERPAPI_API_KEY


def serpapi_search(query: str, num_results: int = 10):
    if not SERPAPI_API_KEY or SERPAPI_API_KEY.lower().startswith("your_"):
        return []

    try:
        params = {"engine": "google","q": query,"api_key": SERPAPI_API_KEY,"num": num_results}
        search = GoogleSearch(params)
        results = search.get_dict()
        return results.get("organic_results",[])
    except Exception as e:
        print(f"[SerpAPI Error] {e}")
        return []
