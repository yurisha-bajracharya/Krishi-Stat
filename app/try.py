import streamlit as st
from streamlit_folium import st_folium
from Script import data_processing
from Script import map_generator

# File Paths
csv_path = "district/NepalAgriStats_Cereal.csv"
geojson_path = "geojson/nepal-districts.geojson"

# Load Data
df = data_processing.load_data(csv_path)

# Sidebar options
st.sidebar.header("Filter Options")
selected_year = st.sidebar.selectbox("Select Year", sorted(df["Year"].unique(), reverse=True))
selected_metric = st.sidebar.radio("Select Metric", ["Yield", "Production", "Area"])

# Generate Map
st.subheader(f"Agricultural {selected_metric} Map for {selected_year}")
folium_map = map_generator.create_map(df, geojson_path, selected_year, selected_metric)
st.components.v1.html(folium_map._repr_html_(), height=600) 