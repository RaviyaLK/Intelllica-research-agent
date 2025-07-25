from newspaper import Article
import requests
import os
from dotenv import load_dotenv

load_dotenv()

RAPIDAPI_HOST = "real-time-web-search.p.rapidapi.com"
RAPIDAPI_KEY = os.getenv("RAPIDAPI_KEY")

def fetch_full_article(url: str) -> str:
    try:
        article = Article(url)
        article.download()
        article.parse()
        return article.text
    except Exception as e:
        print(f"Failed to extract article from {url}: {e}")
        return ""

def web_search(query: str) -> list[dict]:
    url = "https://real-time-web-search.p.rapidapi.com/search-advanced"
    headers = {
        "x-rapidapi-host": RAPIDAPI_HOST,
        "x-rapidapi-key": RAPIDAPI_KEY,
    }
    params = {
        "q": query,
        "num": 10,
        "start": 0,
        "gl": "us",
        "hl": "en",
        "device": "desktop",
        "nfpr": 0,
    }

    response = requests.get(url, headers=headers, params=params)

    if response.status_code != 200:
        print(f"Error: API returned status {response.status_code}: {response.text}")
        return []

    data = response.json()
    search_results = data.get("data", [])

    articles = []
    for item in search_results:
        published_date = item.get("published_date") or item.get("date") or "n.d."
        url = item.get("url", "")
        full_content = fetch_full_article(url)

        article = {
            "title": item.get("title", ""),
            "source": item.get("source", "Unknown Source"),
            "url": url,
            "content": full_content if full_content else item.get("snippet", ""),
            "published_date": published_date,
        }
        articles.append(article)

    return articles
