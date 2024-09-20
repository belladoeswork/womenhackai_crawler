import pandas as pd
import json
import re
from datetime import datetime, timedelta
import streamlit as st
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut, GeocoderServiceError
import folium
from streamlit_folium import folium_static
import plotly.express as px

@st.cache_data
def load_excel_data():
    df = pd.read_excel("cleaned_job_data.xlsx")
    df['publishing_date'] = pd.to_datetime(df['publishing_date'])
    return df

def prepare_concise_summary(df):
    if 'company' not in df.columns:
        st.error("The 'company' column is missing from the data.")
        return None
    summary = {
        'total_jobs': len(df),
        'companies': df['company'].unique().tolist(),
        'countries': df['country'].unique().tolist(),
        'business_units': df['Business Unit'].unique().tolist(),
        'date_range': f"{df['publishing_date'].min().date()} to {df['publishing_date'].max().date()}"
    }
    return summary

def generate_response(prompt, concise_summary):
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are an AI assistant analyzing job market data for the rail industry. Use the provided summary to answer questions concisely."},
                {"role": "user", "content": f"Summary: {concise_summary}\n\nUser query: {prompt}"}
            ],
            max_tokens=100
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")
        return None

def process_query(query, df, concise_summary):
    if "how many jobs" in query.lower():
        company_match = next((company for company in df['company'].unique() if company.lower() in query.lower()), None)
        if company_match:
            if "last" in query.lower() and "months" in query.lower():
                months = int(re.search(r'last (\d+) months', query.lower()).group(1))
                end_date = datetime.now()
                start_date = end_date - timedelta(days=30*months)
                job_count = df[(df['company'] == company_match) & (df['publishing_date'] >= start_date) & (df['publishing_date'] <= end_date)].shape[0]
                return f"{company_match} has posted {job_count} jobs in the last {months} months."
            else:
                job_count = df[df['company'] == company_match].shape[0]
                return f"{company_match} has posted {job_count} jobs in total."
    return generate_response(query, concise_summary)

@st.cache_data
def load_json_data():
    json_files = [
        'alstom_results/job_market_insights_report.json',
        'caf_results/job_market_insights_report.json',
        'hitachi_results/job_market_insights_report.json',
        'stadler_results/job_market_insights_report.json',
        'thales_results/job_market_insights_report.json'
    ]
    
    all_locations = {}
    
    for file in json_files:
        with open(file, 'r') as f:
            data = json.load(f)
            top_locations = data.get('Top Job Locations', {})
            for location, count in top_locations.items():
                if location in all_locations:
                    all_locations[location] += count
                else:
                    all_locations[location] = count
    
    return all_locations

@st.cache_data
def geocode(location, retries=3):
    geolocator = Nominatim(user_agent="my_agent")
    try:
        return geolocator.geocode(location)
    except (GeocoderTimedOut, GeocoderServiceError) as e:
        if retries > 0:
            return geocode(location, retries - 1)
        else:
            print(f"Geocoding failed for location: {location} with error: {e}")
            return None

@st.cache_data
def create_global_job_map(location_data):
    m = folium.Map(location=[20, 0], zoom_start=2)
    
    for location, count in location_data.items():
        loc = geocode(location)
        if loc:
            folium.CircleMarker(
                [loc.latitude, loc.longitude],
                radius=5,
                popup=f"{location}: {count} jobs",
                tooltip=location,
                color="#3186cc",
                fill=True,
                fillColor="#3186cc"
            ).add_to(m)
    
    return m

def company_comparison(df, selected_companies):
    if not selected_companies:
        return None

    comparison_data = {}
    
    # Location comparison
    location_data = df[df['company'].isin(selected_companies)].groupby(['company', 'location']).size().reset_index(name='count')
    location_data = location_data.sort_values('count', ascending=False).groupby('company').head(5)
    
    # Country comparison
    country_data = df[df['company'].isin(selected_companies)].groupby(['company', 'country']).size().reset_index(name='count')
    country_data = country_data.sort_values('count', ascending=False).groupby('company').head(5)
    
    # Title comparison
    title_data = df[df['company'].isin(selected_companies)].groupby(['company', 'title']).size().reset_index(name='count')
    title_data = title_data.sort_values('count', ascending=False).groupby('company').head(5)
    
    # Business Unit comparison
    bu_data = df[df['company'].isin(selected_companies)].groupby(['company', 'Business Unit']).size().reset_index(name='count')
    bu_data = bu_data.sort_values('count', ascending=False).groupby('company').head(5)

    comparison_data['location'] = location_data
    comparison_data['country'] = country_data
    comparison_data['title'] = title_data
    comparison_data['Business Unit'] = bu_data

    return comparison_data

# Load data
df = load_excel_data()
all_locations = load_json_data()

# Prepare concise summary
concise_summary = prepare_concise_summary(df)
if concise_summary is None:
    st.stop()

# Streamlit app
st.title('Rail Industry Job Market Insights')

# Display global job locations on a map
st.subheader('Global Job Locations')
job_map = create_global_job_map(all_locations)
folium_static(job_map)

# Company Comparison
def company_comparison(df, selected_companies, metric):
    if not selected_companies:
        return None

    if metric == 'location':
        data = df[df['company'].isin(selected_companies)].groupby(['company', 'location']).size().reset_index(name='count')
    elif metric == 'country':
        data = df[df['company'].isin(selected_companies)].groupby(['company', 'country']).size().reset_index(name='count')
    elif metric == 'title':
        data = df[df['company'].isin(selected_companies)].groupby(['company', 'title']).size().reset_index(name='count')
    elif metric == 'Business Unit':
        data = df[df['company'].isin(selected_companies)].groupby(['company', 'Business Unit']).size().reset_index(name='count')
    else:
        return None

    return data.sort_values('count', ascending=False).groupby('company').head(5)

# Load data
df = load_excel_data()
all_locations = load_json_data()

# Prepare concise summary
concise_summary = prepare_concise_summary(df)
if concise_summary is None:
    st.stop()


# Company Comparison
st.subheader('Company Comparison')
selected_companies = st.multiselect('Select companies to compare', df['company'].unique())

if selected_companies:
    metrics = ['location', 'country', 'title', 'Business Unit']
    selected_metric = st.selectbox('Select comparison metric', metrics)
    
    comparison_data = company_comparison(df, selected_companies, selected_metric)
    
    if comparison_data is not None:
        st.write(f"Top 5 {selected_metric.capitalize()}s by Company")
        fig = px.bar(comparison_data, x=selected_metric, y='count', color='company', barmode='group')
        st.plotly_chart(fig)

# Chatbot Interface
st.subheader('Chat with AI Assistant')

# Use columns to create a row with input field and send button
col1, col2 = st.columns([3, 1])
with col1:
    user_input = st.text_input("Ask a question about the rail industry job market:", key="user_input")
with col2:
    send_button = st.button("Send")

# Process the query when the send button is clicked
if send_button and user_input:
    response = process_query(user_input, df, concise_summary)
    if response:
        st.write("AI Assistant:", response)