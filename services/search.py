import requests
from bs4 import BeautifulSoup
from urllib.parse import unquote


def clean_url(url):
    if "uddg=" in url:
        url = url.split("uddg=")[-1]
        return unquote(url)
    return url


def find_official_website(company_name):
    try:
        query = f"{company_name} official website"

        url = "https://duckduckgo.com/html/"
        params = {"q": query}

        headers = {"User-Agent": "Mozilla/5.0"}

        res = requests.get(url, params=params, headers=headers, timeout=8)

        soup = BeautifulSoup(res.text, "html.parser")

        links = soup.find_all("a", class_="result__a")

        for link in links:
            href = link.get("href")

            if href and "http" in href:
                return clean_url(href)

        return None

    except Exception as e:
        print("Search error:", e)
        return None