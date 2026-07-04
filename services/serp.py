import os
import requests
from dotenv import load_dotenv

load_dotenv()

SERPER_API_KEY = os.getenv("SERPER_API_KEY")


def find_competitors(company_name):

    if not SERPER_API_KEY:
        print("SERPER KEY MISSING")
        return []

    url = "https://google.serper.dev/search"

    headers = {
        "X-API-KEY": SERPER_API_KEY,
        "Content-Type": "application/json"
    }

    payload = {
        "q": f"{company_name} competitors"
    }

    try:
        res = requests.post(url, json=payload, headers=headers, timeout=10)
        data = res.json()

        competitors = []

        for item in data.get("organic", []):
            title = item.get("title")
            link = item.get("link")

            if title and link:
                competitors.append({
                    "name": title,
                    "website": link
                })

        return competitors[:5]

    except Exception as e:
        print("SERP ERROR:", e)
        return []