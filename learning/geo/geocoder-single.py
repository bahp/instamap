"""

.. note: Other options to investigate

    pgeocode: https://gisgeography.com/geocoders/

"""
# Libraries
import json
import pickle
import geocoder

from pathlib import Path



# Query to google
#g = geocoder.google('Mountain View, CA')

# Query to osm
g = geocoder.osm('Mountain View, CA')

# Results
r1 = g.geojson
r2 = g.json
r3 = g.wkt
r4 = g.osm

# Show
print("Object:")
print(g)
print("\nGEOJSON:")
print(r1)
print("\nJSON:")
print(r2)
print("\nWKT:")
print(r3)
print("\nOSM:")
print(r4)

# Path
path = Path('./outputs/')

# Save
with open(path / 'geocoder_osm.pkl', 'wb') as f:
    pickle.dump(g, f)
with open(path / 'geocoder_osm_geojson.json', 'w') as f:
    json.dump(g.geojson, f, indent=4)
with open(path / 'geocoder_osm_json.json', 'w') as f:
    json.dump(g.json, f, indent=4)
