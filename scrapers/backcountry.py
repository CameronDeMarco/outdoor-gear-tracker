from playwright.sync_api import sync_playwright


def scrape_backcountry(url):

    print("Backcountry scraper started")

    with sync_playwright() as p:

        browser = p.chromium.launch(
            headless=False
        )

        page = browser.new_page(
            user_agent=(
                "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                "AppleWebKit/537.36 "
                "Chrome/120 Safari/537.36"
            )
        )


        page.goto(
            url,
            wait_until="networkidle",
            timeout=60000
        )


        print("URL:")
        print(page.url)


        print("Title:")
        print(page.title())


        print(page.content()[:1000])


        browser.close()


    return {
        "store": "Backcountry",
        "product": "Unknown",
        "price": "Unknown"
    }