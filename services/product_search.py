"""Product search and best-price selection across all registered stores."""

from scrapers.manager import scrape_all


def search_product(product_name):
    """Return every matching product across stores, cheapest first.

    In-stock items are ranked ahead of out-of-stock ones, and within each
    group by ascending price.
    """
    print(f"Searching for: {product_name}")

    results = scrape_all(query=product_name)

    # Sort so the best (in-stock, lowest price) option comes first.
    results.sort(key=lambda item: (not item["available"], item["price"]))

    print(f"Found {len(results)} result(s)")
    return results


def find_best_price(product_name):
    """Return the single best (in-stock, lowest-price) match, or None.

    Returns a dict: ``{query, best, results}`` where ``best`` is the cheapest
    in-stock match (or the cheapest overall if none are in stock), and
    ``results`` is the full sorted comparison list.
    """
    results = search_product(product_name)

    best = results[0] if results else None

    return {
        "query": product_name,
        "best": best,
        "results": results,
    }
