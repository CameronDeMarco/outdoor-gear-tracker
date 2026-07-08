"""Generic scraper for Shopify-powered outdoor gear stores.

Shopify stores expose a public predictive-search endpoint at
``/search/suggest.json`` that takes a query and returns matching products
(title, price, availability, handle) as JSON. Searching server-side is far
more efficient than downloading and filtering a store's whole catalog, and it
works the same on small brand-direct shops and large multi-brand retailers.
This is reliable and needs no headless browser or bot-protection workarounds.
"""

import requests


HEADERS = {
    "User-Agent": "Mozilla/5.0 (compatible; OutdoorGearTracker/1.0)"
}

# Shopify caps predictive search at 10 product results per request.
RESULT_LIMIT = 10


def scrape_shopify(domain, store_name=None, query=None):
    """Search a Shopify store for ``query`` and return normalized results.

    Returns a list of dicts:
    ``{store, product, price, price_display, url, available}`` where ``price``
    is a float (for comparison) and ``price_display`` is a "$xx.xx" string.
    Returns an empty list when no query is given (the endpoint is search-only).
    """
    store_name = store_name or domain
    if not query:
        return []

    response = requests.get(
        f"https://{domain}/search/suggest.json",
        params={
            "q": query,
            "resources[type]": "product",
            "resources[limit]": RESULT_LIMIT,
        },
        headers=HEADERS,
        timeout=15,
    )
    response.raise_for_status()

    products = (
        response.json()
        .get("resources", {})
        .get("results", {})
        .get("products", [])
    )

    results = []
    for product in products:
        # "price" is the lowest variant price (in the store's currency units).
        try:
            price = float(product["price"])
        except (KeyError, TypeError, ValueError):
            continue

        results.append({
            "store": store_name,
            "product": product["title"],
            "price": price,
            "price_display": f"${price:,.2f}",
            "url": f"https://{domain}/products/{product['handle']}",
            "available": bool(product.get("available")),
        })

    return results
