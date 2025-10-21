
import os
import json
import glob
import base64
import folium
from pathlib import Path

def find_node_location(data):
    try:
        v1 = data['_node']['location']
        #print(json.dumps(v1, indent=4))
        return v1
    except Exception as e:
        return None

def find_user_location(data):
    try:
        v2 = data['_node']['iphone_struct']['location']
        #print("_node/iphone_struct/user/location")
        #print(json.dumps(v2, indent=4))
        return v2
    except Exception as e:
        print(e)

def find_text_location():
    pass

def find_locations(data):
    """"""
    # Finding node location
    coordinates_node = find_node_location(data)
    # Finding user location
    #coordinates_user = find_user_location(data)

    # Find locations using the name of the street, city, ...
    # linked with the google API.

    # Return
    return coordinates_node



def popup_v3(data):
    """Insert link to image"""
    shortcode = data['_node']['shortcode']

    #images = []
    #for f in glob.glob(':saved/%s/*.jpg' % shortcode):
    #    images.append(f)
    #encoded = base64.b64encode(open(images[0], 'rb').read())
    print("Aaaaa")
    print('test/%s/thumbnail.jpg'%shortcode)

    encoded = base64.b64encode(open('test/%s/thumbnail.jpg'%shortcode, 'rb').read())


    html = """
        <div>
            <h5> {title} 
            <span class="float-end">
                <a href="https://www.instagram.com/p/{shortcode}/ target="_blank"> <i class="fas fa-link"></i> </a>
            </span>
            </h5> 
            
            <img src="data:image/png;base64,{bin}" style="width:100%; height:100%;">
        </div>
    """
    #style="width:100px;height:100px"
    html = html.format(
        #title=data['_node']['iphone_struct']['location']['short_name'],
        #title=data['_node']['iphone_struct']['location']['name'],
        title=data['_node']['location']['name'],
        shortcode=shortcode,
        bin=encoded.decode('UTF-8'))

    iframe = folium.IFrame(html) #, width=400, height=400)
    #return iframe
    #html = folium.Html(html, script=True, width=300).render(),
    return html



# -------------------------
# Configuration
# -------------------------
# Initial location
LAT, LNG = 51.202044621063315, 38.460162567434566

# Create map
hmap = folium.Map(location=[LAT, LNG], zoom_start=3)

# Path
path = ':saved'
path = 'test'
locations = []

# Loop finding all json files
for i, f in enumerate(glob.glob('%s/**/*.json' % path, recursive=True)):
    print("\n%s. %s" % (i, f))

    # Load data
    with open(f) as json_file:
        data = json.load(json_file)


    # Find coordinates
    coordinates = find_locations(data)
    if coordinates is None:
        continue

    # Show coordinates
    print("Show coordinates:")
    print(json.dumps(coordinates, indent=4))

    # Create tooltip
    tooltip = coordinates['name']
    # Create popup
    popup = popup_v3(data)
    # Add marker
    folium.Marker([coordinates['lat'], coordinates['lng']],
        lazy=True,
        tooltip=tooltip,
        popup=folium.Popup(popup,
                           parse_html=False,
            min_height=400, max_height=400,
            min_width=300, max_width=300),
        icon=folium.Icon(color='orange',
                         icon='utensils', # 'university'
                         prefix='fa')
    ).add_to(hmap)

# Save
hmap.save('map.html')

# ---------------------------------------------
# Export CSV to manually import in google maps
# ---------------------------------------------

# ---------------------------------------------
# Import in my Google Maps automatically
# ---------------------------------------------


