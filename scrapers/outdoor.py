import requests
from bs4 import BeautifulSoup


def scrape_outdoor():

    print("Outdoor scraper started")

    url = "https://books.toscrape.com/"

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

    products = soup.find_all(
        "article",
        class_="product_pod"
    )

    results = []

    for product in products[:5]:

        title = product.h3.a["title"]

        price = product.find(
            "p",
            class_="price_color"
        ).text

        results.append(
            {
                "store": "Outdoor Demo",
                "product": title,
                "price": price
            }
        )

    return results