import os
import glob
import csv
from bs4 import BeautifulSoup

# Folder containing the HTML files
folder = 'mock_roe_4'
# Use glob to get a list of all HTML files in the folder
html_files = glob.glob(os.path.join(folder, '*.html'))

# List to collect each record (each table from each file)
records = []
# Set to collect all keys (for CSV header consistency)
all_keys = set()

# Loop through each HTML file
for file in html_files:
    with open(file, 'r', encoding='utf-8') as f:
        soup = BeautifulSoup(f, 'html.parser')
        # Find all tables with class "table"
        tables = soup.find_all('table', class_='table')
        for table in tables:
            rows = table.find_all('tr')
            if not rows:
                continue
            # Use the first row's header as the business name
            business_name = rows[0].get_text(strip=True)
            record = {'business': business_name}
            # Process remaining rows (each row should have 4 <td> cells)
            for row in rows[1:]:
                cells = row.find_all('td')
                # Process cells in pairs: key, then value
                for i in range(0, len(cells), 2):
                    key = cells[i].get_text(strip=True)
                    value = cells[i+1].get_text(strip=True)
                    record[key] = value
                    all_keys.add(key)
            records.append(record)

# Define CSV fieldnames: start with 'business' then sort the rest of the keys
fieldnames = ['business'] + sorted(all_keys)

# Write all records to html.csv
with open('html.csv', 'w', newline='', encoding='utf-8') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    for rec in records:
        writer.writerow(rec)

print(f"Extracted data from {len(html_files)} files and saved {len(records)} records to html.csv")