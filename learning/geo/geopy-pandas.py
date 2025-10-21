"""

 See: https://gis.stackexchange.com/questions/427341/reverse-geocoding-of-pandas-dataframe-with-lat-long-columns

"""
# Libraries
import pandas as pd
from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter
from functools import partial
from tqdm import tqdm

# Activate
tqdm.pandas()

def get_geolocations(s, reverse=False):
    """

    Parameters
    :param G:
    :return:
    """
    # Create Geolocator
    geolocator = Nominatim(timeout=10, user_agent="myGeo")
    method = geolocator.reverse if reverse else geolocator.geocode
    method = RateLimiter(method, min_delay_seconds=1)

    # Compute the geographical locations
    return s.progress_apply(partial(method, language='en'))


# Create GeoLocator
geolocator = Nominatim(timeout=10, user_agent="myGeo")
method = RateLimiter(geolocator.geocode, min_delay_seconds=1)
#method = RateLimiter(geolocator.reverse, min_delay_seconds=1)

# Create dataFrame
df = pd.DataFrame(data=[
    ['Padova, Italy'],
    ['Madrid, Spain'],
    ['Tower Eiffel, Paris, France']
], columns=['address'])

# .. note: The result on each cell is an object. This object
#          has a <raw> attribute which contains a dictionary
#          with the information.
r = get_geolocations(df.address, reverse=False)

# Create DataFrame with columns
locations = pd.json_normalize(
    r.apply(lambda x: x.raw if x else {})
)

# Combine
df = df.join(locations)

# Show results
print(df.T)