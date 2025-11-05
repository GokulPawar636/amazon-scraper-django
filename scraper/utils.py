import requests
from bs4 import BeautifulSoup

def scrape_amazon_product(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept-Language": "en-US,en;q=0.9"
    }
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, "html.parser")

    title = soup.find(id="productTitle")
    price = soup.select_one("span.a-price span.a-offscreen")
    rating = soup.select_one("span.a-icon-alt")

    return {
        "title": title.get_text(strip=True) if title else "Title not found",
        "price": price.get_text(strip=True) if price else "Price not found",
        "rating": rating.get_text(strip=True) if rating else "Rating not found"
    }
