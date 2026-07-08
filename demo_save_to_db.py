from scrapers.manager import scrape_all
from database import SessionLocal
from models import Product


query = "osprey atmos"
print(f"Scraping '{query}' and saving results to the database...")

results = scrape_all(query=query)

db = SessionLocal()

for item in results:
    product = Product(
        store=item["store"],
        product=item["product"],
        price=item["price_display"],
    )
    db.add(product)

db.commit()

print(f"Saved {len(results)} products to database!")

db.close()
