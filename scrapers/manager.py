"""Runs every registered scraper and aggregates their results.

To add a retailer, add an entry to STORES (for Shopify stores) or write a
dedicated ``scrape_<store>()`` function and call it in ``scrape_all()``.
"""

from concurrent.futures import ThreadPoolExecutor

from scrapers.shopify import scrape_shopify


# Real outdoor gear retailers that run on Shopify (public search endpoint, no
# bot-blocking). Add a line here to track another store.
#
# Multi-brand retailers carry mainstream brands (Osprey, Arc'teryx, Patagonia,
# etc.); brand-direct shops only sell their own gear.
STORES = [
    # Multi-brand retailers — broad brand and product coverage
    ("appoutdoors.com", "App Outdoors"),
    ("gearx.com", "Outdoor Gear Exchange"),
    ("omcgear.com", "OmcGear"),
    ("tahoemountainsports.com", "Tahoe Mountain Sports"),
    ("garagegrowngear.com", "Garage Grown Gear"),
    ("outdoorplay.com", "Outdoorplay"),
    ("featheredfriends.com", "Feathered Friends"),
    # Brand-direct shops — their own gear only
    ("hyperlitemountaingear.com", "Hyperlite Mountain Gear"),
    ("gossamergear.com", "Gossamer Gear"),
    ("seatosummit.com", "Sea to Summit"),
]


def scrape_all(query=None):
    """Search every registered store and aggregate the matches for ``query``.

    Stores are queried in parallel so the total time is roughly the slowest
    single store rather than the sum of all of them.
    """
    if not query:
        return []

    def scrape_one(store):
        domain, name = store
        try:
            return scrape_shopify(domain, name, query=query)
        except Exception as error:
            # A single failing store shouldn't take down the whole search.
            print(f"[warn] scrape failed for {name}: {error}")
            return []

    results = []
    with ThreadPoolExecutor(max_workers=len(STORES)) as pool:
        for store_results in pool.map(scrape_one, STORES):
            results.extend(store_results)

    return results
