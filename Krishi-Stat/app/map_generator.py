import folium
import json
import pandas as pd
from shapely.geometry import shape

def standardize_geojson_districts(geojson_path):
    """Loads the GeoJSON file and ensures district names are standardized."""
    with open(geojson_path, "r", encoding="utf-8") as f:
        geojson_data = json.load(f)
    
    for feature in geojson_data["features"]:
        feature["properties"]["DISTRICT"] = feature["properties"]["DISTRICT"].upper().strip()
    
    return geojson_data

def extract_district_centroids(geojson_data):
    """Extracts district centroids from GeoJSON and returns a dictionary."""
    district_centroids = {}
    for feature in geojson_data["features"]:
        district_name = feature["properties"]["DISTRICT"]
        polygon = shape(feature["geometry"])  # Convert to Geometry
        centroid = polygon.centroid  # Get Centroid
        district_centroids[district_name] = (centroid.y, centroid.x)  # (LAT, LON)
    
    return district_centroids

def create_map(df, geojson_path, selected_crop, selected_year, selected_metric):
    """Creates an interactive Folium map with agricultural data popups."""

    # Load and standardize GeoJSON
    geojson_data = standardize_geojson_districts(geojson_path)

    # Extract centroids for district locations
    district_centroids = extract_district_centroids(geojson_data)

    # Filter dataset based on user selections
    df_filtered = df[(df["Year"] == selected_year) & (df["Crop"] == selected_crop)]

    metric_column = {"Yield": "Yield", "Production": "Production", "Area": "Area"}[selected_metric]

    # Create base map
    m = folium.Map(location=[28.3949, 84.1240], zoom_start=7, control_scale=True)

    # Add Choropleth Layer
    folium.Choropleth(
        geo_data=geojson_data,
        name="choropleth",
        data=df_filtered,
        columns=["DISTRICT_NAME", metric_column],
        key_on="feature.properties.DISTRICT",
        fill_color="YlGnBu",
        fill_opacity=0.7,
        line_opacity=0.3,
        legend_name=f"{selected_metric} for {selected_crop} in {selected_year}",
        control=True
    ).add_to(m)

    # Indentation and attaching popups
    for feature in geojson_data["features"]:
        district_name = feature["properties"]["DISTRICT"]
        district_data = df_filtered[df_filtered["DISTRICT_NAME"] == district_name]

        # Default Text If No Data Found
        popup_text = f"<b>{district_name}</b><br>No Data Available"
        if not district_data.empty:
            row = district_data.iloc[0]
            popup_text = f"""
            <b>{district_name}</b><br>
            Crop: {row['Crop']}<br>
            Yield: {row['Yield']} tons/ha<br>
            Production: {row['Production']} tons<br>
            Area: {row['Area']} ha
            """

        #  (Hover + Click)
        geojson_layer = folium.GeoJson(
            feature,
            tooltip=folium.GeoJsonTooltip(fields=["DISTRICT"], aliases=["District:"]),
            style_function=lambda x: {"fillOpacity": 0.5, "color": "black", "weight": 1},
            highlight_function=lambda x: {"fillOpacity": 0.8, "color": "red", "weight": 2},
        ).add_to(m)

        #  Attach Popup to the GeoJSON layer
        folium.Popup(popup_text, max_width=300).add_to(geojson_layer)
        
        

    return m
