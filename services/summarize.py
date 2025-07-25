# services/summarize.py
import os
import json
import requests
from dotenv import load_dotenv

load_dotenv()

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

def generate_prompt_with_citations(articles: list[dict]) -> str:
    prompt = (
        "You're an intelligent research assistant. Summarize the following articles into clear, well-structured paragraphs. "
        "Embed inline citations using the source name and year, like [Forbes, 2024]. "
        "At the end, include a properly formatted References section (APA style). Keep content informative and citation-rich.\n\n"
    )

    for i, article in enumerate(articles, start=1):
        title = article.get("title", "")
        source = article.get("source", "Unknown Source")
        url = article.get("url", "")
        year = article.get("published_date", "")
        if year and len(year) >= 4:
            year = year[:4]
        content = article.get("content") or article.get("snippet") or ""
        max_length = 1000
        content = content[:max_length] + ("..." if len(content) > max_length else "")

        prompt += f"--- ARTICLE {i} ---\n"
        prompt += f"Title: {title}\n"
        prompt += f"Source: {source}\n"
        prompt += f"Year: {year}\n"
        prompt += f"URL: {url}\n"
        prompt += f"Content:\n{content}\n\n"

    return prompt

def summarize_text(articles: list[dict]) -> str:
    url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
        "X-Title": "Intellica"
    }

    prompt = generate_prompt_with_citations(articles)
    print("Prompt sent to LLM:\n", prompt)  # Optional debug print

    payload = {
        "model": "deepseek/deepseek-r1-0528-qwen3-8b:free",
        "messages": [
            {"role": "system", "content": "You are a helpful assistant that summarizes content in an academic and formal tone."},
            {"role": "user", "content": f"Please summarize the following text in a formal academic style, with clear, concise bullet points or paragraphs:\n\n{prompt}"}
        ]
    }

    try:
        response = requests.post(url, headers=headers, data=json.dumps(payload))
        response.raise_for_status()
        return response.json()["choices"][0]["message"]["content"].strip()
    except requests.RequestException as e:
        print("Error from OpenRouter:", e)
        return "Summary unavailable due to API error."
