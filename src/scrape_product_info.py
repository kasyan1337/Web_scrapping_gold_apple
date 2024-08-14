import csv
import time
import os
from bs4 import BeautifulSoup
from playwright.sync_api import Playwright, sync_playwright

# Product URLs
products = [
    "https://goldapple.ru/19000188196-paradis-nuit",
    "https://goldapple.ru/19760331092-izia-la-nuit"
]

def extract_product_info(page):
    # Wait for the necessary content to load
    page.wait_for_selector('div.Waa6J')

    # Get the HTML content of the product page
    html_content = page.content()
    soup = BeautifulSoup(html_content, 'html.parser')

    # Extract the necessary data
    product_info = {}

    # 1. Ссылка на продукт (URL)
    product_info['URL'] = page.url

    # 2. Наименование (Product Name)
    product_name = soup.find('div', class_='Waa6J')
    product_info['Product Name'] = product_name.get_text(strip=True) if product_name else 'N/A'

    # 3. Цена (Price)
    price = soup.find('meta', itemprop='price')
    product_info['Price'] = price['content'] if price else 'N/A'

    # 5. Описание продукта (Product Description)
    description = soup.find('div', class_='CY6YP', itemprop='description')
    product_info['Product Description'] = description.get_text(strip=True) if description else 'N/A'

    # 6. Инструкция по применению (Usage Instructions)
    usage_instructions = soup.find_all('div', class_='CY6YP')
    if len(usage_instructions) > 1:
        product_info['Usage Instructions'] = usage_instructions[1].get_text(strip=True)
    else:
        product_info['Usage Instructions'] = 'N/A'

    # 7. Страна-производитель (Country of Origin)
    country_origin = None
    additional_info = soup.find('div', string="Дополнительная информация")
    if additional_info:
        country_origin = additional_info.find('div', class_='CY6YP')
    product_info['Country of Origin'] = country_origin.get_text(strip=True) if country_origin else 'N/A'

    return product_info

def save_to_csv(data, filename="product_info.csv"):
    # Ensure the filename includes a path
    if not os.path.dirname(filename):
        filename = os.path.join(os.getcwd(), filename)

    # Define the header based on the keys of the first item in data
    header = data[0].keys() if data else []

    # Write data to CSV
    with open(filename, "w", newline="", encoding="utf-8") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=header)
        writer.writeheader()
        writer.writerows(data)
    print(f"Data saved to {filename}")

def run(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context(permissions=[])
    page = context.new_page()

    product_data = []


    # Route to abort requests for images
    context.route("**/*",
                  lambda route, request: route.abort() if request.resource_type == "image" else route.continue_())

    page = context.new_page()
    page.goto("https://goldapple.ru/parfjumerija")
    page.get_by_role("button", name="Да, верно").click()
    page.keyboard.press("Escape")

    try:
        for product_url in products:
            page.goto(product_url)
            page.wait_for_timeout(3000)  # Wait for the page to load

            # Extract product information
            product_info = extract_product_info(page)
            product_data.append(product_info)
            print(f"Extracted data for {product_info['Product Name']}")

    except Exception as e:
        print(f"An error occurred: {e}")

    finally:
        # Save all collected data to a CSV file
        save_to_csv(product_data)

        # Clean up
        context.close()
        browser.close()

with sync_playwright() as playwright:
    run(playwright)