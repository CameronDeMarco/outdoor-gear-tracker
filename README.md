# Outdoor Gear Tracker

A price-comparison web app for outdoor gear. Enter a product and the app scrapes
retailer listings, then returns matching products and their prices in one place.

Built with **FastAPI**, **SQLAlchemy**, and **BeautifulSoup / Playwright** for scraping.

---

## Features

- 🔎 **Search** for gear from a simple web UI and get results from multiple sources
- 🕸️ **Pluggable scrapers** — each retailer is an isolated module behind a common interface
- 🗄️ **Persistence** — scraped products are stored in SQLite via SQLAlchemy models
- 🔌 **JSON API** — the same search is available programmatically at `/api/search`

---

## Tech Stack

| Layer      | Tooling                                   |
| ---------- | ----------------------------------------- |
| Web / API  | FastAPI, Uvicorn                          |
| Scraping   | requests + BeautifulSoup, Playwright      |
| Data       | SQLAlchemy ORM, SQLite                    |

---

## Project Structure

```
outdoor-gear-tracker/
├── app.py                    # FastAPI app: home page, /search (HTML), /api/search (JSON)
├── database.py               # SQLAlchemy engine + session factory
├── models.py                 # Product ORM model
├── create_db.py              # Creates the SQLite schema
├── scrapers/                 # One module per source, plus a manager that runs them all
│   ├── manager.py            #   scrape_all() — aggregates every scraper
│   ├── books.py              #   demo scraper (books.toscrape.com)
│   ├── outdoor.py            #   demo scraper (books.toscrape.com)
│   └── backcountry.py        #   Playwright-based scraper (WIP)
├── services/
│   └── product_search.py     # search_product() — scrapes then filters by query
└── requirements.txt
```

> **Note:** `books.py` / `outdoor.py` currently scrape [books.toscrape.com](https://books.toscrape.com),
> a public sandbox built for practicing scraping. They act as stand-ins for real
> retailer scrapers while the scraping pipeline is being built out.

---

## Getting Started

### 1. Clone and set up a virtual environment

```bash
git clone <your-repo-url>
cd outdoor-gear-tracker

python3 -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate

pip install -r requirements.txt
playwright install chromium     # only needed for the Backcountry scraper
```

### 2. Create the database

```bash
python create_db.py
```

### 3. Run the app

```bash
uvicorn app:app --reload
```

Open <http://127.0.0.1:8000> and search for gear.

---

## API

`GET /api/search?product=<query>` returns JSON:

```bash
curl "http://127.0.0.1:8000/api/search?product=jacket"
```

```json
{
  "product": "jacket",
  "results": [
    { "store": "Outdoor Demo", "product": "A Light in the Attic", "price": "£51.77" }
  ]
}
```

---

## How It Works

1. A request hits `/search` (HTML) or `/api/search` (JSON).
2. `services/product_search.py` calls `scrapers/manager.py::scrape_all()`, which runs
   every registered scraper and aggregates the results.
3. Results are filtered against the search term and returned to the caller.
4. `test_scraper.py` demonstrates persisting scraped products to SQLite via the `Product` model.

Adding a new retailer is intentionally small: write a `scrape_<store>()` function that
returns `{"store", "product", "price"}` dicts, then register it in `manager.py`.

---

## Roadmap

- [ ] Finish the Playwright-based Backcountry scraper (parse title + price)
- [ ] Swap the demo scrapers for real outdoor retailers (REI, Backcountry, etc.)
- [ ] Cache scrape results in the database instead of scraping on every request
- [ ] Add automated tests (pytest) around scrapers and the search service
- [ ] Price history + drop alerts

---

## Testing / Scripts

Handy scripts used during development:

```bash
python test_search.py       # run a search end to end
python test_scraper.py      # scrape and persist to the database
python test_backcountry.py  # exercise the Playwright scraper
```
