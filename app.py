# import json
# import re
# import streamlit as st
# import pandas as pd
# import plotly.express as px
# import folium
# from streamlit_folium import folium_static
# from geopy.geocoders import Nominatim
# from geopy.exc import GeocoderTimedOut, GeocoderServiceError

# @st.cache_data
# def load_data():
#     json_files = [
#         'alstom_results/job_market_insights_report.json',
#         'caf_results/job_market_insights_report.json',
#         'hitachi_results/job_market_insights_report.json',
#         'stadler_results/job_market_insights_report.json',
#         'thales_results/job_market_insights_report.json'
#     ]
    
#     location_data = {}
#     job_postings_timeline = {}
#     job_functions_data = {}
    
#     for file in json_files:
#         with open(file, 'r') as f:
#             data = json.load(f)
#             top_locations = data.get('Top Job Locations', {})
#             for location, count in top_locations.items():
#                 # Validate location to ensure it's not a date or other non-location data
#                 if re.match(r'^[A-Za-z\s,]+$', location):
#                     if location in location_data:
#                         location_data[location] += count
#                     else:
#                         location_data[location] = count
            
#             # Extract Job Postings Timeline
#             job_postings = data.get('Job Postings Timeline', {})
#             for date, count in job_postings.items():
#                 if date in job_postings_timeline:
#                     job_postings_timeline[date] += count
#                 else:
#                     job_postings_timeline[date] = count
                    
                    
#             # Extract Top Job Functions
#             top_functions = data.get('Top Job Functions', {})
#             for function, count in top_functions.items():
#                 if function in job_functions_data:
#                     job_functions_data[function] += count
#                 else:
#                     job_functions_data[function] = count
    
#     return location_data, job_postings_timeline, job_functions_data

# location_data, job_postings_timeline, job_functions_data = load_data()

# def geocode(location, retries=3):
#     geolocator = Nominatim(user_agent="my_agent")
#     try:
#         return geolocator.geocode(location)
#     except (GeocoderTimedOut, GeocoderServiceError) as e:
#         if retries > 0:
#             return geocode(location, retries - 1)
#         else:
#             print(f"Geocoding failed for location: {location} with error: {e}")
#             return None

# def get_continent(location):
#     geolocator = Nominatim(user_agent="my_agent")
#     try:
#         loc = geolocator.geocode(location)
#         if loc:
#             return loc.raw.get('address', {}).get('continent', 'Unknown')
#     except GeocoderTimedOut:
#         return get_continent(location)
#     return 'Unknown'

# def create_map(location_data):
#     m = folium.Map(location=[0, 0], zoom_start=2)
    
#     for location, count in location_data.items():
#         loc = geocode(location)
#         if loc:
#             folium.Marker(
#                 [loc.latitude, loc.longitude],
#                 popup=f"{location}: {count} jobs",
#                 tooltip=location
#             ).add_to(m)
#         else:
#             print(f"Geocoding failed for location: {location}")
       
#     return m

# # init set up
# st.title('Rail Industry Job Market Insights')
# st.sidebar.header('Filters')

# # Continent filter
# continents = ['All', 'Africa', 'Asia', 'Europe', 'North America', 'Oceania', 'South America']
# selected_continent = st.sidebar.selectbox('Select Continent', continents)

# # Job Locations Map
# st.subheader('Job Locations')

# # Ensure location data is not empty
# if location_data:
#     map = create_map(location_data)
#     folium_static(map)
# else:
#     st.write("No location data available.")

# # Time Series Analysis
# st.subheader('Job Postings Over Time')
# time_series_data = pd.DataFrame(list(job_postings_timeline.items()), columns=['Date', 'Count'])
# time_series_data['Date'] = pd.to_datetime(time_series_data['Date'])
# fig = px.line(time_series_data, x='Date', y='Count', title='Job Postings Over Time')
# st.plotly_chart(fig)







### here


import json
import re
import streamlit as st
import pandas as pd
import plotly.express as px
import folium
from streamlit_folium import folium_static
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut, GeocoderServiceError

@st.cache_data
def load_data():
    json_files = [
        'alstom_results/job_market_insights_report.json',
        'caf_results/job_market_insights_report.json',
        'hitachi_results/job_market_insights_report.json',
        'stadler_results/job_market_insights_report.json',
        'thales_results/job_market_insights_report.json'
    ]
    
    all_data = {}
    
    for file in json_files:
        company_name = file.split('/')[0].split('_')[0].capitalize()
        with open(file, 'r') as f:
            data = json.load(f)
            all_data[company_name] = data
    
    return all_data

all_data = load_data()

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

def get_continent(location):
    geolocator = Nominatim(user_agent="my_agent")
    try:
        loc = geolocator.geocode(location)
        if loc:
            return loc.raw.get('address', {}).get('continent', 'Unknown')
    except GeocoderTimedOut:
        return get_continent(location)
    return 'Unknown'

def create_map(location_data):
    m = folium.Map(location=[0, 0], zoom_start=2)
    
    for location, count in location_data.items():
        loc = geocode(location)
        if loc:
            folium.Marker(
                [loc.latitude, loc.longitude],
                popup=f"{location}: {count} jobs",
                tooltip=location
            ).add_to(m)
        else:
            print(f"Geocoding failed for location: {location}")
       
    return m


# init set up
st.title('Rail Industry Job Market Insights')
st.sidebar.header('Filters')

# Continent filter
continents = ['All', 'Africa', 'Asia', 'Europe', 'North America', 'Oceania', 'South America']
selected_continent = st.sidebar.selectbox('Select Continent', continents)

# Job Locations Map
st.subheader('Job Locations')

# Aggregate location data across all companies
location_data = {}
for company_data in all_data.values():
    for location, count in company_data.get('Top Job Locations', {}).items():
        if re.match(r'^[A-Za-z\s,]+$', location):
            location_data[location] = location_data.get(location, 0) + count

if location_data:
    map = create_map(location_data)
    folium_static(map)
else:
    st.write("No location data available.")

# Time Series Analysis
st.subheader('Job Postings Over Time')
time_series_data = pd.DataFrame()
for company, data in all_data.items():
    df = pd.DataFrame(list(data.get('Job Postings Timeline', {}).items()), columns=['Date', company])
    df['Date'] = pd.to_datetime(df['Date'])
    if time_series_data.empty:
        time_series_data = df
    else:
        time_series_data = pd.merge(time_series_data, df, on='Date', how='outer')

time_series_data = time_series_data.fillna(0)
time_series_data = time_series_data.set_index('Date')
fig = px.line(time_series_data, title='Job Postings Over Time')
st.plotly_chart(fig)

# Company Comparison
st.subheader('Company Comparison')
companies = list(all_data.keys())
selected_companies = st.multiselect('Select companies to compare', companies, default=companies[:2])
comparison_metric = st.selectbox('Select comparison metric', ['Top Job Functions', 'Common Job Title Keywords'])

comparison_data = {}
for company in selected_companies:
    if comparison_metric == 'Top Job Functions':
        comparison_data[company] = all_data[company].get('Top Job Functions', {})
    else:
        comparison_data[company] = all_data[company].get('Common Job Title Keywords', {})

comparison_df = pd.DataFrame(comparison_data).fillna(0)
fig_comparison = px.bar(comparison_df, title=f'Company Comparison: {comparison_metric}')
st.plotly_chart(fig_comparison)
# company and keyword
# which setup has xyz in country
# scalability is easy to add a competitor - admin page, define your competitors suggest somethin in the front end to add a new competitor 


# Industry Shifts
st.subheader('Industry Shifts')
industry_shifts = {}
for company, data in all_data.items():
    shifts = data.get('Industry Shifts', [])
    for shift in shifts:
        trend = shift[0]
        count = shift[1]
        industry_shifts[trend] = industry_shifts.get(trend, 0) + count

industry_shifts_df = pd.DataFrame(list(industry_shifts.items()), columns=['Trend', 'Count'])
industry_shifts_df = industry_shifts_df.sort_values('Count', ascending=False).head(10)
fig_shifts = px.bar(industry_shifts_df, x='Trend', y='Count', title='Top 10 Industry Trends')
st.plotly_chart(fig_shifts)