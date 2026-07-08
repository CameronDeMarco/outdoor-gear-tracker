# Outdoor Gear Tracker

A price-comparison web app for outdoor gear. Search for a product and the app
scrapes multiple outdoor retailers, then returns the **best (lowest) available
price** along with a full comparison of every match.

Built with **FastAPI**, **SQLAlchemy**, and **requests** for scraping.

---

## Features

- 🏷️ **Best-price finder** — search a product, get the lowest in-stock price and where to buy it
- 📊 **Full comparison** — every matching listing across stores, cheapest first
- 🕸️ **Real scraping** — live products, prices, and stock from actual outdoor stores
- 🧩 **Pluggable scrapers** — adding a store is a one-line change
- 🔌 **JSON API** — the same result is available programmatically at `/api/search`
- 🗄️ **Persistence** — scraped products can be stored in SQLite via SQLAlchemy

---

## Tech Stack

| Layer      | Tooling                    |
| ---------- | -------------------------- |
| Web / API  | FastAPI, Uvicorn           |
| Scraping   | requests (Shopify feeds)   |
| Data       | SQLAlchemy ORM, SQLite     |

---

## How the scraper works

Outdoor retailers commonly run their storefronts on **Shopify**, which exposes a
public predictive-search endpoint at `/search/suggest.json`. `scrapers/shopify.py`
queries that endpoint per store and normalizes each match into
`{store, product, price, price_display, url, available}`. Searching server-side
(rather than downloading a whole catalog) is fast and works identically on small
brand-direct shops and large multi-brand retailers.

Stores are queried **in parallel** (one request each), so a search across all of
them takes about as long as the single slowest store (~0.5s), not the sum.

Stores currently tracked (all real):

- **Multi-brand retailers** — App Outdoors, Outdoor Gear Exchange, OmcGear, Tahoe
  Mountain Sports, Garage Grown Gear, Outdoorplay, Feathered Friends. Between them
  they carry mainstream brands (Osprey, Arc'teryx, Patagonia, Marmot, Columbia,
  Black Diamond…), so the same product can be compared across stores.
- **Brand-direct shops** — Hyperlite Mountain Gear, Gossamer Gear, Sea to Summit
  (their own gear only).

> **Design note:** big retailers like Amazon, REI, and Backcountry actively block
> scrapers (Backcountry serves an empty page to automated browsers). Rather than fight
> that, the tracker targets Shopify stores whose search endpoint is openly accessible —
> a more honest and maintainable foundation. Adding another store is a one-line change
> in `manager.py`.

---

## Project Structure

```
outdoor-gear-tracker/
├── app.py                    # FastAPI app: home page, /search (HTML), /api/search (JSON)
├── database.py               # SQLAlchemy engine + session factory
├── models.py                 # Product ORM model
├── create_db.py              # Creates the SQLite schema
├── scrapers/
│   ├── manager.py            # scrape_all() — runs every registered store, aggregates results
│   └── shopify.py            # generic scraper for Shopify-backed stores
├── services/
│   └── product_search.py     # search_product() + find_best_price()
└── requirements.txt
```

---

## Getting Started

**Requirements:** Python 3.9+ and an internet connection (searches scrape stores live).

```bash
git clone <your-repo-url>
cd outdoor-gear-tracker

python3 -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt

uvicorn app:app --reload
```

Open <http://127.0.0.1:8000> and search for a product. Specific product names work
best (e.g. `Osprey Atmos`, `Junction`, `UltaMid`, `Telos`); broad category words
(`tent`) return the cheapest matching item, which may be an accessory.

Two runnable demo scripts are included:

```bash
python demo_search.py       # print the best price for a sample query

python create_db.py         # create the SQLite schema
python demo_save_to_db.py   # scrape a query and save the results to the database
```

---

## API

`GET /api/search?product=<query>` returns the best price plus the full comparison:

```bash
curl "http://127.0.0.1:8000/api/search?product=osprey%20atmos"
```

```json
{
  "query": "osprey atmos",
  "best": {
    "store": "App Outdoors",
    "product": "Men's Atmos AG LT 65 Backpack",
    "price": 290.0,
    "price_display": "$290.00",
    "url": "https://appoutdoors.com/products/atmos-ag-lt-65",
    "available": true
  },
  "results": [
    {
      "store": "App Outdoors",
      "product": "Men's Atmos AG LT 65 Backpack",
      "price": 290.0,
      "price_display": "$290.00",
      "url": "https://appoutdoors.com/products/atmos-ag-lt-65",
      "available": true
    },
    {
      "store": "App Outdoors",
      "product": "Men's Atmos AG LT 50 Backpack",
      "price": 300.0,
      "price_display": "$300.00",
      "url": "https://appoutdoors.com/products/atmos-ag-lt-50",
      "available": true
    }
  ]
}
```

---

## How It Works

1. A request hits `/search` (HTML) or `/api/search` (JSON).
2. `services/product_search.py::find_best_price()` calls `scrapers/manager.py::scrape_all(query=...)`,
   which runs each store scraper and aggregates matches.
3. Matches are sorted so in-stock items rank first, then by ascending price — so the
   first result is the best price.
4. The best price is highlighted and the full comparison is returned.

Adding a new Shopify retailer is one line in `STORES` in `manager.py`:

```python
STORES = [
    ("appoutdoors.com", "App Outdoors"),
    ("gearx.com", "Outdoor Gear Exchange"),
    ("omcgear.com", "OmcGear"),
    # …seven more…
    # ("your-store.com", "Your Store"),
]
```

---

## Roadmap

- [ ] De-duplicate the *same* product across multi-brand retailers and rank by best price
- [ ] Cache scrape results in the database instead of scraping on every request
- [ ] Add more retailers (and non-Shopify stores via dedicated scrapers)
- [ ] Add automated tests (pytest) around the scrapers and search service
- [ ] Price history + drop alerts
