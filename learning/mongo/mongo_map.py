import os
import json
import glob
import base64
import folium
import requests
import numpy as np
from pathlib import Path
import pymongo

#https://medium.com/datasciencearth/map-visualization-with-folium-d1403771717

def create_html(row):
    """Create popup HTML"""
    html = """
        <div>
            <h5> {title} 
            <span class="float-end">
                <a href="{post_url}" target="_blank"> 
                    <i class="fas fa-link"></i> 
                </a>
            </span>
            </h5> 
             <h6>{w1} {w2} {w3} {w4}</h6>
            <!--<img src="display_url" style="width:100%; height:100%;">-->
            <img src="data:image/png;base64,{encoded}" style="width:100%; height:100%;">
        </div>
    """

    # Variables
    #post_url = "https://www.instagram.com/p/{shortcode}/"
    #shortcode = row.shortcode
    #thumbnail = open('test/%s/thumbnail.jpg' % shortcode, 'rb').read()
    #encoded = base64.b64encode(thumbnail)

    encoded = ''
    #if not pd.isna(row.display_url):
    #    response = requests.get(row.display_url)
    #    encoded = base64.b64encode(response.content)
    #    encoded = encoded.decode('UTF-8')

    # Format
    html = html.format(
        #title=row.location_name,
        title=row.display_name,
        shortcode=row.place_id,
        #post_url=post_url.format(shortcode=row.place_id),
        post_url="https://www.google.com",
        #display_url=row.display_url,
        encoded=1,
        w1=row.addresstype,
        w2=row['class'],
        w3=row['type'],
        w4=3)


    #iframe = folium.IFrame(html)  # , width=400, height=400)
    # return iframe
    # html = folium.Html(html, script=True, width=300).render(),
    return html




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

database.posts_nlp.drop()

aux = database.posts.aggregate([
  {
    "$lookup": {
      "from": "b_post_nlp",
      "localField": "_id",
      "foreignField": "_id",
      "as": "linked_collections"
    }
  },
  {
    "$unwind": "$linked_collections"
  },
  {
    "$project": {
      "feo": 1,
      "is_video": 1,
      "thumbnail_src": 1,
      'bitacora': "$linked_collections.bitacora"
    }
  },
  {
    "$out": "posts_nlp"
  }
])

coll_nlpp = database.get_collection("posts_nlp")


"""
#print("\nCollections:")
#print(database.list_collection_names())
print(aux)
e = coll_nlpp.find({})
for i,(l) in enumerate(e):
    print(i, l)

    if i>10:
        break

print(e)
"""

"""
"name": 1,
"username_twitter": 1,
"user_id_twitter": 1,
"text_twitter": 1,
"page_wikipedia": "$linked_collections.page_wikipedia",
"text_wikipedia": "$linked_collections.text_wikipedia"
"""





# -------------------------
# Configuration
# -------------------------
# Libraries
import pandas as pd

# Initial location
LAT, LNG = 51.20, 38.46

# Create map
hmap = folium.Map(location=[LAT, LNG], zoom_start=3)

COLLECTION = 'test'
COLORS = {
    'historic': 'beige',
    'amenity': 'orange',
    'road': 'gray',
    'country': 'lightgray',
    'city': 'lightgray'
}
ICONS = {
    'historic': 'torii-gate',
    'amenity': 'utensils'
}

# Load posts
posts = pd.read_csv('./geo.csv')

# Add colors
#posts['color'] = posts.address
posts['icon'] = None
posts['color'] = posts.addresstype.map(COLORS)
posts['icon'] = posts['class'].map(ICONS)

#print(posts.columns)
#print(posts[['shortcode', 'importance', 'addresstype', 'class', 'type', 'place_rank']])

# utensils


# Loop adding markers
for index, row in posts.iterrows():

    #break

    # Variables
    lat = row.lat
    lng = row.lon
    tooltip = row.display_name
    html = create_html(row)


    # No latitude found
    if np.isnan(lat) or np.isnan(lng):
        print("%s. Skipping... %s" % (index, "E"))
        continue



    # Add marker
    folium.Marker([lat, lng],
        azy=True, tooltip=tooltip,
        popup=folium.Popup(html,
                         parse_html=False,
                         min_height=400, max_height=400,
                         min_width=300, max_width=300),
        icon=folium.Icon(color=row.color,
                       icon=row.icon,  # 'university'
                       prefix='fa') # angle=angle
        ).add_to(hmap)



# Save
hmap.save('./map.html')

# ---------------------------------------------
# Export CSV to manually import in google maps
# ---------------------------------------------

# ---------------------------------------------
# Import in my Google Maps automatically
# ---------------------------------------------


