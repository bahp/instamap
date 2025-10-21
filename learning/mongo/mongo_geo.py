# Libraries
import re
import json
import pymongo
import pandas as pd
# -----------------------------------------------------
# Main
# -----------------------------------------------------
# Create client
client = pymongo.MongoClient('mongodb://localhost:27017')

# Create database
database = client['bitacora_insta_db']

# Show
print("\nCollections:")
print(database.list_collection_names())

# Get collection weekly_demand
coll_posts = database.get_collection("posts")
coll_nlp = database.get_collection("b_post_nlp")



#database.b_post_nlp.drop()
#print("Delete collection")

print("Total posts: %s" % coll_posts.count_documents({}))
print("Total NLP entries: %s" % coll_nlp.count_documents({}))

posts = coll_nlp.find({})

#posts = list(posts)
#print(posts)


bitacora = [p['bitacora']['top_entity'] for p in posts]

#for p in posts:
#    print(p['_id'], p['bitacora']['top_entity'])


df = pd.DataFrame(bitacora)
df['text'] = df['text'].str.lower()
print(df)
v = df['text'].value_counts()
print(v)
print(v.sum())
v.to_csv('count_entities')


#geo = pd.read_csv('geo.csv')
#geo['text'] = v.index

#print(v)
#print(geo)


#import sys
#sys.exit()


import pandas as pd
from functools import partial
from tqdm import tqdm

# Geopy
from geopy.geocoders import Nominatim
from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter

tqdm.pandas()

# -------------------------------------------------------------------
# Methods
# -------------------------------------------------------------------
def get_geolocations(s, reverse=False, as_dataframe=False):
    """

    Parameters
    :param G:
    :return:
    """
    # Create Geolocator
    geolocator = Nominatim(timeout=10, user_agent="myGeo")
    method = geolocator.reverse if reverse else geolocator.geocode
    method = RateLimiter(method, min_delay_seconds=1)

    print(s)

    # Compute geolocations
    r = s.progress_apply(partial(method, language='en'))
    print(r)

    # Convert to dataframe
    if as_dataframe:
       s = r.apply(lambda x: x.raw if x else None)
       #s = s.reset_index(drop=False)
       #print(s)
       df = pd.json_normalize(s, sep='_')
       df['text'] = s.index
       print(df)
       return df

    # Return
    return r


v = v.take([1, 5])
v = v.index.to_series()

print(type(v))

result = get_geolocations(v, as_dataframe=True)

result.to_csv('geo.csv')
result.to_json('geo.json', orient='records')


"""
 from geopy import geocoders

 gn = geocoders.Google()
 place, (lat, lng) = gn.geocode("istanbul")
 print place
"""