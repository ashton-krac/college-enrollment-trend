import sqlite3
import pandas as pd
import os

def insert_yearly_data(year, file_path, conn):
    df = pd.read_csv(file_path, usecols=['INSTNM', 'STABBR', 'UGDS'])
    df.rename(columns={'INSTNM': 'Name', 'STABBR': 'State', 'UGDS': 'Enrollment'}, inplace=True)
    df['Year'] = year
    df.dropna(subset=['Enrollment'], inplace=True)  # Drop rows where Enrollment is NaN
    df['Enrollment'] = df['Enrollment'].astype(int)  # Convert Enrollment to integer

    # Using INSERT OR IGNORE to avoid inserting duplicate rows
    for _, row in df.iterrows():
        insert_query = '''INSERT OR IGNORE INTO enrollment_data (Name, State, Year, Enrollment) VALUES (?, ?, ?, ?)'''
        conn.execute(insert_query, (row['Name'], row['State'], year, row['Enrollment']))

    conn.commit()

def main():
    data_folder_path = 'data'
    database_path = 'outputs/enrollment_data.db'

    # Ensure the directory exists
    os.makedirs(os.path.dirname(database_path), exist_ok=True)

    conn = sqlite3.connect(database_path)
    conn.execute('DROP TABLE IF EXISTS enrollment_data')  # Drop the table to start fresh
    conn.execute('''CREATE TABLE enrollment_data (
                        Name TEXT,
                        State TEXT,
                        Year INTEGER,
                        Enrollment INTEGER,
                        PRIMARY KEY (Name, State, Year)
                    )''')
    conn.commit()

    for year in range(1996, 2022):
        file_name = f"MERGED{year}_{str(year+1)[-2:]}_PP.csv"
        file_path = os.path.join(data_folder_path, file_name)
        if os.path.exists(file_path):
            insert_yearly_data(year, file_path, conn)

    # Close the database connection at the end
    conn.close()

if __name__ == "__main__":
    main()
