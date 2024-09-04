import streamlit as st
import folium
from streamlit_folium import st_folium
from models import (free_space_path_loss, rain_attenuation, gas_attenuation, fog_attenuation,
                    close_in_path_loss, longley_rice_path_loss, tirem_path_loss, ray_tracing_path_loss)

def create_map(location):
    m = folium.Map(location=location, zoom_start=13)
    return m

def update_map_with_coverage(map_obj, location, path_loss, distance):
    radius = min(50, distance)
    folium.CircleMarker(
        location=location,
        radius=radius,
        color='blue',
        fill=True,
        fill_color='blue',
        fill_opacity=0.5,
        popup=f"Path Loss: {path_loss:.2f} dB"
    ).add_to(map_obj)
    return map_obj

# Initialize session state for the map
if 'coverage_map' not in st.session_state:
    st.session_state.coverage_map = create_map([39.92, 32.86])  # Default location (Ankara)

st.title("RF Propagation - Coverage Tool")

# Propagation model selection
model = st.selectbox("Propagation Model", ["Free Space", "Rain", "Gas", "Fog", "CloseIn", "LongleyRice", "TIREM", "RayTracing"])

# User inputs
freq = st.number_input("Frequency (MHz)", min_value=0, value=900)
antenna_height = st.slider("Antenna Height (m)", min_value=0, max_value=100, value=10)
latitude = st.number_input("Latitude", format="%.6f", value=37.7749)
longitude = st.number_input("Longitude", format="%.6f", value=-122.4194)
altitude = st.number_input("Altitude (m)", min_value=0, value=0)
distance = st.slider("Distance (km)", min_value=0, max_value=50, value=10)

# Update location
location = [latitude, longitude]

# Calculate button
if st.button("Calculate Coverage"):
    if model == "Free Space":
        path_loss = free_space_path_loss(freq, distance)
    elif model == "Rain":
        rain_rate = st.slider("Rain Rate (mm/h)", min_value=0, max_value=50, value=25)
        path_loss = rain_attenuation(freq / 1000, distance, rain_rate)
    elif model == "Gas":
        path_loss = gas_attenuation(freq / 1000, distance)
    elif model == "Fog":
        fog_density = st.slider("Fog Density (g/m³)", min_value=0, max_value=1, value=0.5)
        path_loss = fog_attenuation(freq / 1000, distance, fog_density)
    elif model == "CloseIn":
        path_loss = close_in_path_loss(freq, distance)
    elif model == "LongleyRice":
        terrain_type = st.selectbox("Terrain Type", ["average", "hilly", "mountainous"])
        path_loss = longley_rice_path_loss(freq, distance, terrain_type)
    elif model == "TIREM":
        terrain_type = st.selectbox("Terrain Type", ["average", "hilly", "mountainous"])
        path_loss = tirem_path_loss(freq, distance, terrain_type)
    elif model == "RayTracing":
        environment = st.selectbox("Environment", ["urban", "rural"])
        path_loss = ray_tracing_path_loss(freq / 1000, distance, environment)
    
    st.write(f"Path Loss: {path_loss:.2f} dB")
    
    # Update the map in session state
    st.session_state.coverage_map = update_map_with_coverage(st.session_state.coverage_map, location, path_loss, distance)

# Display the map
st_folium(st.session_state.coverage_map, width=700, height=500)
