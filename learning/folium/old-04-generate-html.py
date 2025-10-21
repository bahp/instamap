import os
import json
import glob
import base64
import folium
import requests
import numpy as np

import pymongo
from pathlib import Path

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
    post_url = "https://www.instagram.com/p/{shortcode}/"
    shortcode = row.shortcode
    #thumbnail = open('test/%s/thumbnail.jpg' % shortcode, 'rb').read()
    #encoded = base64.b64encode(thumbnail)

    encoded = ''
    if not pd.isna(row.display_url):
        response = requests.get(row.display_url)
        encoded = base64.b64encode(response.content)
        encoded = encoded.decode('UTF-8')

    # Format
    html = html.format(
        #title=row.location_name,
        title=row.location_name,
        shortcode=shortcode,
        post_url=post_url.format(shortcode=shortcode),
        #display_url=row.display_url,
        encoded=encoded,
        w1=row.addresstype,
        w2=row['class'],
        w3=row['type'],
        w4=shortcode)


    #iframe = folium.IFrame(html)  # , width=400, height=400)
    # return iframe
    # html = folium.Html(html, script=True, width=300).render(),
    return html





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
posts = pd.read_csv('./data/%s/geolocation.csv' % COLLECTION)

# Add colors
#posts['color'] = posts.address
posts['icon'] = None
posts['color'] = posts.addresstype.map(COLORS)
posts['icon'] = posts['class'].map(ICONS)

print(posts.columns)
print(posts[['shortcode', 'importance', 'addresstype', 'class', 'type', 'place_rank']])

# utensils


# Loop adding markers
for index, row in posts.iterrows():

    # Variables
    lat = row.location_lat
    lng = row.location_lng
    tooltip = row.location_name
    html = create_html(row)


    # No latitude found
    if np.isnan(lat) or np.isnan(lng):
        print("%s. Skipping... %s" % (index, row.shortcode))
        continue


    folium.CircleMarker(
        location=[lat, lng],
        radius=10
    )

    """
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
    """


# Save
hmap.save('./data/%s/map.html' % COLLECTION)

# ---------------------------------------------
# Export CSV to manually import in google maps
# ---------------------------------------------

# ---------------------------------------------
# Import in my Google Maps automatically
# ---------------------------------------------


