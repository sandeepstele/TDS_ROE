import pandas as pd
import os

# File paths (adjust paths as necessary)
file1 = 'html.csv'
file2 = 'violations.csv'
output_file = 'output2.csv'

# Define the join column as it appears in W1.csv
join_column = "business_id"

# Check if files exist
if not os.path.exists(file1):
    print(f"Error: '{file1}' does not exist.")
    exit(1)
if not os.path.exists(file2):
    print(f"Error: '{file2}' does not exist.")
    exit(1)

# Read the CSV files
df1 = pd.read_csv(file1)
df2 = pd.read_csv(file2)

# Print the column names to inspect them
print("Columns in W1.csv:", df1.columns.tolist())
print("Columns in Pincode_Station_Code.csv:", df2.columns.tolist())

# In Pincode_Station_Code.csv the header for the first column might contain a newline.
# For example, it might be read as "STATION\nCODE". Let's fix that.
# We'll iterate over the columns in df2 and if any column, after replacing newline with space and stripping,
# equals our join_column, we rename it accordingly.
for col in df2.columns:
    fixed = col.replace("\n", " ").strip()
    if fixed == join_column:
        df2.rename(columns={col: join_column}, inplace=True)
        break

# Confirm that the join column is present in both DataFrames
if join_column not in df1.columns:
    print(f"Error: Join column '{join_column}' not found in W1.csv")
    exit(1)
if join_column not in df2.columns:
    print(f"Error: Join column '{join_column}' not found in Pincode_Station_Code.csv")
    exit(1)

# Perform the inner join on the join column
merged_df = pd.merge(df1, df2, how='inner', on=join_column)

# Write the merged result to the output file
merged_df.to_csv(output_file, index=False)
print(f"Inner join complete. Output saved to '{output_file}'.")

# For demonstration, let's print out the first few rows of the merged DataFrame:
print("\nFirst few rows of the merged data:")
print("Number of rows in merged data:", len(merged_df))
print(merged_df.head())