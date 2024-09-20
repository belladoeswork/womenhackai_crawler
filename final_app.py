# import streamlit as st
# import pandas as pd
# import plotly.express as px
# import folium
# from streamlit_folium import folium_static
# from geopy.geocoders import Nominatim
# from geopy.exc import GeocoderTimedOut, GeocoderServiceError
# from collections import Counter
# import nltk
# from nltk.corpus import stopwords
# import re
# import time


# # Download NLTK data
# nltk.download('stopwords', quiet=True)

# @st.cache_data
# def load_data():
#     df = pd.read_excel("cleaned_job_data.xlsx")
#     df['publishing_date'] = pd.to_datetime(df['publishing_date'])
#     return df



# def geocode(location, retries=3, delay=1):
#     geolocator = Nominatim(user_agent="my_agent")
#     try:
#         return geolocator.geocode(location, timeout=10)
#     except (GeocoderTimedOut, GeocoderServiceError) as e:
#         if retries > 0:
#             time.sleep(delay)  # Add delay before retrying
#             return geocode(location, retries - 1, delay)
#         else:
#             print(f"Geocoding failed for location: {location} with error: {e}")
#             return None

# def create_map(df):
#     m = folium.Map(location=[0, 0], zoom_start=2)

#     for _, row in df.iterrows():
#         loc = geocode(f"{row['city']}, {row['country']}")
#         if loc:
#             folium.Marker(
#                 [loc.latitude, loc.longitude],
#                 popup=f"{row['city']}, {row['country']}: {row['title']}",
#                 tooltip=row['company']
#             ).add_to(m)

#     return m

# def extract_keywords(text):
#     stop_words = set(stopwords.words('english'))
#     words = re.findall(r'\w+', text.lower())
#     return [word for word in words if word not in stop_words and len(word) > 2]

# # Load data
# df = load_data()

# # Convert all values in the 'country' column to strings
# df['country'] = df['country'].astype(str)

# # Streamlit app
# st.title('Rail Industry Job Market Insights')

# # Sidebar filters
# st.sidebar.header('Filters')
# companies = ['All'] + sorted(df['company'].unique().tolist())
# selected_company = st.sidebar.selectbox('Select Company', companies)
# countries = ['All'] + sorted(df['country'].unique().tolist())
# selected_country = st.sidebar.selectbox('Select Country', countries)

# # Filter data based on selections
# if selected_company != 'All':
#     df_filtered = df[df['company'] == selected_company]
# else:
#     df_filtered = df

# if selected_country != 'All':
#     df_filtered = df_filtered[df_filtered['country'] == selected_country]

# # Job Locations Map
# st.subheader('Job Locations')
# map = create_map(df_filtered)
# folium_static(map)

# # Time Series Analysis
# st.subheader('Job Postings Over Time')
# time_series = df_filtered.groupby('publishing_date').size().reset_index(name='count')
# fig_time = px.line(time_series, x='publishing_date', y='count', title='Job Postings Over Time')
# st.plotly_chart(fig_time)

# # Company Comparison
# st.subheader('Company Comparison')
# company_counts = df['company'].value_counts()
# fig_company = px.bar(x=company_counts.index, y=company_counts.values, title='Job Postings by Company')
# st.plotly_chart(fig_company)

# # Industry Trends
# st.subheader('Industry Trends')
# all_keywords = [keyword for job_desc in df['job_description'] for keyword in extract_keywords(job_desc)]
# keyword_counts = Counter(all_keywords).most_common(20)
# trend_df = pd.DataFrame(keyword_counts, columns=['Keyword', 'Count'])
# fig_trends = px.bar(trend_df, x='Keyword', y='Count', title='Top 20 Keywords in Job Descriptions')
# st.plotly_chart(fig_trends)

# # Industry Skills
# st.subheader('Industry Skills')
# all_titles = [title for job_title in df['title'] for title in extract_keywords(job_title)]
# title_counts = Counter(all_titles).most_common(20)
# skills_df = pd.DataFrame(title_counts, columns=['Skill', 'Count'])
# fig_skills = px.bar(skills_df, x='Skill', y='Count', title='Top 20 Skills in Job Titles')
# st.plotly_chart(fig_skills)

# # Company + Keyword Search
# st.subheader('Company + Keyword Search')
# search_company = st.selectbox('Select a company', companies)
# search_keyword = st.text_input('Enter a keyword')
# if search_company and search_keyword:
#     search_results = df[(df['company'] == search_company) & (df['job_description'].str.contains(search_keyword, case=False))]
#     st.write(f"Found {len(search_results)} jobs matching '{search_keyword}' for {search_company}")
#     st.dataframe(search_results[['title', 'location', 'publishing_date']])

# # Keyword by Country
# st.subheader('Keyword by Country')
# country_keyword = st.text_input('Enter a keyword to search across countries')
# if country_keyword:
#     country_results = df[df['job_description'].str.contains(country_keyword, case=False)].groupby('country').size().reset_index(name='count')
#     country_results = country_results.sort_values('count', ascending=False)
#     fig_country_keyword = px.bar(country_results, x='country', y='count', title=f'Countries with jobs mentioning "{country_keyword}"')
#     st.plotly_chart(fig_country_keyword)

# # Add New Competitor
# st.subheader('Add New Competitor')
# new_competitor = st.text_input('Enter the name of a new competitor')
# if new_competitor:
#     if new_competitor not in companies:
#         st.session_state['companies'] = companies + [new_competitor]
#         st.success(f"Added {new_competitor} to the list of companies!")
#     else:
#         st.warning(f"{new_competitor} is already in the list of companies.")

# if st.button('Refresh Data'):
#     st.experimental_rerun()



import os
import pandas as pd
import numpy as np
from datetime import datetime
import streamlit as st
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
import nltk
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut, GeocoderServiceError
import time
import folium
from streamlit_folium import folium_static
import re
from nltk.corpus import stopwords
from collections import Counter
import plotly.express as px
from dotenv import load_dotenv

# Load environment variables from .env.local file
load_dotenv('.env.local')

# Set up OpenAI API

# Download NLTK data
nltk.download('stopwords', quiet=True)

@st.cache_data
def load_data():
    df = pd.read_excel("cleaned_job_data.xlsx")
    df['publishing_date'] = pd.to_datetime(df['publishing_date'])
    return df

def geocode(location, retries=3, delay=1):
    geolocator = Nominatim(user_agent="my_agent")
    try:
        return geolocator.geocode(location, timeout=10)
    except (GeocoderTimedOut, GeocoderServiceError) as e:
        if retries > 0:
            time.sleep(delay)
            return geocode(location, retries - 1, delay)
        else:
            print(f"Geocoding failed for location: {location} with error: {e}")
            return None

def create_map(df):
    m = folium.Map(location=[0, 0], zoom_start=2)

    for _, row in df.iterrows():
        loc = geocode(f"{row['city']}, {row['country']}")
        if loc:
            folium.Marker(
                [loc.latitude, loc.longitude],
                popup=f"{row['city']}, {row['country']}: {row['title']}",
                tooltip=row['company']
            ).add_to(m)

    return m

def extract_keywords(text):
    stop_words = set(stopwords.words('english'))
    words = re.findall(r'\w+', text.lower())
    return [word for word in words if word not in stop_words and len(word) > 2]

def prepare_data_summary(df):
    company_summary = df.groupby('company').agg({
        'title': 'count',
        'country': lambda x: ', '.join(x.unique()),
        'job_description': lambda x: ' '.join(x)
    }).reset_index()
    company_summary.columns = ['company', 'job_count', 'countries', 'all_descriptions']

    for _, row in company_summary.iterrows():
        keywords = extract_keywords(row['all_descriptions'])
        keyword_freq = Counter(keywords).most_common(10)
        row['top_keywords'] = ', '.join([f"{k}({v})" for k, v in keyword_freq])

    return company_summary

from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# from openai import OpenAI

# client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def generate_response(prompt, data_summary):
    response = client.chat.completions.create(model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": "You are an AI assistant analyzing job market data for the rail industry. Use the provided data summary to answer questions."},
        {"role": "user", "content": f"Data summary:\n{data_summary}\n\nUser query: {prompt}"}
    ],
    max_tokens=150)
    return response.choices[0].message.content.strip()

# Load data
df = load_data()
df['country'] = df['country'].astype(str)

# Prepare data summary
data_summary = prepare_data_summary(df)

# Streamlit app
st.title('Rail Industry Job Market Insights')

# Sidebar filters
st.sidebar.header('Filters')
companies = ['All'] + sorted(df['company'].unique().tolist())
selected_company = st.sidebar.selectbox('Select Company', companies)
countries = ['All'] + sorted(df['country'].unique().tolist())
selected_country = st.sidebar.selectbox('Select Country', countries)

#Filter data based on selections
if selected_company != 'All':
    df_filtered = df[df['company'] == selected_company]
else:
    df_filtered = df

if selected_country != 'All':
    df_filtered = df_filtered[df_filtered['country'] == selected_country]

# Job Locations Map
st.subheader('Job Locations')
map = create_map(df_filtered)
folium_static(map)

# Time Series Analysis
st.subheader('Job Postings Over Time')
time_series = df_filtered.groupby('publishing_date').size().reset_index(name='count')
fig_time = px.line(time_series, x='publishing_date', y='count', title='Job Postings Over Time')
st.plotly_chart(fig_time)

# Company Comparison
st.subheader('Company Comparison')
company_counts = df['company'].value_counts()
fig_company = px.bar(x=company_counts.index, y=company_counts.values, title='Job Postings by Company')
st.plotly_chart(fig_company)

# Industry Trends
st.subheader('Industry Trends')
all_keywords = [keyword for job_desc in df['job_description'] for keyword in extract_keywords(job_desc)]
keyword_counts = Counter(all_keywords).most_common(20)
trend_df = pd.DataFrame(keyword_counts, columns=['Keyword', 'Count'])
fig_trends = px.bar(trend_df, x='Keyword', y='Count', title='Top 20 Keywords in Job Descriptions')
st.plotly_chart(fig_trends)

# Industry Skills
st.subheader('Industry Skills')
all_titles = [title for job_title in df['title'] for title in extract_keywords(job_title)]
title_counts = Counter(all_titles).most_common(20)
skills_df = pd.DataFrame(title_counts, columns=['Skill', 'Count'])
fig_skills = px.bar(skills_df, x='Skill', y='Count', title='Top 20 Skills in Job Titles')
st.plotly_chart(fig_skills)

# Company + Keyword Search
st.subheader('Company + Keyword Search')
search_company = st.selectbox('Select a company', companies)
search_keyword = st.text_input('Enter a keyword')
if search_company and search_keyword:
    search_results = df[(df['company'] == search_company) & (df['job_description'].str.contains(search_keyword, case=False))]
    st.write(f"Found {len(search_results)} jobs matching '{search_keyword}' for {search_company}")
    st.dataframe(search_results[['title', 'location', 'publishing_date']])

# Keyword by Country
st.subheader('Keyword by Country')
country_keyword = st.text_input('Enter a keyword to search across countries')
if country_keyword:
    country_results = df[df['job_description'].str.contains(country_keyword, case=False)].groupby('country').size().reset_index(name='count')
    country_results = country_results.sort_values('count', ascending=False)
    fig_country_keyword = px.bar(country_results, x='country', y='count', title=f'Countries with jobs mentioning "{country_keyword}"')
    st.plotly_chart(fig_country_keyword)

# Add New Competitor
st.subheader('Add New Competitor')
new_competitor = st.text_input('Enter the name of a new competitor')
if new_competitor:
    if new_competitor not in companies:
        st.session_state['companies'] = companies + [new_competitor]
        st.success(f"Added {new_competitor} to the list of companies!")
    else:
        st.warning(f"{new_competitor} is already in the list of companies.")

# Chatbot Interface
st.subheader('Chat with AI Assistant')
user_input = st.text_input("Ask a question about the rail industry job market:")
if user_input:
    data_summary_str = data_summary.to_string(index=False)
    response = generate_response(user_input, data_summary_str)
    st.write("AI Assistant:", response)

if st.button('Refresh Data'):
    st.experimental_rerun()