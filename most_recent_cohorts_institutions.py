import pandas as pd

# Load the Most-Recent-Cohorts-Institution CSV file
institution_data_path = 'most_recent_cohorts_institutions.csv'
institution_data = pd.read_csv(institution_data_path)

# Extract the required columns
# Here, 'INSTNM' corresponds to the institution's name, 'STABBR' to the state abbreviation,
# and 'UGDS' to the enrollment of undergraduate certificate/degree-seeking students.
required_columns = institution_data[['INSTNM', 'STABBR', 'UGDS']]

# Rename the columns to match the desired output
required_columns_renamed = required_columns.rename(columns={'INSTNM': 'Name', 'STABBR': 'State', 'UGDS': 'Enrollment'})

# Save to a new CSV file
new_csv_path = 'current_enrollment_by_institution.csv'
required_columns_renamed.to_csv(new_csv_path, index=False)

print(f"The new CSV has been saved to {new_csv_path}")