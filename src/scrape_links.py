import json
import os
import time

from bs4 import BeautifulSoup
from playwright.sync_api import Playwright, sync_playwright


def append_href_to_json(page, href_set):
    html_content = page.content()  # Get the HTML content of the page
    soup = BeautifulSoup(html_content, 'html.parser')  # Parse the HTML with BeautifulSoup

    # Extract all <article> tags with a class
    articles = soup.find_all('article', class_=True)

    # Loop through each article and extract the href of the first <a> tag
    for article in articles:
        a_tag = article.find('a', href=True)  # Find the first <a> tag with an href within the article
        if a_tag and a_tag['href']:
            href_set.add(a_tag['href'])  # Add only the href value to the set

    print(f"Unique hrefs collected so far: {len(href_set)}")


def save_hrefs_to_json(href_set, filename="data/product_links/href_links.json"):
    data = {"hrefs": list(href_set)}  # Convert set to list for saving

    # Save the unique hrefs to the JSON file
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
    print(f"All unique href links saved to {filename}")


def run(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context(permissions=[])

    # Route to abort requests for images
    context.route("**/*",
                  lambda route, request: route.abort() if request.resource_type == "image" else route.continue_())

    page = context.new_page()
    page.goto("https://goldapple.ru/parfjumerija")
    page.get_by_role("button", name="Да, верно").click()
    page.keyboard.press("Escape")
    page.goto("https://goldapple.ru/tovary-dlja-zhivotnyh")  # test page
    # page.goto("https://goldapple.ru/parfjumerija")

    href_set = set()  # Initialize an empty set to store unique hrefs

    try:
        for x in range(1, 1000):
            if page.locator(".lKfCK > button").first.click():
                page.locator(".lKfCK > button").first.click()
                print("Clicked")
            page.keyboard.press("End")
            print(f"Scrolling... (Scroll count: {x})")
            time.sleep(1)

            # Append the unique hrefs to the set after each iteration
            append_href_to_json(page, href_set)

    except Exception as e:
        print(e)

    finally:
        # Save all unique hrefs to a single JSON file, regardless of success or failure
        save_hrefs_to_json(href_set)

    # ---------------------
    context.close()
    browser.close()


with sync_playwright() as playwright:
    run(playwright)
