import folium
import json

# (This code would go after the code above)
# Assume 'all_locations_data' exists

filename = 'locations_data.json'
with open(filename, 'r') as file:
    # Use json.load() to parse the file object
    all_locations_data = json.load(file)

# Create a map centered on the first location
m = folium.Map(location=[
    all_locations_data[0]['lat'], all_locations_data[0]['lon']], zoom_start=10)

# Loop through your new data and add pins
for loc in all_locations_data:
    if loc['lat'] is not None and loc['lon'] is not None:
        folium.Marker(
            location=[loc['lat'], loc['lon']],
            popup=f"<strong>{loc['title']}</strong><br>{loc['subtitle']}",
            tooltip=loc['title']
        ).add_to(m)

# Save the map
m.save("my_travel_map.html")
print("\nMap created! Open 'my_travel_map.html' in your browser.")