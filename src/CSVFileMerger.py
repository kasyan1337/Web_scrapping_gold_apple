import csv
import os


class CSVFileMerger:
    def __init__(self, part1_path, part2_path, output_path):
        self.part1_path = part1_path
        self.part2_path = part2_path
        self.output_path = output_path
        self.part1_data = []
        self.part2_data = {}

    def read_csv_files(self):
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
        for row in merged_data:
            product_url = row['Product URL']
            if product_url not in self.part2_data:
                print(f"Warning: {product_url} not found in PART_2_test.csv")

    def execute(self):
        self.read_csv_files()
        merged_data = self.merge_files()
        self.validate(merged_data)
        self.write_merged_file(merged_data)
        print(f"Merged file created at: {self.output_path}")


if __name__ == "__main__":
    data_folder = '../data'
    part1_file = os.path.join(data_folder, "PART_1.csv")
    part2_file = os.path.join(data_folder, "PART_2.csv")
    output_file = os.path.join(data_folder, "Goldapple_parfyumeriya.csv")

    merger = CSVFileMerger(part1_file, part2_file, output_file)
    merger.execute()
