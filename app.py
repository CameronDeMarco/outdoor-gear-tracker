from fastapi import FastAPI
from fastapi.responses import HTMLResponse

app = FastAPI()

@app.get("/", response_class=HTMLResponse)
def home():

    return """
    <h1>Outdoor Gear Tracker</h1>

    <form action="/search">
        <input name="product" placeholder="Search gear">
        <button type="submit">Search</button>
    </form>
    """

@app.get("/search")
def search(product: str):

    return {
        "product": product,
        "results": [
            {
                "store": "REI",
                "price": 249.99
            },
            {
                "store": "Backcountry",
                "price": 229.99
            }
        ]
    }