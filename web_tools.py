import requests

SERPAPI_KEY = "your_serpapi_key"

def search_web(query):
    url = f"https://serpapi.com/search.json?q={query}&api_key={SERPAPI_KEY}"
    res = requests.get(url)
    results = res.json().get("organic_results", [])
    return results[:3]  # top 3 results