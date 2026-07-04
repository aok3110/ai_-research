import os
import requests
import json
import re
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("OPENROUTER_API_KEY")


def clean_json(text):
    """fix OpenRouter messy output"""
    try:
        return json.loads(text)
    except:
        match = re.search(r"\{.*\}", text, re.DOTALL)
        if match:
            return json.loads(match.group())
        return None


def analyze_company(text, company_name):

    if not API_KEY:
        return fallback(company_name)

    url = "https://openrouter.ai/api/v1/chat/completions"

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    prompt = f"""
Return ONLY JSON:

{{
  "summary": "...",
  "industry": "...",
  "products": ["..."],
  "pain_points": ["..."],
  "keywords": ["..."]
}}

Company: {company_name}

Data:
{text[:3000]}
"""

    payload = {
        "model": "openai/gpt-4o-mini",
        "messages": [{"role": "user", "content": prompt}]
    }

    try:
        res = requests.post(url, headers=headers, json=payload, timeout=20)
        data = res.json()

        content = data["choices"][0]["message"]["content"]

        parsed = clean_json(content)

        if parsed:
            return parsed

        return fallback(company_name)

    except Exception as e:
        print("AI ERROR:", e)
        return fallback(company_name)


def fallback(company_name):
    return {
        "summary": f"{company_name} is a global company.",
        "industry": "Unknown",
        "products": [],
        "pain_points": [],
        "keywords": [company_name]
    }