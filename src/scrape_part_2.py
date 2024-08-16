import csv
import os

import requests
from bs4 import BeautifulSoup


class ProductScraper_part_2:
    def __init__(self, input_file_path, output_file_path):
        self.input_file_path = input_file_path
        self.output_file_path = output_file_path
        self.urls = []
        self.total_urls = 0

    def load_urls(self):
        """Load URLs from the input CSV file."""
        with open(self.input_file_path, mode='r', encoding='utf-8') as input_file:
            reader = csv.reader(input_file)
            self.urls = [row[0] for row in reader][1:]  # Skip the header and get all URLs
            self.total_urls = len(self.urls)

    def scrape_data(self, url):
        """Scrape the necessary data from a single product page."""
        response = requests.get(url)

        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')

            # Find the description (Description)
            description_div = soup.find('div', itemprop="description")
            description_text = description_div.get_text(strip=True) if description_div else "None"

            # Find the Text_1 (Usage/Применение)
            text_1_div = soup.find('div', value="Text_1", )
            text_1_text = text_1_div.get_text(strip=True) if text_1_div else "None"

            # Find the Text_4 (Additional Information/Дополнительная информация)
            text_4_div = None
            keywords = ['страна', 'производитель', 'изготовитель', 'происхождение', 'адрес']

            for value in ["Text_4", "Text_3", "Text_2"]:
                div = soup.find('div', value=value)
                if div and any(keyword in div.get_text(strip=True).lower() for keyword in keywords):
                    text_4_div = div
                    break

            text_4_text = text_4_div.get_text(strip=True) if text_4_div else "None"

            return [url, description_text, text_1_text, text_4_text]
        else:
            print(f"Failed to retrieve the webpage at {url}. Status code: {response.status_code}")
            return [url, "Failed to retrieve", "Failed to retrieve", "Failed to retrieve"]

    def write_output(self, data):
        """Write the scraped data to the output CSV file."""
        with open(self.output_file_path, mode='w', newline='', encoding='utf-8') as output_file:
            writer = csv.writer(output_file)
            writer.writerow(
                ["Product URL", "Description", "Usage", "Additional information - Manufacturer"])
            writer.writerows(data)

    def run(self):
        """Run the scraper through all URLs and save the results."""
        self.load_urls()
        all_data = []
        for index, url in enumerate(self.urls, start=1):
            data = self.scrape_data(url)
            all_data.append(data)
            print(f"Data successfully written for {index}/{self.total_urls} - {url}")
        self.write_output(all_data)
        print(f"All data successfully written to {self.output_file_path}")