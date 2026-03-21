#!/usr/bin/env python3
import sys
import csv
from pathlib import Path
import xlsxwriter

def main():
    if len(sys.argv) != 3:
        print("Usage: python parse_to_excel.py <input_tsv_file> <output_excel_file>")
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2]

    if not Path(input_file).exists():
        print(f"Error: Input file {input_file} does not exist")
        sys.exit(1)

    # 创建 Excel 工作簿和工作表
    workbook = xlsxwriter.Workbook(output_file)
    worksheet = workbook.add_worksheet("Data")

    with open(input_file, 'r', encoding='utf-8') as f:
        reader = csv.reader(f, delimiter='\t')
        try:
            header = next(reader)
        except StopIteration:
            print("Error: TSV file is empty")
            workbook.close()
            sys.exit(1)

        for col_idx, value in enumerate(header):
            worksheet.write(0, col_idx, value)

        expected_cols = len(header)
        row_count = 0

        for row_idx, row in enumerate(reader, start=1):
            if not row:
                continue

            if len(row) != expected_cols:
                print(f"Warning: Row {row_idx+1} has {len(row)} columns, but header has {expected_cols} columns. Padding/truncating.")
                if len(row) < expected_cols:
                    row.extend([''] * (expected_cols - len(row)))
                else:
                    row = row[:expected_cols]

            for col_idx, value in enumerate(row):
                worksheet.write(row_idx, col_idx, value)
            row_count += 1

    workbook.close()
    print(f"Successfully wrote {row_count} rows to {output_file}")

if __name__ == '__main__':
    main()
