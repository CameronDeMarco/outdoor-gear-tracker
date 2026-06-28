from scrapers.manager import scrape_all


def search_product(product_name):

    print(f"Searching for: {product_name}")


    results = scrape_all()


    matches = []


    for item in results:

        if product_name.lower() in str(item).lower():

            matches.append(item)


    return matches