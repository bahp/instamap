"""

"""
# Libraries
import json

from pathlib import Path

# Libraries
from geopy.geocoders import Nominatim

path = Path('outputs')

# Create Geolocator
geolocator = Nominatim(timeout=10, user_agent="myGeo")

# ------------------
# Direct query
# ------------------
# Create address
address = '4550 Kester Mill Rd,Winston-Salem,NC'
address = 'igersumbria' # real example returns None
address = 'uk' # real example (weird)
# address = 'france'
address = 'indonesia'
address = 'Pitigliano'

# Query
location = geolocator.geocode(address)

# Show
print("\nLocation:\n%s\n%s" %
      (location, json.dumps(location.raw, indent=4)))


# Save
with open(path / 'geopy_nominatim_direct.json', 'w') as f:
    json.dump(location.raw, f, indent=4)


# -------------
# Reverse query
# -------------
# Create coordinates
coordinates = "40.5180167, 16.0632073"
coordinates = (40.5180167, 16.0632073)

# Query
location = geolocator.reverse(coordinates)

# Show
print("\nReverse:\n%s\n%s" %
      (location, json.dumps(location.raw, indent=4)))

# Save
with open(path / 'geopy_nominatim_reverse.json', 'w') as f:
    json.dump(location.raw, f, indent=4)