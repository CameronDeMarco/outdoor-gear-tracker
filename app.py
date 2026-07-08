from fastapi import FastAPI, Query
from fastapi.responses import HTMLResponse, JSONResponse

from services.product_search import search_product


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


def render_results(product, results):
    if not results:
        return f'<p class="empty">No results found for "{product}".</p>'

    rows = "".join(
        f"<tr><td>{item.get('store', '')}</td>"
        f"<td>{item.get('product', item.get('title', ''))}</td>"
        f"<td>{item.get('price', '')}</td></tr>"
        for item in results
    )

    return f"""
        <h3>Results for "{product}"</h3>
        <table>
            <thead><tr><th>Store</th><th>Product</th><th>Price</th></tr></thead>
            <tbody>{rows}</tbody>
        </table>
    """


@app.get("/", response_class=HTMLResponse)
def home():
    return render_home()


@app.get("/search", response_class=HTMLResponse)
def search(product: str = Query(..., description="Product to search for")):
    results = search_product(product)
    return render_home(render_results(product, results))


@app.get("/api/search")
def api_search(product: str = Query(..., description="Product to search for")):
    """JSON API for the same search, for programmatic access."""
    return JSONResponse({
        "product": product,
        "results": search_product(product),
    })
