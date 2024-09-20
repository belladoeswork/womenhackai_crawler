import pandas as pd
import json

# Load the Excel file
df = pd.read_excel("cleaned_job_data.xlsx")

# Convert datetime columns to string for JSON serialization
df['publishing_date'] = df['publishing_date'].astype(str)

# Convert DataFrame to dictionary
data_dict = df.to_dict(orient='records')

# Save as JSON
with open('job_data.json', 'w') as f:
    json.dump(data_dict, f)

print("Conversion complete. Data saved as 'job_data.json'")