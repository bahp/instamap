"""
"""

# Libraries
import re
import json
import glob
import pandas as pd

from src.utils.ner import NERFlair
from pathlib import Path

# Path
path = Path('./data/bernardhp/')

# Results
results = pd.DataFrame()
results = []

# Load GeoLocations
with open(path / '_geolocations.json') as f:
    geo = json.load(f)

# Load Instagrm posts
with open(path / '_posts.json') as f:
    posts = json.load(f)

# Loop
# for f in glob.glob('%s/**/geo_nominatim.json' % path , recursive=False):
entries = pd.DataFrame()

for f in glob.glob('%s/posts/**/fair_ner.json' % path, recursive=False):
    print(f)
    # Load file
    with open(f, "r") as file:
        data = json.load(file)

    # Get entities
    entities = NERFlair().entities_to_dataframe(data)
    entities['shortcode'] = str(Path(f).parent.stem)

    if entities.empty:
        continue

    # Define which entities to keep
    entities = entities.drop_duplicates(subset=['text'])
    entities = entities[entities.value.isin(['LOC'])]
    if entities.empty:
        continue
    entities = entities.sort_values(by=['confidence'], ascending=False)
    if entities.empty:
        continue
    entities = entities[entities.confidence > 0.7]
    if entities.empty:
        continue

    # entities = entities.groupby(by='shortcode').head(1)  # Just for testing
    # entities = entities.head(2)
    # entities = entities.reset_index(drop=True)
    # entities = entities.set_index('text')

    # Include
    entries = pd.concat([entries, entities])


g = pd.DataFrame(geo)
g = g.T

print(g)
print(entries)


aux = entries.merge(g, how='left', left_on='text', right_on=g.index)

aux = aux.dropna(how='any', subset=['latitude', 'longitude'])


import base64
import folium
import requests
import numpy as np


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
             <button class="btn btn-primary" type="button" data-bs-toggle="offcanvas" data-bs-target="#offcanvasRight" aria-controls="offcanvasRight">Toggle right offcanvas</button>
             <!--<iframe src="https://www.instagram.com/p/CyGDGR3sv7z/"></iframe>-->

            <!--<img src="display_url" style="width:100%; height:100%;">-->
            <!--<img src="data:image/png;base64,{encoded}" style="width:100%; height:100%;">-->
        </div>
    """

    # Variables
    post_url = "https://www.instagram.com/p/{shortcode}/"
    shortcode = row.shortcode
    # thumbnail = open('test/%s/thumbnail.jpg' % shortcode, 'rb').read()
    # encoded = base64.b64encode(thumbnail)

    encoded = ''
    if not pd.isna(row.thumbnail):
        response = requests.get(row.thumbnail)
        encoded = base64.b64encode(response.content)
        encoded = encoded.decode('UTF-8')

    print(encoded)

    # Format
    html = html.format(
        # title=row.location_name,
        # title=row.location_name,
        title='Test',
        shortcode=shortcode,
        post_url=post_url.format(shortcode=shortcode),
        display_url=row.thumbnail,
        encoded=encoded,
        # w1=row.addresstype,
        # w2=row['class'],
        # w3=row['type'],
        w1=1, w2=2, w3=3,
        w4=shortcode)

    # iframe = folium.IFrame(html)  # , width=400, height=400)
    # return iframe
    # html = folium.Html(html, script=True, width=300).render(),
    return html


# Initial location
LAT, LNG = 51.20, 38.46

# Create map
hmap = folium.Map(location=[LAT, LNG], zoom_start=3)


# Loop drawing instagram posts
for index, row in aux.iterrows():

    print(row)

    with open(path / 'posts' / row.shortcode / 'post.json') as f:
        p = json.load(f)

    print(p)
    print(row)
    row['thumbnail'] = p['thumbnail_src']

    # Variables
    lat = row.latitude
    lng = row.longitude
    tooltip = row.text
    html = create_html(row)

    # No latitude found
    if np.isnan(lat) or np.isnan(lng):
        print("%s. Skipping... %s" % (index, row.shortcode))
        continue

    # folium.CircleMarker(
    #    location=[lat, lng],
    #    radius=10
    # )

    # Add marker
    folium.Marker([lat, lng],
                  azy=True, tooltip=tooltip,
                  popup=folium.Popup(html,
                                     parse_html=False,
                                     min_height=400, max_height=400,
                                     min_width=300, max_width=300),
                  icon=folium.Icon(color='blue',  # row.color,
                                   icon='university',  # row.icon,  # 'university'
                                   prefix='fa')  # angle=angle
                  ).add_to(hmap)

# Save
hmap.save(path / 'map-simple.html')