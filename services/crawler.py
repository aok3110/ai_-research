import requests
from bs4 import BeautifulSoup

def crawl_website(url):

    if not url or "google.com" in url:
        return ""

    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        res = requests.get(url, headers=headers, timeout=5)

        soup = BeautifulSoup(res.text, "html.parser")

        for tag in soup(["script", "style", "noscript"]):
            tag.extract()

        return soup.get_text(separator=" ", strip=True)[:3000]

    except:
        return ""