import json
import time
import os
from bs4 import BeautifulSoup


# Function to extract href links immediately following <article class> and save to JSON
def append_href_to_json(page, filename="href_links.json"):
    html_content = page.content()  # Get the HTML content of the page
    soup = BeautifulSoup(html_content, 'html.parser')  # Parse the HTML with BeautifulSoup

    # Extract all <article> tags with a class
    articles = soup.find_all('article', class_=True)

    # Initialize a list to hold the hrefs found in this iteration
    hrefs = []

    # Loop through each article and extract the href of the first <a> tag
    for article in articles:
        a_tag = article.find('a', href=True)  # Find the first <a> tag with an href within the article
        if a_tag and a_tag['href']:
            hrefs.append(a_tag['href'])  # Add only the href value to the list

    # Check if the file exists
    if os.path.exists(filename):
        # Read the existing data
        with open(filename, "r", encoding="utf-8") as f:
            data = json.load(f)
    else:
        data = {"hrefs": []}  # Initialize with an empty list if the file does not exist

    # Append the new hrefs
    data["hrefs"].extend(hrefs)

    # Save the updated data back to the JSON file
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
    print(f"Href links appended to {filename}")


# Your original loop
for x in range(1, 50):
    if page.locator(".lKfCK > button").first.click():
        page.locator(".lKfCK > button").first.click()
        print("Clicked")
    page.keyboard.press("End")
    print(f"Scrolling... (Scroll count: {x})")
    time.sleep(1)

    # Append the href links to the JSON file after each iteration
    append_href_to_json(page)