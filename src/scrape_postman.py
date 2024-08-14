import requests
import os
import csv
import urllib.parse
import time

# Base URL parts
base_url = "https://goldapple.ru/front/api/catalog/products"
query_params = {
    "categoryId": "1000000007",
    "cityId": "0c5b2444-70a0-4932-980c-b4dc0d3f02b5",
    "geoPolygons[]": [
        "EKB-000000360",
        "EKB-000000367",
        "EKB-000000347",
        "EKB-000000356"
    ]
}
# Request headers from Postman, do not touch
headers = {
    'Accept': 'application/json, text/plain, */*',
    'Sec-Fetch-Site': 'same-origin',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'en-US,en;q=0.9',
    'Sec-Fetch-Mode': 'cors',
    'Host': 'goldapple.ru',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.5 Safari/605.1.15',
    'Connection': 'keep-alive',
    'Sec-Fetch-Dest': 'empty',
    'Cookie': '_ga_QE5MQ8XJJK=GS1.1.1723635506.16.1.1723635540.0.0.0; tmr_detect=0%7C1723635510869; _ym_visorc=b; _ym_isad=1; tmr_lvid=fdaef488e743b23b37f6c9f4bee62c2a; tmr_lvidTS=1723102720410; MCS_SESSID=ad61c82f984e6a594eb0ee7edf6d65bd; section_data_ids=%7B%22cart%22%3A1723635506%2C%22adult_goods%22%3A1723635507%2C%22geolocation%22%3A1723635506%7D; _ga=GA1.2.800260019.1723102720; _gcl_au=1.1.2081473348.1723102720; _gid=GA1.2.1529193665.1723552270; advcake_track_url=%3D20240812pxHIjmPQ3Ptllo7rEUiJN%2Bj4rlmZshbzvBKApykL%2FmQPGC0H%2BGuIjkRD0MxagOAdGMCc%2BXqcrBOZMrnQ4wE3wQ5gSUuEylWZ%2FQWoLUZV36vfW1hoED%2FsoXeG4depCIqW8QVs5KUW8tF6infqGNOE8DjwQWXbe1GADtPlK3q3qaun2o863UwS%2F5WMq7ZjISFvgxw0vR2y%2FYVpFO13YM%2BQDuxes710PjtXkJNtCnBMMjRdk8gOYDWSHA0CJVkn%2FHpgFunSlHw3qbHD55hdHi06QssG0fbbzEj%2BNY3khKCJjrdbh3T8l%2Fso0kqgzJ%2BiBxbQ0dSOdLc8qC8l41kSZQVny3WdWFKTDHN%2FHUxQSrqmBsUHu7GiBDTbRLshZG0B9MNJZiSVbC5Z%2BfohZB4nJ2sIq6jT6ve7OT1gpBoMVwE%2B4bMuLPZ5bUAFh3nhts%2BojF3Ai4G0VuWX9YCYm7PyDrCaVD6%2BdIn46eV%2F6rLg%2B3zsztQMNb3m9PdVI5j8XX7YDuzCFywrCyY2bgb2KZgtxLtOT4d0Wv0RDgQpCKy3ZW47WJ9vfKdnVlchEnpDBO3A8%2FvfLsIswuJzRADcsgcD%2BiP8VeWqMMmHxYD8V7ch9lm6Jzqpy9aAVTvCUobCJ%2FGFByxbpr6%2BAh5c579zP5WkYERUY4Z6%2BlrXVU9oZaoMC6CUtzkyiMZrH%2B1QoGU%3D; digi-analytics-sessionId=O8ZWE2rkcAYV_fJJTA9SN; client-store-code=default; ga-lang=ru; ngenix_jscv_2198e54375cc=bot_profile_check=true&cookie_signature=FH8z0S891eY9Yhfp2WGKeNEnjRo%3D&cookie_expires=1723639103; isAddressConfirmed=true; domain_sid=9JU1lbYZMOeAacVbpiuWQ%3A1723552271212; _ym_d=1723102720; _ym_uid=1723102720830207345; advcake_session_id=25976154-7d16-78a9-b91a-e2c7e8c8d0db; advcake_track_id=68c0abf5-4d5f-c45e-41ae-fde176ab2af1; directCrm-session=%7B%22deviceGuid%22%3A%22eeea756f-7b83-49b2-a06b-42668ad32380%22%7D; mindboxDeviceUUID=eeea756f-7b83-49b2-a06b-42668ad32380; ga-device-id=WacqeEOwc9CmIeDzjfOGy; ga-lang=ru',
    'traceparent': '00-8bf61a32784d488d4d62873dd858db97-0844072404707339-01',
    'x-app-version': '1.47.0',
    'x-gast': '36923682.452567786,36923682.452567786'
}

# Create directory if it doesn't exist
output_dir = '../data'
os.makedirs(output_dir, exist_ok=True)

# Initialize the CSV file
csv_file_path = os.path.join(output_dir, 'postman_product_info.csv')
fieldnames = ['Product URL', 'Product Name', 'Price (RUB)', 'Rating']

with open(csv_file_path, mode='w', newline='', encoding='utf-8') as csv_file:
    writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
    writer.writeheader()

    seen_item_ids = set()

    # Loop through the pages; should be 504 pages in total; since there is 24 products/page and 120965 products in total
    for page_number in range(1, 505):
        print(f"Processing page {page_number}...")

        try:
            # Add the page number to the query parameters in the URL
            query_params["pageNumber"] = page_number

            # Properly encode the query parameters
            encoded_params = urllib.parse.urlencode(query_params, doseq=True)

            # Create the full URL with the encoded query parameters
            full_url = f"{base_url}?{encoded_params}"

            response = requests.get(full_url, headers=headers)
            response.raise_for_status()  # Raise an HTTPError for bad responses (4xx and 5xx)

            products = response.json().get('data', {}).get('products', [])

            for product in products:
                item_id = product.get('itemId')
                if item_id in seen_item_ids:
                    continue

                seen_item_ids.add(item_id)

                product_url = product.get('url', '')
                full_url = f"https://goldapple.ru{product_url}"
                brand = product.get('brand', '').strip()
                name = product.get('name', '').strip()
                full_name = f"{brand}: {name}"

                price = product.get('price', {}).get('actual', {}).get('amount')
                rating = product.get('reviews', {}).get('rating', None)

                writer.writerow({
                    'Product URL': full_url,
                    'Product Name': full_name,
                    'Price (RUB)': price,
                    'Rating': rating if rating is not None else 'None'
                })

        except requests.exceptions.HTTPError as http_err:
            print(f"HTTP error occurred on page {page_number}: {http_err}")
        except requests.exceptions.RequestException as req_err:
            print(f"Request error occurred on page {page_number}: {req_err}")

        # time.sleep(1)  # Add a 1-second delay if http error occurs; too many requests

print("Processing complete.")