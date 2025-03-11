import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium

# Load dataset
@st.cache_data
def load_data():
    df = pd.read_csv("../data/NepalAgriStats_Cereal.csv")
    return df

df = load_data()
df.rename(columns={"DISTRICT_NAME": "District"}, inplace=True)

# Function to get top crop for a district
def get_crop_info(district):
    district_data = df[df["District"] == district]
    if district_data.empty:
        return "No data available", "No climate effects data"
    
    crop_columns = [col for col in df.columns if "_P_" in col]
    top_crop = district_data[crop_columns].sum().idxmax().replace("_P_", "")
    climate_effect = "Climate has X effect on this crop."
    return top_crop, climate_effect

# Streamlit UI
st.title("Nepal Crop Production Map 🌾")
st.write("Click on a district to see its crop production insights.")

# Create Nepal map with Folium
nepal_map = folium.Map(location=[28.3949, 84.1240], zoom_start=7)

# Sample districts
districts = {
    "Kathmandu": [27.7172, 85.3240],
    "Lalitpur": [27.6667, 85.3333],
    "Bhaktapur": [27.6710, 85.4298]
}

for district, coords in districts.items():
    folium.Marker(
        location=coords,
        popup=district,
        tooltip=f"Click to see data for {district}",
    ).add_to(nepal_map)

st_folium(nepal_map)  # Use st_folium instead of folium_static

# Select district
district_selected = st.selectbox("Select a District:", list(districts.keys()))

# Show crop insights
if district_selected:
    top_crop, climate_effect = get_crop_info(district_selected)
    st.subheader(f"Top Crop in {district_selected}: {top_crop}")
    st.write(f"Climate Impact: {climate_effect}")
