#!/usr/bin/env python3
import sys
import csv
from pathlib import Path
from openpyxl import Workbook

def main():
    if len(sys.argv) != 3:
        print("Usage: python parse_to_excel.py <input_tsv_file> <output_excel_file>")
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2]

    if not Path(input_file).exists():
        print(f"Error: Input file {input_file} does not exist")
        sys.exit(1)

    workbook = Workbook()
    worksheet = workbook.active
    worksheet.title = "Data"

    with open(input_file, 'r', encoding='utf-8') as f:
        reader = csv.reader(f, delimiter='\t')
        try:
            header = next(reader)
        except StopIteration:
            print("Error: TSV file is empty")
            sys.exit(1)

        worksheet.append(header)

        expected_cols = len(header)
        row_count = 0

        for row in reader:
            if not row:
                continue

            if len(row) != expected_cols:
                print(f"Warning: Row {row_count+2} has {len(row)} columns, but header has {expected_cols} columns. Padding/truncating.")
                if len(row) < expected_cols:
                    row.extend([''] * (expected_cols - len(row)))
                else:
                    row = row[:expected_cols]

            worksheet.append(row)
            row_count += 1

    workbook.save(output_file)
    print(f"Successfully wrote {row_count} rows to {output_file}")

if __name__ == '__main__':
    main()
