from fastapi import FastAPI, Query
from fastapi.responses import HTMLResponse, JSONResponse

from services.product_search import find_best_price


app = FastAPI(title="Outdoor Gear Tracker")


PAGE_STYLE = """
<style>
    body {
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
        max-width: 720px;
        margin: 60px auto;
        padding: 0 20px;
        color: #1a1a1a;
    }
    h1 { margin-bottom: 4px; }
    .subtitle { color: #666; margin-top: 0; }
    form { margin: 24px 0; display: flex; gap: 8px; }
    input {
        flex: 1;
        padding: 10px 12px;
        font-size: 16px;
        border: 1px solid #ccc;
        border-radius: 6px;
    }
    button {
        padding: 10px 18px;
        font-size: 16px;
        background: #2e7d32;
        color: white;
        border: none;
        border-radius: 6px;
        cursor: pointer;
    }
    button:hover { background: #256628; }
    table { width: 100%; border-collapse: collapse; margin-top: 16px; }
    th, td { text-align: left; padding: 10px; border-bottom: 1px solid #eee; }
    th { color: #666; font-weight: 600; }
    .empty { color: #999; margin-top: 24px; }
    .best {
        margin-top: 24px;
        padding: 16px 20px;
        background: #f1f8f2;
        border: 1px solid #cfe8d4;
        border-radius: 8px;
    }
    .best .label { font-size: 13px; color: #2e7d32; font-weight: 600; text-transform: uppercase; letter-spacing: .04em; }
    .best .price { font-size: 28px; font-weight: 700; color: #1b5e20; }
    .best .where { color: #444; }
    .best a { color: #2e7d32; }
    .muted { color: #999; }
</style>
"""


def render_home(results_html=""):
    return f"""
    <html>
    <head><title>Outdoor Gear Tracker</title>{PAGE_STYLE}</head>
    <body>
        <h1>Outdoor Gear Tracker</h1>
        <p class="subtitle">Compare outdoor gear prices across retailers.</p>

        <form action="/search" method="get">
            <input name="product" placeholder="Search gear (e.g. jacket, tent)" required>
            <button type="submit">Search</button>
        </form>

        {results_html}
    </body>
    </html>
    """


def _stock(item):
    return "In stock" if item["available"] else '<span class="muted">Out of stock</span>'


def render_results(product, best, results):
    if not results:
        return f'<p class="empty">No results found for "{product}".</p>'

    best_where = (
        f'<a href="{best["url"]}" target="_blank">{best["product"]}</a> '
        f'at {best["store"]}'
    )
    best_html = f"""
        <div class="best">
            <div class="label">Best price for "{product}"</div>
            <div class="price">{best["price_display"]}</div>
            <div class="where">{best_where}</div>
        </div>
    """

    rows = "".join(
        f'<tr><td>{item["store"]}</td>'
        f'<td><a href="{item["url"]}" target="_blank">{item["product"]}</a></td>'
        f'<td>{item["price_display"]}</td>'
        f'<td>{_stock(item)}</td></tr>'
        for item in results
    )

    table_html = f"""
        <h3>All {len(results)} matches (cheapest first)</h3>
        <table>
            <thead><tr><th>Store</th><th>Product</th><th>Price</th><th>Stock</th></tr></thead>
            <tbody>{rows}</tbody>
        </table>
    """

    return best_html + table_html


@app.get("/", response_class=HTMLResponse)
def home():
    return render_home()


@app.get("/search", response_class=HTMLResponse)
def search(product: str = Query(..., description="Product to search for")):
    found = find_best_price(product)
    return render_home(render_results(product, found["best"], found["results"]))


@app.get("/api/search")
def api_search(product: str = Query(..., description="Product to search for")):
    """JSON API: returns the best price plus the full comparison list."""
    return JSONResponse(find_best_price(product))
