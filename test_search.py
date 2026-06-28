from services.product_search import search_product


results = search_product(
    "A Light"
)


for result in results:
    print(result)