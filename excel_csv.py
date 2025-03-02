import pandas as pd
import argparse
import os

def excel_to_csv(excel_file, csv_file):
    # Read the Excel file (first sheet by default)
    df = pd.read_excel(excel_file)
    # Save to CSV
    df.to_csv(csv_file, index=False)
    print(f"Converted '{excel_file}' to '{csv_file}'.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Convert an Excel file to a CSV file."
    )
    parser.add_argument(
        "excel_file",
        help="Path to the input Excel file (e.g., data.xlsx)"
    )
    parser.add_argument(
        "csv_file",
        help="Path to the output CSV file (e.g., data.csv)"
    )
    args = parser.parse_args()

    # Check if input Excel file exists
    if not os.path.exists(args.excel_file):
        print(f"Error: The file '{args.excel_file}' does not exist.")
    else:
        excel_to_csv(args.excel_file, args.csv_file)