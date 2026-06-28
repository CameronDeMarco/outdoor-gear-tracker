from scrapers.books import scrape_books
from scrapers.outdoor import scrape_outdoor


def scrape_all():

    results = []

    results.append(
        scrape_books(
            "https://books.toscrape.com/"
        )
    )

    results.extend(
        scrape_outdoor()
    )

    return results