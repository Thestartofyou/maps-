import geopandas as gpd
import folium
import rasterio
from rasterio.plot import show

# Sample data: Parcel ID, Zoning, Acreage, and Geometry (Point or Polygon)
data = {
    'Parcel_ID': [1, 2, 3],
    'Zoning': ['Residential', 'Commercial', 'Industrial'],
    'Acreage': [2.5, 1.0, 5.0],
    'geometry': [
        Point(-77.0369, 38.8951),  # Replace with actual coordinates
        Point(-77.0451, 38.8895),
        Point(-77.0522, 38.8845)
    ]
}

# Create a GeoDataFrame
gdf = gpd.GeoDataFrame(data, geometry='geometry')

# Load topographic data (replace 'path/to/topo.tif' with your actual file path)
topo_path = 'path/to/topo.tif'
topo_data = rasterio.open(topo_path)

# Create a base map
m = folium.Map(location=[38.8951, -77.0369], zoom_start=12)  # Centered around Washington, DC

# Add GeoJSON data to the map
folium.GeoJson(gdf.to_json(), name='geojson').add_to(m)

# Add popup information for each feature
for idx, row in gdf.iterrows():
    popup_text = f"Parcel ID: {row['Parcel_ID']}<br>Zoning: {row['Zoning']}<br>Acreage: {row['Acreage']} acres"
    folium.Marker(location=[row['geometry'].y, row['geometry'].x], popup=popup_text).add_to(m)

# Add topographic layer to the map
folium.raster_layers.ImageOverlay(
    image=topo_data.read(1),
    bounds=[[topo_data.bounds.bottom, topo_data.bounds.left], [topo_data.bounds.top, topo_data.bounds.right]],
    colormap=lambda x: (0, 0, 0, x),  # Adjust the colormap as needed
).add_to(m)

# Save the map as an HTML file
m.save('gis_map_with_topo.html')

