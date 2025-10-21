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
path = Path('./data/bernardhp/data/')

# Results
results = pd.DataFrame()
results = []

# Load geo-locations
with open(path / '_geolocations.json') as f:
    geo = json.load(f)

# Load posts
with open(path / '_posts.json') as f:
    posts = json.load(f)



# Loop
# for f in glob.glob('%s/**/geo_nominatim.json' % path , recursive=False):
entries = pd.DataFrame()

for f in glob.glob(str(path / '**/fair_ner.json'), recursive=False):
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
             <button id='boff-{boff}' class="btn btn-primary" type="button" data-bs-toggle="offcanvas" data-bs-target="#offcanvasRight" aria-controls="offcanvasRight">Toggle right offcanvas</button>
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
        boff=shortcode,
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


from src.utils.html import template_v5


# Initial location
LAT, LNG = 51.20, 38.46

# Create map
hmap = folium.Map(location=[LAT, LNG], zoom_start=3)

from jinja2 import Template
from folium.map import Marker
# Modify Marker template to include the onClick event
click_template = """{% macro script(this, kwargs) %}
    var {{ this.get_name() }} = L.marker(
        {{ this.location|tojson }},
        {{ this.options|tojson }}
    ).addTo({{ this._parent.get_name() }}).on('click', onClick);
{% endmacro %}"""

# Change template to custom template
Marker._template = Template(click_template)



"""
with open('./data/bernardhp/_geolocations.json') as f:
    aux = json.load(f)

print(aux)

raw = [v['raw'] for k,v in aux.items() if v is not None]
df = pd.DataFrame(raw)
print(raw)
print(df)
print(df.columns)

print(df['class'].unique())
print(df['type'].unique())
print(df['addresstype'].unique())
df = df[['class', 'type', 'addresstype']]
df = df.drop_duplicates()
print(df)
"""

"""
  class            type     addresstype
0      place            city            city
1   boundary  administrative         country
2   boundary  administrative           state
4   boundary  administrative            city
8   boundary  administrative        province
13   tourism      alpine_hut         tourism
21     place         village         village
22  boundary  administrative  administrative
23     place        province        province
25     place         quarter         quarter
26  boundary  administrative          suburb
27     place          suburb          suburb
31     place            town            town
34   highway      pedestrian            road
35  boundary  administrative            town
36  boundary  administrative         village
37   leisure            park            park
41     place          square          square
42  boundary  administrative          county
43   amenity           clock         amenity
45  boundary  administrative          region
46     craft         caterer           craft

import sys
sys.exit()
"""

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


# Loop drawing instagram posts
for index, row in aux.iterrows():

    print(row)

    with open(path / row.shortcode / 'post.json') as f:
        p = json.load(f)

    print(p)
    print(row)
    print(row.raw)
    print(row.raw.keys())
    row['thumbnail'] = p['thumbnail_src']

    # Variables
    lat = row.latitude
    lng = row.longitude
    tooltip = row.text
    #html = create_html(row)
    html = template_v5(title=row.text, subtitle=shortcode, shortcode=shortce)

    color = COLORS.get(row.raw['addresstype'], 'gray')
    icon = ICONS.get(row.raw['class'], None)
    """
    # posts['color'] = posts.address
    posts['icon'] = None
    posts['color'] = posts.addresstype.map(COLORS)
    posts['icon'] = posts['class'].map(ICONS)
    """

    # No latitude found
    if np.isnan(lat) or np.isnan(lng):
        print("%s. Skipping... %s" % (index, row.shortcode))
        continue

    # folium.CircleMarker(
    #    location=[lat, lng],
    #    radius=10
    # )
    folium.Circle(radius=4, fill_color="orange", fill_opacity=0.4, color="black", weight=1).add_to(hmap)

    # Add marker
    folium.Marker([lat, lng],
                  name=row.shortcode,
                  azy=True, tooltip=tooltip,
                  popup=folium.Popup(html,
                                     parse_html=False, lazy=True,
                                     min_height=400, max_height=400,
                                     min_width=300, max_width=300),
                  icon=folium.Icon(color=color, #'blue',  # row.color,
                                   icon='university',  # row.icon,  # 'university'
                                   prefix='fa')  # angle=angle
                  ).add_to(hmap)


embed = """
  <blockquote class="instagram-media" data-instgrm-captioned data-instgrm-permalink="https://www.instagram.com/p/{shortcode}/?utm_source=ig_embed&amp;utm_campaign=loading" data-instgrm-version="14" style=" background:#FFF; border:0; border-radius:3px; box-shadow:0 0 1px 0 rgba(0,0,0,0.5),0 1px 10px 0 rgba(0,0,0,0.15); margin: 1px; max-width:540px; min-width:326px; padding:0; width:99.375%; width:-webkit-calc(100% - 2px); width:calc(100% - 2px);"><div style="padding:16px;"> <a href="https://www.instagram.com/p/CymAX_8qiEu/?utm_source=ig_embed&amp;utm_campaign=loading" style=" background:#FFFFFF; line-height:0; padding:0 0; text-align:center; text-decoration:none; width:100%;" target="_blank"> <div style=" display: flex; flex-direction: row; align-items: center;"> <div style="background-color: #F4F4F4; border-radius: 50%; flex-grow: 0; height: 40px; margin-right: 14px; width: 40px;"></div> <div style="display: flex; flex-direction: column; flex-grow: 1; justify-content: center;"> <div style=" background-color: #F4F4F4; border-radius: 4px; flex-grow: 0; height: 14px; margin-bottom: 6px; width: 100px;"></div> <div style=" background-color: #F4F4F4; border-radius: 4px; flex-grow: 0; height: 14px; width: 60px;"></div></div></div><div style="padding: 19% 0;"></div> <div style="display:block; height:50px; margin:0 auto 12px; width:50px;"><svg width="50px" height="50px" viewBox="0 0 60 60" version="1.1" xmlns="https://www.w3.org/2000/svg" xmlns:xlink="https://www.w3.org/1999/xlink"><g stroke="none" stroke-width="1" fill="none" fill-rule="evenodd"><g transform="translate(-511.000000, -20.000000)" fill="#000000"><g><path d="M556.869,30.41 C554.814,30.41 553.148,32.076 553.148,34.131 C553.148,36.186 554.814,37.852 556.869,37.852 C558.924,37.852 560.59,36.186 560.59,34.131 C560.59,32.076 558.924,30.41 556.869,30.41 M541,60.657 C535.114,60.657 530.342,55.887 530.342,50 C530.342,44.114 535.114,39.342 541,39.342 C546.887,39.342 551.658,44.114 551.658,50 C551.658,55.887 546.887,60.657 541,60.657 M541,33.886 C532.1,33.886 524.886,41.1 524.886,50 C524.886,58.899 532.1,66.113 541,66.113 C549.9,66.113 557.115,58.899 557.115,50 C557.115,41.1 549.9,33.886 541,33.886 M565.378,62.101 C565.244,65.022 564.756,66.606 564.346,67.663 C563.803,69.06 563.154,70.057 562.106,71.106 C561.058,72.155 560.06,72.803 558.662,73.347 C557.607,73.757 556.021,74.244 553.102,74.378 C549.944,74.521 548.997,74.552 541,74.552 C533.003,74.552 532.056,74.521 528.898,74.378 C525.979,74.244 524.393,73.757 523.338,73.347 C521.94,72.803 520.942,72.155 519.894,71.106 C518.846,70.057 518.197,69.06 517.654,67.663 C517.244,66.606 516.755,65.022 516.623,62.101 C516.479,58.943 516.448,57.996 516.448,50 C516.448,42.003 516.479,41.056 516.623,37.899 C516.755,34.978 517.244,33.391 517.654,32.338 C518.197,30.938 518.846,29.942 519.894,28.894 C520.942,27.846 521.94,27.196 523.338,26.654 C524.393,26.244 525.979,25.756 528.898,25.623 C532.057,25.479 533.004,25.448 541,25.448 C548.997,25.448 549.943,25.479 553.102,25.623 C556.021,25.756 557.607,26.244 558.662,26.654 C560.06,27.196 561.058,27.846 562.106,28.894 C563.154,29.942 563.803,30.938 564.346,32.338 C564.756,33.391 565.244,34.978 565.378,37.899 C565.522,41.056 565.552,42.003 565.552,50 C565.552,57.996 565.522,58.943 565.378,62.101 M570.82,37.631 C570.674,34.438 570.167,32.258 569.425,30.349 C568.659,28.377 567.633,26.702 565.965,25.035 C564.297,23.368 562.623,22.342 560.652,21.575 C558.743,20.834 556.562,20.326 553.369,20.18 C550.169,20.033 549.148,20 541,20 C532.853,20 531.831,20.033 528.631,20.18 C525.438,20.326 523.257,20.834 521.349,21.575 C519.376,22.342 517.703,23.368 516.035,25.035 C514.368,26.702 513.342,28.377 512.574,30.349 C511.834,32.258 511.326,34.438 511.181,37.631 C511.035,40.831 511,41.851 511,50 C511,58.147 511.035,59.17 511.181,62.369 C511.326,65.562 511.834,67.743 512.574,69.651 C513.342,71.625 514.368,73.296 516.035,74.965 C517.703,76.634 519.376,77.658 521.349,78.425 C523.257,79.167 525.438,79.673 528.631,79.82 C531.831,79.965 532.853,80.001 541,80.001 C549.148,80.001 550.169,79.965 553.369,79.82 C556.562,79.673 558.743,79.167 560.652,78.425 C562.623,77.658 564.297,76.634 565.965,74.965 C567.633,73.296 568.659,71.625 569.425,69.651 C570.167,67.743 570.674,65.562 570.82,62.369 C570.966,59.17 571,58.147 571,50 C571,41.851 570.966,40.831 570.82,37.631"></path></g></g></g></svg></div><div style="padding-top: 8px;"> <div style=" color:#3897f0; font-family:Arial,sans-serif; font-size:14px; font-style:normal; font-weight:550; line-height:18px;">Ver esta publicación en Instagram</div></div><div style="padding: 12.5% 0;"></div> <div style="display: flex; flex-direction: row; margin-bottom: 14px; align-items: center;"><div> <div style="background-color: #F4F4F4; border-radius: 50%; height: 12.5px; width: 12.5px; transform: translateX(0px) translateY(7px);"></div> <div style="background-color: #F4F4F4; height: 12.5px; transform: rotate(-45deg) translateX(3px) translateY(1px); width: 12.5px; flex-grow: 0; margin-right: 14px; margin-left: 2px;"></div> <div style="background-color: #F4F4F4; border-radius: 50%; height: 12.5px; width: 12.5px; transform: translateX(9px) translateY(-18px);"></div></div><div style="margin-left: 8px;"> <div style=" background-color: #F4F4F4; border-radius: 50%; flex-grow: 0; height: 20px; width: 20px;"></div> <div style=" width: 0; height: 0; border-top: 2px solid transparent; border-left: 6px solid #f4f4f4; border-bottom: 2px solid transparent; transform: translateX(16px) translateY(-4px) rotate(30deg)"></div></div><div style="margin-left: auto;"> <div style=" width: 0px; border-top: 8px solid #F4F4F4; border-right: 8px solid transparent; transform: translateY(16px);"></div> <div style=" background-color: #F4F4F4; flex-grow: 0; height: 12px; width: 16px; transform: translateY(-4px);"></div> <div style=" width: 0; height: 0; border-top: 8px solid #F4F4F4; border-left: 8px solid transparent; transform: translateY(-4px) translateX(8px);"></div></div></div> <div style="display: flex; flex-direction: column; flex-grow: 1; justify-content: center; margin-bottom: 24px;"> <div style=" background-color: #F4F4F4; border-radius: 4px; flex-grow: 0; height: 14px; margin-bottom: 6px; width: 224px;"></div> <div style=" background-color: #F4F4F4; border-radius: 4px; flex-grow: 0; height: 14px; width: 144px;"></div></div></a><p style=" color:#c9c8cd; font-family:Arial,sans-serif; font-size:14px; line-height:17px; margin-bottom:0; margin-top:8px; overflow:hidden; padding:8px 0 7px; text-align:center; text-overflow:ellipsis; white-space:nowrap;"><a href="https://www.instagram.com/p/CymAX_8qiEu/?utm_source=ig_embed&amp;utm_campaign=loading" style=" color:#c9c8cd; font-family:Arial,sans-serif; font-size:14px; font-style:normal; font-weight:normal; line-height:17px; text-decoration:none;" target="_blank">Una publicación compartida por Scandinavia (@scandinavia.explore)</a></p></div></blockquote> <script async src="https://www.instagram.com/embed.js"></script>

"""

print(embed.format(shortcode='guapo'))

# Include child with the overlay sidebar.
hmap.get_root().html.add_child(
    folium.Element("""
        <script async src="https://www.instagram.com/embed.js"></script>
        <div class="offcanvas offcanvas-end" 
            tabindex="-1" 
            id="offcanvasRight" 
            aria-labelledby="offcanvasRightLabel">
            <div class="offcanvas-header">
                <h5 id='post-shortcode'><h5>
                <button type="button" 
                    class="btn-close text-reset" 
                    data-bs-dismiss="offcanvas" 
                    aria-label="Close">
                </button>
            </div>
            <div id='offcanvas-body' class="offcanvas-body">
                 <div id='post-embed'></div>
            </div>
        </div>
    """)
)

# Create the onClick listener function as a branca element and add to the map html
click_js = """function onClick(e) {
             
     var shortcode = e.target.options.name;
     //var b = $( "#boff-" + shortcode ).trigger( "click" );
    
     //$( "#boff-" + shortcode ).click();
     //console.log(e.target.options.name); alert('feo');
     var embed = '<blockquote class="instagram-media" data-instgrm-captioned data-instgrm-permalink="https://www.instagram.com/p/' + shortcode + '/?utm_source=ig_embed&amp;utm_campaign=loading" data-instgrm-version="14" style="width:100%;"></blockquote>'
     console.log(embed);
     document.getElementById('post-shortcode').innerHTML = shortcode;
     $('#post-embed').html(embed)
     window.instgrm.Embeds.process()
     $('#post-sidebar-' + shortcode).trigger('click')
}"""

e = folium.Element(click_js)
html = hmap.get_root()
html.script.get_root().render()
html.script._children[e.get_name()] = e


# Save
hmap.save(path.parent / 'map-offside.html')