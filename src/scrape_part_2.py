import time
import requests
from bs4 import BeautifulSoup
import csv


class ProductScraper_part_2:
    """
    A class to scrape detailed product information from individual product pages and save the results to a CSV file.
    """

    def __init__(self, input_file_path, output_file_path):
        """
        Initialize the ProductScraper_part_2 with the input and output file paths.

        Parameters:
        input_file_path (str): The path to the input CSV file containing product URLs.
        output_file_path (str): The path to the output CSV file where scraped data will be saved.
        """
        self.input_file_path = input_file_path
        self.output_file_path = output_file_path
        self.urls = []
        self.total_urls = 0

    def load_urls(self):
        """
        Load URLs from the input CSV file.
        """
        with open(self.input_file_path, mode="r", encoding="utf-8") as input_file:
            reader = csv.reader(input_file)
            self.urls = [row[0] for row in reader][
                1:
            ]  # Skip the header and get all URLs
            self.total_urls = len(self.urls)

    def scrape_data(self, url, retries=10, delay=1):
        """
        Scrape the necessary data from a single product page, with retry logic.

        Parameters:
        url (str): The product URL to scrape.
        retries (int): The number of retry attempts in case of a request failure (default is 10).
        delay (int): The delay between retry attempts in seconds (default is 1).

        Returns:
        list: A list containing the product URL, description, usage, and additional information.
        """
        for attempt in range(retries):
            try:
                response = requests.get(url)
                response.raise_for_status()  # Raise an HTTPError for bad responses (4xx and 5xx)

                soup = BeautifulSoup(response.text, "html.parser")

                # Find the description (Description)
                description_div = soup.find("div", itemprop="description")
                description_text = (
                    description_div.get_text(strip=True) if description_div else "None"
                )

                # Find the Text_1 (Usage/Применение)
                text_1_div = soup.find("div", value="Text_1")
                text_1_text = text_1_div.get_text(strip=True) if text_1_div else "None"

                # Find the Text_4 (Additional Information/Дополнительная информация)
                text_4_div = None
                keywords = [
                    "страна",
                    "производитель",
                    "изготовитель",
                    "происхождение",
                    "адрес",
                ]

                for value in ["Text_4", "Text_3", "Text_2"]:
                    div = soup.find("div", value=value)
                    if div and any(
                        keyword in div.get_text(strip=True).lower()
                        for keyword in keywords
                    ):
                        text_4_div = div
                        break

                text_4_text = text_4_div.get_text(strip=True) if text_4_div else "None"

                return [url, description_text, text_1_text, text_4_text]

            except requests.exceptions.RequestException as e:
                print(f"Attempt {attempt + 1} failed for {url}: {e}")
                if attempt < retries - 1:
                    print(f"Retrying in {delay} second...")
                    time.sleep(delay)
                else:
                    print(
                        f"Failed to retrieve the webpage at {url} after {retries} attempts."
                    )
                    return [
                        url,
                        "Failed to retrieve",
                        "Failed to retrieve",
                        "Failed to retrieve",
                    ]

    def write_output(self, data):
        """
        Write the scraped data to the output CSV file.

        Parameters:
        data (list): A list of lists, where each sublist contains data for one product.
        """
        with open(
            self.output_file_path, mode="w", newline="", encoding="utf-8"
        ) as output_file:
            writer = csv.writer(output_file)
            writer.writerow(
                [
                    "Product URL",
                    "Description",
                    "Usage",
                    "Additional information - Manufacturer",
                ]
            )
            writer.writerows(data)

    def run(self):
        """
        Run the scraper through all URLs and save the results.
        """
        self.load_urls()
        all_data = []
        for index, url in enumerate(self.urls, start=1):
            data = self.scrape_data(url)
            all_data.append(data)
            print(f"Data successfully written for {index}/{self.total_urls} - {url}")
        self.write_output(all_data)
        print(f"All data successfully written to {self.output_file_path}")
