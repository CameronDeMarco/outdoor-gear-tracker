import requests
from bs4 import BeautifulSoup


def scrape_books(url):

    print("Books scraper started")

    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    response = requests.get(
        url,
        headers=headers,
        timeout=15
    )

    soup = BeautifulSoup(
        response.text,
        "html.parser"
    )

    product = soup.find(
        "article",
        class_="product_pod"
    )

    title = product.h3.a["title"]

    price = product.find(
        "p",
        class_="price_color"
    ).text

    return {
        "store": "Books",
        "title": title,
        "price": price
    }