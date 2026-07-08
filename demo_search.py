from services.product_search import find_best_price


found = find_best_price("tent")

best = found["best"]
if best:
    print(f"Best price: {best['price_display']} — {best['product']} at {best['store']}")
else:
    print("No matches found")

print(f"\nAll {len(found['results'])} matches:")
for result in found["results"]:
    print(f"  {result['price_display']:>10}  {result['store']:26}  {result['product']}")
