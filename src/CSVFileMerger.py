import csv
import os


class CSVFileMerger:
    """
    A class to merge two CSV files based on a common 'Product URL' key.
    """

    def __init__(self, part1_path, part2_path, output_path):
        """
        Initialize the CSVFileMerger with paths to the two CSV files and the output file.

        Parameters:
        part1_path (str): Path to the first CSV file (PART_1_test.csv).
        part2_path (str): Path to the second CSV file (PART_2_test.csv).
        output_path (str): Path to the output CSV file.
        """
        self.part1_path = part1_path
        self.part2_path = part2_path
        self.output_path = output_path
        self.part1_data = []
        self.part2_data = {}

    def read_csv_files(self):
        """
        Read the two CSV files and store their contents.

        The first CSV file is read and stored as a list of dictionaries.
        The second CSV file is read and stored as a dictionary, where the key is 'Product URL'.
        """
        # Read PART_1_test.csv
        with open(self.part1_path, mode='r', encoding='utf-8') as file1:
            reader = csv.DictReader(file1)
            self.part1_data = list(reader)

        # Read PART_2_test.csv
        with open(self.part2_path, mode='r', encoding='utf-8') as file2:
            reader = csv.DictReader(file2)
            for row in reader:
                product_url = row['Product URL']
                self.part2_data[product_url] = {
                    'Description': row['Description'],
                    'Usage': row['Usage'],
                    'Additional information - Manufacturer': row['Additional information - Manufacturer']
                }

    def merge_files(self):
        """
        Merge the data from the two CSV files based on 'Product URL'.

        If a 'Product URL' from the first CSV file is found in the second CSV file,
        additional information from the second CSV file is added to the corresponding row.

        If a 'Product URL' is not found in the second CSV file, empty fields are added
        for the additional information.

        Returns:
        list: A list of dictionaries representing the merged CSV data.
        """
        merged_data = []
        for row in self.part1_data:
            product_url = row['Product URL']
            if product_url in self.part2_data:
                row.update(self.part2_data[product_url])
            else:
                # If the product URL is missing in part 2, add empty fields for part 2 data
                row.update({
                    'Description': '',
                    'Usage': '',
                    'Additional information - Manufacturer': ''
                })
            merged_data.append(row)
        return merged_data

    def write_merged_file(self, merged_data):
        """
        Write the merged data to the output CSV file.

        Parameters:
        merged_data (list): A list of dictionaries representing the merged CSV data.
        """
        if not merged_data:
            print("No data to write.")
            return

        # Write the merged data to the output CSV
        with open(self.output_path, mode='w', newline='', encoding='utf-8') as output_file:
            fieldnames = list(merged_data[0].keys())
            writer = csv.DictWriter(output_file, fieldnames=fieldnames)
            writer.writeheader()
            for data in merged_data:
                writer.writerow(data)

    def validate(self, merged_data):
        """
        Validate the merged data by checking if all 'Product URL' entries in the first CSV file
        are present in the second CSV file.

        Parameters:
        merged_data (list): A list of dictionaries representing the merged CSV data.
        """
        for row in merged_data:
            product_url = row['Product URL']
            if product_url not in self.part2_data:
                print(f"Warning: {product_url} not found in PART_2_test.csv")

    def execute(self):
        """
        Execute the merging process by reading the CSV files, merging them, validating the results,
        and writing the merged data to the output file.
        """
        self.read_csv_files()
        merged_data = self.merge_files()
        self.validate(merged_data)
        self.write_merged_file(merged_data)
        print(f"Merged file created at: {self.output_path}")