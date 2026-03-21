#!/usr/bin/env python3
import sys
import csv
from pathlib import Path
from openpyxl import Workbook

def main():
    if len(sys.argv) != 3:
        print("Usage: python parse_to_excel.py <input_file> <output_excel_file>")
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2]

    if not Path(input_file).exists():
        print(f"Error: Input file {input_file} does not exist")
        sys.exit(1)

    # Read CSV
    rows = []
    with open(input_file, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        try:
            header = next(reader)
        except StopIteration:
            print("Error: CSV file is empty")
            sys.exit(1)

        for row in reader:
            if row:  # skip empty lines
                rows.append(row)

    if not rows:
        print("No valid data found, exiting")
        sys.exit(0)

    # Ensure consistent column count
    expected_cols = len(header)
    for i, row in enumerate(rows):
        if len(row) != expected_cols:
            print(f"Warning: Row {i+2} has {len(row)} columns, but header has {expected_cols} columns. Padding/truncating.")
            if len(row) < expected_cols:
                row.extend([''] * (expected_cols - len(row)))
            else:
                rows[i] = row[:expected_cols]

    # Create Excel workbook
    wb = Workbook()
    ws = wb.active
    ws.title = "Data"

    # Write header
    ws.append(header)

    # Write data rows
    for row in rows:
        ws.append(row)

    # Save
    wb.save(output_file)
    print(f"Successfully wrote {len(rows)} rows to {output_file}")

if __name__ == '__main__':
    main()
