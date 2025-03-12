import folium
import json
from shapely.geometry import shape

# def extract_districts_centroids(geojson_path):
#     """Extracts centroids of districts from GeoJSON file."""
    
#     with open(geojson_path, "r", encoding="utf-8") as f:
#         nepal_geojson = json.load(f)

#     district_centroids = {}
#     for feature in nepal_geojson["features"]:
#         district_name = feature["properties"]["DISTRICT"].upper().strip()  # Standardize name
#         polygon = shape(feature["geometry"])  # Convert to geometry
#         centroid = polygon.centroid  # Get centroid

#         district_centroids[district_name] = (centroid.y, centroid.x)  # (LAT, LON)

#     return district_centroids
def standardize_geojson_districts(geojson_path):
    """Loads the GeoJSON file and ensures district names are standardized."""
    with open(geojson_path, "r", encoding="utf-8") as f:
        geojson_data = json.load(f)

    for feature in geojson_data["features"]:
        feature["properties"]["DISTRICT"] = feature["properties"]["DISTRICT"].upper().strip()

    return geojson_data  

def create_map(df, geojson_path, selected_year, selected_metric):
    """Creates an interactive Folium map with agricultural data popups."""
    
    # district_centroids = extract_districts_centroids(geojson_path)
    with open(geojson_path, "r", encoding="utf-8") as f:
        geojson_data= json.load(f)
    
    


    df_filtered= df[(df["Year"]==selected_year)]
    metric_column = {"Yield": "Yield", "Production": "Production", "Area": "Area"}[selected_metric]
    m = folium.Map(location=[28.3949, 84.1240], zoom_start=7)
    
    geojson_data = standardize_geojson_districts(geojson_path)
       # Choropleth
    folium.Choropleth(
        geo_data=geojson_data,
        name="choropleth",
        data=df_filtered,
        columns=["DISTRICT_NAME", metric_column],
        key_on="feature.properties.DISTRICT",
        fill_color="YlGnBu",
        fill_opacity=0.7,
        line_opacity=0.2,
        legend_name=f"{selected_metric} in {selected_year}"
    ).add_to(m)

    # Add popups with details
    for _, row in df_filtered.iterrows():
        district_name = row["DISTRICT_NAME"]
        popup_text = f"""
        <b>{district_name}</b><br>
        Yield: {row['Yield']} tons/ha<br>
        Production: {row['Production']} tons<br>
        Area: {row['Area']} ha
        """
        folium.Marker(location=[28.5, 84.0], popup=popup_text).add_to(m)

    return m