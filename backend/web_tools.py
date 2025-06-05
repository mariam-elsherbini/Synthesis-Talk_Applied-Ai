import requests
import os
from dotenv import load_dotenv

load_dotenv()

SERPAPI_KEY = os.getenv("SERPAPI_KEY", "")

def search_web(query):
    """
    Basic web search function. If no SERPAPI_KEY is provided,
    returns mock results for testing purposes.
    """
    if not SERPAPI_KEY:
        # Return mock results for testing
        return [
            {
                "title": f"Mock Result 1 for '{query}'",
                "snippet": "This is a mock search result. Please add your SERPAPI_KEY to .env file for real search results.",
                "link": "https://example.com"
            },
            {
                "title": f"Mock Result 2 for '{query}'",
                "snippet": "Another mock result. The search functionality will work once you configure the API key.",
                "link": "https://example.com"
            }
        ]
    
    try:
        url = f"https://serpapi.com/search.json?q={query}&api_key={SERPAPI_KEY}"
        res = requests.get(url, timeout=10)
        if res.status_code == 200:
            results = res.json().get("organic_results", [])
            return results[:3]  # top 3 results
        else:
            return [{"title": "Search Error", "snippet": f"API returned status code: {res.status_code}"}]
    except Exception as e:
        return [{"title": "Search Error", "snippet": f"Error occurred: {str(e)}"}]