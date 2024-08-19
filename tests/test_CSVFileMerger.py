import os.path

import pytest

from src.CSVFileMerger import CSVFileMerger


@pytest.fixture
def setup_test_environment():
    part1_path = "./mock_data/test_PART_1.csv"
    part2_path = "./mock_data/test_PART_2.csv"
    output_path = "./mock_data/test_merged_output.csv"
    merger = CSVFileMerger(part1_path, part2_path, output_path)
    return merger


def test_read_csv_files(setup_test_environment):
    setup_test_environment.read_csv_files()
    assert len(setup_test_environment.part1_data) > 0, "Part 1 data should be loaded"
    assert len(setup_test_environment.part2_data) > 0, "Part 2 data should be loaded"


def test_merge_files(setup_test_environment):
    setup_test_environment.read_csv_files()
    merged_data = setup_test_environment.merge_files()
    assert len(merged_data) == len(
        setup_test_environment.part1_data
    ), "Merged data should have same length as Part 1"


def test_write_merged_file(setup_test_environment):
    setup_test_environment.read_csv_files()
    merged_data = setup_test_environment.merge_files()
    setup_test_environment.write_merged_file(merged_data)
    assert os.path.exists(
        setup_test_environment.output_path
    ), "Merged CSV file should be created"


def test_validate(setup_test_environment):
    setup_test_environment.read_csv_files()
    merged_data = setup_test_environment.merge_files()
    setup_test_environment.validate(merged_data)
    assert len(merged_data) == 120, "Merged data should be validated"