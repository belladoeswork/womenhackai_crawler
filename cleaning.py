# import pandas as pd
# import numpy as np
# from datetime import datetime

# def clean_job_data(file_path):
#     # Step 1: Load the data
#     df = pd.read_excel(file_path)
    
#     # Step 2: Drop unnecessary columns
#     columns_to_drop = ['Unnamed: 0', 'link', 'function']  # Add any other unnecessary columns here
#     df = df.drop(columns=columns_to_drop, errors='ignore')
    
#     # df = df[df['Business Unit'] != 'No Keywords Found']

    
#     # Step 3: Handle missing values
#     df = df.dropna(subset=['title', 'company', 'location', 'publishing_date'])  # Drop rows with missing crucial information
    
#     # Step 4: Standardize date/time
#     df['publishing_date'] = pd.to_datetime(df['publishing_date'], format='%b %d, %Y', errors='coerce')
#     df = df.dropna(subset=['publishing_date'])
#     df['publishing_date'] = df['publishing_date'].dt.strftime('%d-%b-%Y')

    
#     # Step 5: Clean and standardize location data
#     df['city'] = df['city'].str.strip()
#     df['country'] = df['country'].str.strip()
    
#     # Step 6: Standardize company names
#     df['company'] = df['company'].str.strip().str.title()
    
#     # Step 7: Clean job titles
#     df['title'] = df['title'].str.strip().str.title()
    

    
#     # Step 9: Remove duplicate entries
#     df = df.drop_duplicates()
    
#     # Step 10: Sort the dataframe by date
#     df = df.sort_values('publishing_date')
    
#     # Step 11: Reset index after all the cleaning steps
#     df = df.reset_index(drop=True)
    
#     return df

# # Usage example
# if __name__ == "__main__":
#     file_path = "Job_Postings.xlsx"
#     cleaned_df = clean_job_data(file_path)
#     print(cleaned_df.head())
#     print(cleaned_df.info())
    
#     # Optionally, save the cleaned data to a new Excel file
#     cleaned_df.to_excel("cleaned_job_data.xlsx", index=False)


import pandas as pd
import numpy as np
from datetime import datetime

def clean_job_data(file_path):
    # Step 1: Load the data
    df = pd.read_excel(file_path)
    
    # Step 2: Drop unnecessary columns
    columns_to_drop = ['Unnamed: 0', 'link', 'function']  # Add any other unnecessary columns here
    df = df.drop(columns=columns_to_drop, errors='ignore')
    
    # Step 3: Handle missing values
    print("Rows before dropping NaN in 'company':", len(df))
    print("Unique companies after cleaning: ", df['company'].unique())

    df = df.dropna(subset=['title', 'company', 'location', 'publishing_date'])
    print("Rows after dropping NaN in 'company':", len(df))
    print("Unique companies after dropping NaN: ", df['company'].unique())

    # Step 4: Standardize date/time
    df['publishing_date'] = pd.to_datetime(df['publishing_date'], format='%b %d, %Y', errors='coerce')
    print("Unique companies after date: ", df['company'].unique())

    # Step 5: Clean and standardize location data
    df['city'] = df['city'].str.strip()
    df['country'] = df['country'].str.strip()
    print("Unique companies after country/city: ", df['company'].unique())

    # Step 6: Standardize company names
    df['company'] = df['company'].str.strip().str.title()
    df = df[df['company'].str.lower() != 'company']  # Remove rows where 'company' name is 'company'
    print("Unique companies after dropping 'company': ", df['company'].unique())

    # Step 7: Clean job titles
    df['title'] = df['title'].str.strip().str.title()
    print("Unique companies after title: ", df['company'].unique())

    # Step 8: Remove rows with 'No Keywords Found' in 'Business Unit'
    if 'Business Unit' in df.columns:
        df = df[df['Business Unit'] != 'No Keywords Found']
    print("Unique companies after dropping 'Business Unit': ", df['company'].unique())

    # Step 9: Remove duplicate entries
    df = df.drop_duplicates()

    # Step 10: Sort the dataframe by date
    df = df.sort_values('publishing_date')

    # Step 11: Reset index after all the cleaning steps
    df = df.reset_index(drop=True)
    print("Unique companies after resetting index and sorting: ", df['company'].unique())

    return df

# Usage example
if __name__ == "__main__":
    file_path = "Job_Postings.xlsx"
    cleaned_df = clean_job_data(file_path)
    print(cleaned_df.head())
    print(cleaned_df.info())
    
    # Optionally, save the cleaned data to a new Excel file
    cleaned_df.to_excel("cleaned_job_data.xlsx", index=False)