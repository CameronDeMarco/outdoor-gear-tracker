from scrapers.manager import scrape_all

from database import SessionLocal

from models import Product



print("Starting test...")


results = scrape_all()


db = SessionLocal()


for item in results:


    product = Product(

        store=item["store"],

        product=item.get(
            "product",
            item.get("title")
        ),

        price=item["price"]

    )


    db.add(product)



db.commit()


print("Saved to database!")


db.close()