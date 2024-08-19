import csv
import json
import os

import pytest

from src.scrape_part_1 import ProductScraper_part_1


@pytest.fixture
def setup_test_environment():
    """Setup test environment with necessary files and directories."""
    base_url = "https://goldapple.ru/front/api/catalog/products"
    query_params = {
        "categoryId": "1000000007",
        "cityId": "0c5b2444-70a0-4932-980c-b4dc0d3f02b5",
        "geoPolygons[]": [
            "EKB-000000360",
            "EKB-000000367",
            "EKB-000000347",
            "EKB-000000356",
        ],
    }

    # Request headers
    headers = {
        "Accept": "application/json, text/plain, */*",
        "Sec-Fetch-Site": "same-origin",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "en-US,en;q=0.9",
        "Sec-Fetch-Mode": "cors",
        "Host": "goldapple.ru",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.5 Safari/605.1.15",
        "Connection": "keep-alive",
        "Sec-Fetch-Dest": "empty",
        "Cookie": "_ga_QE5MQ8XJJK=GS1.1.1723635506.16.1.1723635540.0.0.0; tmr_detect=0%7C1723635510869; _ym_visorc=b; _ym_isad=1; tmr_lvid=fdaef488e743b23b37f6c9f4bee62c2a; tmr_lvidTS=1723102720410; MCS_SESSID=ad61c82f984e6a594eb0ee7edf6d65bd; section_data_ids=%7B%22cart%22%3A1723635506%2C%22adult_goods%22%3A1723635507%2C%22geolocation%22%3A1723635506%7D; _ga=GA1.2.800260019.1723102720; _gcl_au=1.1.2081473348.1723102720; _gid=GA1.2.1529193665.1723552270; advcake_track_url=%3D20240812pxHIjmPQ3Ptllo7rEUiJN%2Bj4rlmZshbzvBKApykL%2FmQPGC0H%2BGuIjkRD0MxagOAdGMCc%2BXqcrBOZMrnQ4wE3wQ5gSUuEylWZ%2FQWoLUZV36vfW1hoED%2FsoXeG4depCIqW8QVs5KUW8tF6infqGNOE8DjwQWXbe1GADtPlK3q3qaun2o863UwS%2F5WMq7ZjISFvgxw0vR2y%2FYVpFO13YM%2BQDuxes710PjtXkJNtCnBMMjRdk8gOYDWSHA0CJVkn%2FHpgFunSlHw3qbHD55hdHi06QssG0fbbzEj%2BNY3khKCJjrdbh3T8l%2Fso0kqgzJ%2BiBxbQ0dSOdLc8qC8l41kSZQVny3WdWFKTDHN%2FHUxQSrqmBsUHu7GiBDTbRLshZG0B9MNJZiSVbC5Z%2BfohZB4nJ2sIq6jT6ve7OT1gpBoMVwE%2B4bMuLPZ5bUAFh3nhts%2BojF3Ai4G0VuWX9YCYm7PyDrCaVD6%2BdIn46eV%2F6rLg%2B3zsztQMNb3m9PdVI5j8XX7YDuzCFywrCyY2bgb2KZgtxLtOT4d0Wv0RDgQpCKy3ZW47WJ9vfKdnVlchEnpDBO3A8%2FvfLsIswuJzRADcsgcD%2BiP8VeWqMMmHxYD8V7ch9lm6Jzqpy9aAVTvCUobCJ%2FGFByxbpr6%2BAh5c579zP5WkYERUY4Z6%2BlrXVU9oZaoMC6CUtzkyiMZrH%2B1QoGU%3D; digi-analytics-sessionId=O8ZWE2rkcAYV_fJJTA9SN; client-store-code=default; ga-lang=ru; ngenix_jscv_2198e54375cc=bot_profile_check=true&cookie_signature=FH8z0S891eY9Yhfp2WGKeNEnjRo%3D&cookie_expires=1723639103; isAddressConfirmed=true; domain_sid=9JU1lbYZMOeAacVbpiuWQ%3A1723552271212; _ym_d=1723102720; _ym_uid=1723102720830207345; advcake_session_id=25976154-7d16-78a9-b91a-e2c7e8c8d0db; advcake_track_id=68c0abf5-4d5f-c45e-41ae-fde176ab2af1; directCrm-session=%7B%22deviceGuid%22%3A%22eeea756f-7b83-49b2-a06b-42668ad32380%22%7D; mindboxDeviceUUID=eeea756f-7b83-49b2-a06b-42668ad32380; ga-device-id=WacqeEOwc9CmIeDzjfOGy; ga-lang=ru",
        "traceparent": "00-8bf61a32784d488d4d62873dd858db97-0844072404707339-01",
        "x-app-version": "1.47.0",
        "x-gast": "36923682.452567786,36923682.452567786",
    }

    # FIRST PART
    data_dir = "./mock_data"
    part1_filename = "part_1_test_output.csv"
    return ProductScraper_part_1(
        base_url, query_params, headers, data_dir, part1_filename
    )


def test_fetch_page(setup_test_environment):
    products = setup_test_environment.fetch_page(1)
    assert isinstance(products, list), "Fetched data should be a list"
    assert "itemId" in products[0], "Product data should contain 'itemId'"


def test_process_product(setup_test_environment):
    with open("./mock_data/product_1.json") as f:
        product = json.load(f)
    processed_product = setup_test_environment.process_product(product)
    assert processed_product is not None, "Processed product should not be None"
    assert (
        "Product URL" in processed_product
    ), "Processed product should contain 'Product URL'"
    assert (
        "Product Name" in processed_product
    ), "Processed product should contain 'Product Name'"
    assert (
        "Price (RUB)" in processed_product
    ), "Processed product should contain 'Price (RUB)'"
    assert "Rating" in processed_product, "Processed product should contain 'Rating'"


def test_save_to_csv(setup_test_environment):
    scraper = setup_test_environment

    with open("./mock_data/page_1.json") as f:
        page_data = json.load(f)

    # Extract the list of products from the page data
    products = page_data["data"]["products"]

    # Extract the 4 fields needed for the CSV
    extracted_data = []
    for product in products:
        product_info = {
            "Product URL": f"https://goldapple.ru{product['url']}",
            "Product Name": f"{product.get('brand', 'Unknown Brand')}: {product.get('name', 'Unknown Name')}",
            "Price (RUB)": product["price"]["actual"]["amount"],
            # Using .get() to avoid KeyError if 'reviews' is not there
            "Rating": product.get("reviews", {}).get("rating", "None"),
        }
        extracted_data.append(product_info)

    # Pass the extracted data to save_to_csv
    scraper.save_to_csv(extracted_data)

    assert os.path.exists(scraper.output_file_path), "CSV file should be created"

    with open(scraper.output_file_path, mode="r", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        rows = list(reader)
        assert len(rows) == 24, "Should be 24 products on the page"


def test_scrape(monkeypatch, setup_test_environment):
    scraper = setup_test_environment

    def mock_fetch_page(page_number):
        page_number = 1
        return [
            {
                "url": f"/19000125769",
                "brand": "BASTILLE",
                "name": f"Demain Promis",
                "price": {"actual": {"amount": 1000}},
                "reviews": {"rating": 5},
            }
        ]

    def mock_save_to_csv(data):
        assert len(data) == 1
        assert data[0]["Product Name"] == "BASTILLE: Demain Promis"
        assert data[0]["Product URL"] == "https://goldapple.ru/19000125769"
        assert data[0]["Price (RUB)"] == 1000
        assert data[0]["Rating"] == 5

    monkeypatch.setattr(scraper, "fetch_page", mock_fetch_page)
    monkeypatch.setattr(scraper, "save_to_csv", mock_save_to_csv)

    scraper.scrape(1, 1)
