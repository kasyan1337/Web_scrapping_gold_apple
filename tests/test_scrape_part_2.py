import csv
import os

import pytest

from src.scrape_part_2 import ProductScraper_part_2


@pytest.fixture
def setup_test_environment():
    input_file_path = "./mock_data/test_PART_1.csv"
    output_file_path = "./mock_data/test_PART_2.csv"
    scraper = ProductScraper_part_2(input_file_path, output_file_path)
    return scraper


def test_load_urls(setup_test_environment):
    setup_test_environment.load_urls()
    assert (
        len(setup_test_environment.urls) > 0
    ), "URLs should be loaded from the input CSV"


def test_scrape_data(setup_test_environment):
    test_url = "https://goldapple.ru/19000125769-demain-promis"
    data = setup_test_environment.scrape_data(test_url)
    assert len(data) == 4, "Scraped data should return a list of 4 elements"
    assert data[0] == test_url, "First element should be the product URL"


def test_write_output(setup_test_environment):
    test_data = [
        [
            "https://goldapple.ru/19000125769-demain-promis",
            "День для себя – это любимая книга, просмотр сериала, теплая ванна и парфюмерная вода DEMAIN PROMIS. "
            "Окутывающая ароматическая композиция – словно эликсир расслабления во флаконе.Кажущийся знакомым и близким, "
            "но при этом чувственный аромат идеально подходит для беззаботных моментов отдыха. Приятная гармония нежных "
            "молочных нот, шалфея, розы, кардамона, сладких бобов тонка и кремового звучания сандала помогает отвлечься "
            "от всех забот, отложить дела и посвятить время себе.Французская парфюмерная вода BASTILLE создана на основе "
            "натуральных компонентов.Парфюмер – Caroline Dumur.",
            "Для наружного применения.",
            'страна происхожденияФранцияизготовитель:"ESTER SAS", '
            "адрес: 5 AVENUE DU GEN DE GAULLE, 94160 SAINT-MANDE, Франция.",
        ]
    ]
    setup_test_environment.write_output(test_data)
    assert os.path.exists(
        setup_test_environment.output_file_path
    ), "CSV file should be created"

    with open(
        setup_test_environment.output_file_path, mode="r", encoding="utf-8"
    ) as file:
        reader = csv.DictReader(file)
        rows = list(reader)
        assert len(rows) == 1, "CSV file should contain one row of data"
