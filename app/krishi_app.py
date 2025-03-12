import streamlit as st
from streamlit_folium import st_folium
import data_processing
import map_generator
from PIL import Image
import os

# File Paths
csv_path = "../data/NepalAgriStats_Cereal.csv"
geojson_path = "../data/nepal-districts.json"
visualization_folder = "../notebooks/" 

# Load Data
df = data_processing.load_data(csv_path)

# Sidebar Navigation
st.sidebar.header("Navigation")
page = st.sidebar.radio("Select Page", ["Map View", "Visualization"])

if page == "Map View":
    # Sidebar options for map filters
    st.sidebar.header("Filter Options")
    selected_year = st.sidebar.selectbox("Select Year", sorted(df["Year"].unique(), reverse=True))
    selected_metric = st.sidebar.radio("Select Metric", ["Yield", "Production", "Area"])

    # Generate Map
    st.subheader(f"Agricultural {selected_metric} Map for {selected_year}")
    folium_map = map_generator.create_map(df, geojson_path, selected_year, selected_metric)
    st_folium(folium_map, width=800, height=600)

elif page == "Visualization":
    st.subheader("Visualizations")

    # Check if the visualization folder exists
    if os.path.exists(visualization_folder):
        image_files = sorted([f for f in os.listdir(visualization_folder) if f.endswith(('.png', '.jpg', '.jpeg'))])

        if image_files:
            for image_file in image_files:
                image_path = os.path.join(visualization_folder, image_file)
                image = Image.open(image_path)

                # Display images one per row
                with st.container():
                    st.image(image, caption=image_file, use_container_width=True)
                    st.write("---")  # Adds a separator for better readability

        else:
            st.write("No saved visualizations found.")
    else:
        st.write("Visualization folder does not exist.")
