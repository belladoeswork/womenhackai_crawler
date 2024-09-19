import json
import pandas as pd
from datetime import datetime

def json_to_excel(json_file_path, excel_file_path=None):
    # Load JSON data
    with open(json_file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
    
    # to df
    df = pd.DataFrame(data)
    
    # create excel_file_path 
    if excel_file_path is None:
        # timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        excel_file_path = f'alstom_jobs.xlsx'
    
    # Save to Excel
    df.to_excel(excel_file_path, index=False, engine='openpyxl')
    print(f"Data saved to {excel_file_path}")

if __name__ == "__main__":
    # Replace with your JSON file path
    json_file = 'alstom_jobs_20240919_170036.json'
    json_to_excel(json_file)
    