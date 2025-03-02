import sqlite3
import csv
import os
import argparse

def db_to_csv(db_file):
    # Connect to the SQLite database
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    
    # Retrieve all table names from the database
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    
    # Create an output directory to save CSV files
    output_dir = "csv_output"
    os.makedirs(output_dir, exist_ok=True)
    
    for table in tables:
        table_name = table[0]
        print(f"Exporting table: {table_name}")
        
        # Fetch all rows from the table
        cursor.execute(f"SELECT * FROM {table_name}")
        rows = cursor.fetchall()
        
        # Get column headers
        cursor.execute(f"PRAGMA table_info({table_name})")
        headers = [info[1] for info in cursor.fetchall()]
        
        # Define CSV file path
        csv_file_path = os.path.join(output_dir, f"{table_name}.csv")
        
        # Write the table data to CSV
        with open(csv_file_path, mode="w", newline="", encoding="utf-8") as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow(headers)  # write header row
            writer.writerows(rows)    # write data rows
    
    # Clean up and close the connection
    conn.close()
    print(f"CSV files have been saved to the '{output_dir}' directory.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("file", help="Name of the input SQLite database file")
    args = parser.parse_args()
    db_to_csv(args.file)