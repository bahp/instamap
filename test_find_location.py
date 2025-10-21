
import os
import json
import glob
from pathlib import Path


def find_node_location(data):
    try:
        v1 = data['_node']['location']
        print(json.dumps(v1, indent=4))
        return v1
    except Exception as e:
        return None

def find_user_location(data):
    try:
        v2 = data['_node']['iphone_struct']['location']
        print("_node/iphone_struct/user/location")
        print(json.dumps(v2, indent=4))
        return v2
    except Exception as e:
        print(e)

def find_text_location():
    pass

# Path
path = ':saved'

locations = []

# Loop finding all xz files but excluding the
# file if it starts with the word iterator.
for i, f in enumerate(glob.glob('%s/**/*.json' % path, recursive=True)):
    print("\n%s. %s" % (i, f))

    # Load data
    with open(f) as json_file:
        data = json.load(json_file)

    # Finding node location...
    coordinates = find_node_location(data)
    if coordinates is not None:
        print("Node:")
        print(json.dumps(coordinates, indent=4))

    # Finding user location...
    coordinates = find_user_location(data)
    if coordinates is not None:
        print("User:")
        print(coordinates)
        locations.append(coordinates)

    # If not lng, lat use google to find it!

# Need to create database and allow user to later select locations
# if needed. Because some instagrams posts have more than one
# location with names found in the text.


# Query locations by name
# https://geopy.readthedocs.io/en/stable/#installation
import geopy
#object=geopy.Nominatim(user_agent="Nikki")
#¢location = input("Enter the location ")
#h=object.geocode(ation)


# -----------------------------
# Display map using folium
# -----------------------------
# Library
import base64
import folium

# Initial location
LAT, LNG = 51.202044621063315, 38.460162567434566

# Create map
hmap = folium.Map(location=[LAT, LNG], zoom_start=3)

#html = '<img src="data:image/jpeg;base64,{}">'.format
#encoded = base64.b64encode(open(name + ' ' + cit + '.jpg', 'rb').read()).decode()
#iframe = folium.IFrame(html(encoded), width=300, height=150)
#tooltip = folium.Popup(iframe)
#icon = folium.IFrame('<i class="fas fa-archway"></i>')
#folium.Marker([lat, lng], tooltip=label, popup=tooltip,
#              icon=folium.Icon(color='orange', icon='university', prefix='fa')).add_to(arch_map)

#html = 'Tonto<br><img src="data:image/jpeg;base64,{}">'.format
#encoded = base64.b64encode(open(':saved/CzD6fazOqTe/item_1.jpg', 'rb').read()).decode()
#iframe = folium.IFrame(html(encoded), width=300, height=150)

#html = '<figure>'
#encoded = base64.b64encode(open(':saved/CzD6fazOqTe/item_1.jpg', 'rb').read()).decode()
#html += '<img src="data:image/jpg;base64,{}">'.format(encoded)
#html += '<figcaption>{}</figcaption></figure>'.format("FEO")
#iframe = folium.IFrame(html, width=300, height=150)

import base64

#Add Marker

#html = '<a href="https://www.instagram.com/p/CzD6fazOqTe/" >Click</a>'
#html+= '<img src="data:image/png;base64,{}" style="width:100%; height:100%;">'
html = '<a href="https://www.instagram.com/p/CzJtvEuIbUf/" >Click</a>'

#iframe = folium.IFrame(html.format(encoded.decode('UTF-8')), width=200, height=350)
iframe = folium.IFrame(html, width=200, height=350)
popup = folium.Popup(iframe, max_width=400)

def popup_v0():
    """Insert simple text"""
    return "Text"

def popup_v1():
    """Insert simple link"""
    return '<a href="https://www.instagram.com/p/CzJtvEuIbUf/ target="_blank"> Post </a>'

def popup_v2():
    """Insert simple image (encoded)"""
    encoded = base64.b64encode(open(':saved/CzD6fazOqTe/item_1.jpg', 'rb').read())
    html = '<img src="data:image/png;base64,{}" style="width:100%; height:100%;">'
    html = html.format(encoded.decode('UTF-8'))
    iframe = folium.IFrame(html, width=200, height=350)
    return iframe

    #popup = folium.Popup(iframe, max_width=400)
    #pass

def popup_v3():
    """Insert link to image"""
    encoded = base64.b64encode(open(':saved/CzD6fazOqTe/item_1.jpg', 'rb').read())
    html = """
        <div>
            <a href="https://www.instagram.com/p/CzJtvEuIbUf/ target="_blank"> Post </a>
            <img src="data:image/png;base64,{}" style="width:100%; height:100%;">
        </div>
    """
    html = html.format(encoded.decode('UTF-8'))
    #iframe = folium.IFrame(html, width=200, height=350)
    #return iframe
    return html

def popup_v4():
    """"""
    link_to_image = "https://scontent-lhr8-1.cdninstagram.com/v/t51.2885-15/397214462_233775913047319_5198776213886687270_n.jpg?stp=dst-jpg_e15&efg=eyJ2ZW5jb2RlX3RhZyI6ImltYWdlX3VybGdlbi43MjB4OTAwLnNkciJ9&_nc_ht=scontent-lhr8-1.cdninstagram.com&_nc_cat=107&_nc_ohc=5hWjQGjUh20AX9cJmam&edm=AP_V10EBAAAA&ccb=7-5&oh=00_AfD-GgYcYFgCiuQs-P2wJ9q7xU62cGYJZJbMhGyy7HTBgQ&oe=6549808D&_nc_sid=2999b8"
    html = '<img src="{}" style="width:100%; height:100%;">'
    return html.format(link_to_image)

"""
var link = "<a href=\""+"http://localhost/Webseite_Daten/diagramm_erstellen.php?diagramm=" +nr+"\""+" target=\"_blank\">Grafik erstellen</a>";
L.marker([lat,lon], {icon: marker}).bindPopup(link).addTo(map);
"""

link_to_image = "https://scontent-lhr8-1.cdninstagram.com/v/t51.2885-15/397214462_233775913047319_5198776213886687270_n.jpg?stp=dst-jpg_e15&efg=eyJ2ZW5jb2RlX3RhZyI6ImltYWdlX3VybGdlbi43MjB4OTAwLnNkciJ9&_nc_ht=scontent-lhr8-1.cdninstagram.com&_nc_cat=107&_nc_ohc=5hWjQGjUh20AX9cJmam&edm=AP_V10EBAAAA&ccb=7-5&oh=00_AfD-GgYcYFgCiuQs-P2wJ9q7xU62cGYJZJbMhGyy7HTBgQ&oe=6549808D&_nc_sid=2999b8"


# Add all locations
for d in locations:

    # Create variables
    #tooltip = d['short_name']
    #popup = html3.format(
    #    title=tooltip,
    #    link=link,
    #    encoded=encoded.decode('UTF-8')
    #)

    # Create tooltip
    tooltip = d['name']

    # Create popup
    popup = popup_v0()
    popup = popup_v1()
    popup = popup_v2()
    popup = popup_v3()
    #popup = popup_v4()

    # Add marker
    folium.Marker([d['lat'], d['lng']],
        tooltip=tooltip,
        popup=folium.Popup(popup, max_width=600),
        icon=folium.Icon(color='orange',
                         icon='university',
                         prefix='fa')
    ).add_to(hmap)

"""
marker = folium.Marker(
    [49.61068, 6.13127],
    popup="<a href=https://fr.wikipedia.org/wiki/Place_Guillaume_II>Place Guillaume II</a>",
    to
"""

# Save
hmap.save('map.html')


# ---------------------------------------------
# Export CSV to manually import in google maps
# ---------------------------------------------

# ---------------------------------------------
# Import in my Google Maps automatically
# ---------------------------------------------


