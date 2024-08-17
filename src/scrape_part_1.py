import csv
import os
import urllib.parse

import requests


class ProductScraper_part_1:
    """
    A class to scrape product data from a website across multiple pages and save the results to a CSV file.
    """

    def __init__(self, base_url, query_params, headers, output_dir, output_file_name):
        """
        Initialize the ProductScraper_part_1 with necessary parameters.

        Parameters:
        base_url (str): The base URL of the website to scrape.
        query_params (dict): The query parameters to append to the URL for each request.
        headers (dict): The headers to include in the request, such as User-Agent.
        output_dir (str): The directory where the output CSV file will be saved.
        output_file_name (str): The name of the output CSV file.
        """
        self.base_url = base_url
        self.query_params = query_params
        self.headers = headers
        self.output_dir = output_dir
        self.output_file_path = os.path.join(self.output_dir, output_file_name)
        self.fieldnames = ['Product URL', 'Product Name', 'Price (RUB)', 'Rating']
        self.seen_item_ids = set()

        # Ensure the output directory exists
        os.makedirs(self.output_dir, exist_ok=True)

    def fetch_page(self, page_number):
        """
        Fetch the data from a single page by making an HTTP GET request.

        Parameters:
        page_number (int): The page number to retrieve.

        Returns:
        list: A list of products from the retrieved page.
        """
        self.query_params["pageNumber"] = page_number
        encoded_params = urllib.parse.urlencode(self.query_params, doseq=True)
        full_url = f"{self.base_url}?{encoded_params}"

        response = requests.get(full_url, headers=self.headers)
        response.raise_for_status()  # Raise an HTTPError for bad responses

        return response.json().get('data', {}).get('products', [])

    def process_product(self, product):
        """
        Process a single product and return a dictionary of its data.

        Parameters:
        product (dict): A dictionary representing a single product's data.

        Returns:
        dict or None: A dictionary containing the product's URL, name, price, and rating,
                      or None if the product has already been processed.
        """
        item_id = product.get('itemId')
        if item_id in self.seen_item_ids:
            return None

        self.seen_item_ids.add(item_id)

        product_url = product.get('url', '')
        full_url = f"https://goldapple.ru{product_url}"
        brand = product.get('brand', '').strip()
        name = product.get('name', '').strip()
        full_name = f"{brand}: {name}"

        price = product.get('price', {}).get('actual', {}).get('amount')
        rating = product.get('reviews', {}).get('rating', None)

        return {
            'Product URL': full_url,
            'Product Name': full_name,
            'Price (RUB)': price,
            'Rating': rating if rating is not None else 'None'
        }

    def save_to_csv(self, products_data):
        """
        Save a list of product data dictionaries to a CSV file.

        Parameters:
        products_data (list): A list of dictionaries representing the product data.
        """
        with open(self.output_file_path, mode='w', newline='', encoding='utf-8') as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=self.fieldnames)
            writer.writeheader()
            for product_data in products_data:
                if product_data:
                    writer.writerow(product_data)

    def scrape(self, start_page=1, end_page=505):
        """
        Main method to scrape the products across multiple pages and save the results.

        Parameters:
        start_page (int): The starting page number (default is 1).
        end_page (int): The ending page number (default is 505).
        """
        all_products_data = []

        for page_number in range(start_page, end_page + 1):
            print(f"Processing page {page_number}...")

            try:
                products = self.fetch_page(page_number)

                for product in products:
                    product_data = self.process_product(product)
                    if product_data:
                        all_products_data.append(product_data)

            except requests.exceptions.HTTPError as http_err:
                print(f"HTTP error occurred on page {page_number}: {http_err}")
            except requests.exceptions.RequestException as req_err:
                print(f"Request error occurred on page {page_number}: {req_err}")

            # Optional: Uncomment the line below to add a delay between requests
            # time.sleep(1)

        self.save_to_csv(all_products_data)
        print("Processing complete.")
