import re
import time
import json
import os

from playwright.sync_api import Playwright, sync_playwright, expect
from bs4 import BeautifulSoup


categories = [
    "lajm",
    "teens",
    "novye-brendy",
    "videokonsul-tacija",
    "makijazh",
    "uhod",
    "volosy",
    "parfjumerija",
    "aptechnaja-kosmetika",
    "sexual-wellness",
    "azija",
    "organika",
    "dlja-muzhchin",
    "detjam",
    "tehnika",
    "dlja-doma",
    "uborki-i-gigiena",
    "odezhda-i-aksessuary",
    "figura-mechty",
    "ukrashenija",
    "mini-formaty",
    "tovary-dlja-zhivotnyh",
]


def save_html_to_json(page, filename="website_content.json"):
    html_content = page.content()  # Get the HTML content of the page
    data = {"html": html_content}  # Create a dictionary with the HTML content

    # Save the data to a JSON file
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
    print(f"HTML content saved to {filename}")


def append_html_to_json(page, filename="website_content.json"):
    html_content = page.content()  # Get the HTML content of the page

    # Check if the file exists
    if os.path.exists(filename):
        # Read the existing data
        with open(filename, "r", encoding="utf-8") as f:
            data = json.load(f)
    else:
        data = {"html": []}  # Initialize with an empty list if file does not exist

    # Append the new HTML content
    data["html"].append(html_content)

    # Save the updated data back to the JSON file
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
    print(f"HTML content appended to {filename}")


def run(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    page.goto("https://goldapple.ru/")
    page.get_by_role("button", name="Да, верно").click()
    page.keyboard.press("Escape")
    page.goto("https://goldapple.ru/tovary-dlja-zhivotnyh")


    for x in range(1, 50):
        if page.locator(".lKfCK > button").first.click():
            page.locator(".lKfCK > button").first.click()
            print("Clicked")
        page.keyboard.press("End")
        print(f"Scrolling... (Scroll count: {x})")
        time.sleep(1)

        # Append the HTML content to the JSON file after each iteration
        append_html_to_json(page)

    for x in range(1, 50):
        if page.locator(".lKfCK > button").first.click():
            page.locator(".lKfCK > button").first.click()
            print("Clicked")
        page.keyboard.press("End")
        print(f"Scrolling... (Scroll count: {x})")
        time.sleep(1)
        save_html_to_json(page)

    # page.inner_html('')

    # ---------------------
    context.close()
    browser.close()


with sync_playwright() as playwright:
    run(playwright)
