# import streamlit as st
# import plotly.graph_objects as go
# import numpy as np

# # Set page title
# st.set_page_config(page_title="3D Globe Viewer")

# # Create a slider for resolution
# res = st.slider("Resolution", 50, 200, 100, 10)

# # Create the sphere
# phi = np.linspace(0, np.pi, res)
# theta = np.linspace(0, 2*np.pi, res)
# phi, theta = np.meshgrid(phi, theta)

# x = np.sin(phi) * np.cos(theta)
# y = np.sin(phi) * np.sin(theta)
# z = np.cos(phi)

# # Create the globe
# globe = go.Surface(
#     x=x, y=y, z=z,
#     colorscale=[[0, 'rgb(0, 0, 255)'],    # blue for water
#                 [1, 'rgb(0, 200, 0)']],   # green for land
#     showscale=False
# )

# # Create the layout
# layout = go.Layout(
#     title='Interactive 3D Globe',
#     scene=dict(
#         xaxis=dict(visible=False),
#         yaxis=dict(visible=False),
#         zaxis=dict(visible=False),
#         aspectmode='data'
#     ),
#     updatemenus=[dict(
#         type='buttons',
#         showactive=False,
#         buttons=[dict(
#             label='Play',
#             method='animate',
#             args=[None, dict(frame=dict(duration=50, redraw=True), fromcurrent=True, mode='immediate')]
#         )]
#     )]
# )

# # Create frames for rotation
# frames = [go.Frame(data=[go.Surface(
#     z=z,
#     x=x * np.cos(2 * np.pi * k / 100) + y * np.sin(2 * np.pi * k / 100),
#     y=y * np.cos(2 * np.pi * k / 100) - x * np.sin(2 * np.pi * k / 100),
#     colorscale=[[0, 'rgb(0, 0, 255)'], [1, 'rgb(0, 200, 0)']],
#     showscale=False
# )]) for k in range(100)]

# # Create the figure and add frames
# fig = go.Figure(data=[globe], layout=layout, frames=frames)

# # Display the globe in Streamlit
# st.plotly_chart(fig, use_container_width=True)

# # Add some information about the globe
# st.write("This 3D globe is created using Plotly and displayed with Streamlit.")
# st.write("Use the 'Resolution' slider to adjust the globe's detail level.")
# st.write("Click the 'Play' button to start the rotation animation.")

#ok too
# import streamlit as st
# import plotly.graph_objects as go
# import numpy as np
# from geovista import GeoPlotter  # Ensure this is the correct import

# # Set page title
# st.set_page_config(page_title="3D Globe Viewer")

# # Create a slider for resolution
# res = st.slider("Resolution", 50, 200, 100, 10)

# # Create the sphere
# phi = np.linspace(0, np.pi, res)
# theta = np.linspace(0, 2 * np.pi, res)
# phi, theta = np.meshgrid(phi, theta)
# x = np.sin(phi) * np.cos(theta)
# y = np.sin(phi) * np.sin(theta)
# z = np.cos(phi)

# # Create the surface color
# surfacecolor = np.sin(phi)

# # Create the globe
# globe = go.Surface(
#     x=x, y=y, z=z,
#     surfacecolor=surfacecolor,
#     colorscale=[[0, 'rgb(0, 0, 255)'], [1, 'rgb(0, 0, 255)']],
#     showscale=False
# )

# # Create the layout
# layout = go.Layout(
#     title="3D Globe",
#     scene=dict(
#         xaxis=dict(showbackground=False),
#         yaxis=dict(showbackground=False),
#         zaxis=dict(showbackground=False),
#     ),
#     margin=dict(l=0, r=0, b=0, t=0),
# )

# # Create the figure
# fig = go.Figure(data=[globe], layout=layout)

# # Display the globe in Streamlit
# st.plotly_chart(fig, use_container_width=True)

# # Add some information about the globe
# st.write("This 3D globe is created using GeoVista, Plotly, and displayed with Streamlit.")
# st.write("Use the 'Resolution' slider to adjust the globe's detail level.")

import streamlit as st
import geovista as gv
import geovista.theme
import pyvista as pv
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut
import json
import re
import stpyvista
import numpy as np

# Function to load and geocode job location data
def load_data():
    json_files = [
        'alstom_results/job_market_insights_report.json',
        'caf_results/job_market_insights_report.json',
        'hitachi_results/job_market_insights_report.json',
        'stadler_results/job_market_insights_report.json',
        'thales_results/job_market_insights_report.json'
    ]
    
    location_data = {}
    for file in json_files:
        with open(file, 'r') as f:
            data = json.load(f)
            top_locations = data.get('Top Job Locations', {})
            for location, count in top_locations.items():
                # Validate location
                if re.match(r'^[A-Za-z\s,]+$', location):
                    if location in location_data:
                        location_data[location] += count
                    else:
                        location_data[location] = count
    
    return location_data

# Function to geocode locations
def geocode(location):
    geolocator = Nominatim(user_agent="geo_agent")
    try:
        return geolocator.geocode(location)
    except GeocoderTimedOut:
        return geocode(location)

# Plot the job locations on a globe
def plot_job_locations_globe(location_data):
    # Create the geovista mesh (earth's surface)
    plotter = gv.GeoPlotter()

    # Create the globe mesh using Blue Marble as the texture
    globe_mesh = gv.Transform.from_1d(np.linspace(-180, 180, 360), np.linspace(-90, 90, 180))
    
    # Add a base layer (Blue Marble or coastline)
    plotter.add_base_layer(texture=gv.datasets.blue_marble())
    plotter.add_coastlines()

    # Add job locations to the globe
    for location, count in location_data.items():
        geo_location = geocode(location)
        if geo_location:
            lon = geo_location.longitude
            lat = geo_location.latitude
            
            # Add points to the globe
            point = pv.Sphere(radius=0.5, center=(lon, lat, 0))  # Adjust point size if needed
            plotter.add_mesh(point, color="red", label=f"{location} ({count} jobs)")

    # Configure the globe appearance and interaction
    plotter.view_xz()
    plotter.add_axes()
    
    return plotter

# Streamlit app
st.title("Interactive 3D Job Locations Globe")

# Load and geocode location data
location_data = load_data()

# Create and plot the globe
plotter = plot_job_locations_globe(location_data)

# Render the globe in Streamlit using stpyvista
stpyvista.vtk_render_window(plotter.show(auto_close=False))

