import sqlite3
import pandas as pd

def export_database_to_csv(database_path, csv_output_path):
    # Connect to the SQLite database
    conn = sqlite3.connect(database_path)

    # Query to select all data from enrollment_data table
    query = "SELECT * FROM enrollment_data ORDER BY Name, State, Year"

    # Execute the query and store the result in a pandas DataFrame
    df = pd.read_sql_query(query, conn)

    # Pivot the DataFrame to have years as columns and institutions as rows
    pivoted_df = df.pivot_table(index=['Name', 'State'], columns='Year', values='Enrollment').reset_index()

    # Rename the columns for clarity
    pivoted_df.columns.name = None  # Remove the categories name
    pivoted_df.columns = ['Name', 'State'] + [str(year) + ' Enrollment' for year in pivoted_df.columns[2:]]

    # Export the pivoted DataFrame to a CSV file
    pivoted_df.to_csv(csv_output_path, index=False)

    # Close the database connection
    conn.close()

    print(f"Data exported to {csv_output_path}")

# Usage example
database_path = 'outputs/enrollment_data.db'
csv_output_path = 'outputs/institutions_enrollment_by_year_20240306v2.csv'
export_database_to_csv(database_path, csv_output_path)
