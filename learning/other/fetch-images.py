""""""

# Libraries
import json
from urllib import request


def urls_instaloader_json(filepath):
    """

    .. note: It is a bit useless to try to download the thumbnails
             using the urls provided in the post.json because they
             have a signature that expires in a few hours/days.

    """
    # Load data
    with open(filepath) as json_file:
        data = json.load(json_file)

    # Get information
    shortcode = data['node']['shortcode']
    display_url = data['node']['display_url']
    thumbnail_src = data['node']['thumbnail_src']

    # Return
    return [display_url, thumbnail_src]


def urls_manual():
    """"""
    return [
        'https://blog.finxter.com/wp-content/uploads/2022/04/greenland_01a.jpg',
        'https://blog.finxter.com/wp-content/uploads/2022/04/greenland_02a.jpg',
        'https://blog.finxter.com/wp-content/uploads/2022/04/greenland_03a.jpg',
        'https://blog.finxter.com/wp-content/uploads/2022/04/greenland_04a.jpg'
    ]


# Get urls
#urls = urls_instaloader_json('./inputs/post.json')
urls = urls_manual()

# Download images
for i,url in enumerate(urls):
    request.urlretrieve(url, './outputs/thumbnail-%s.jpg' % i)


"""
import urllib.request
from PIL import Image

# Retrieving the resource located at the URL
# and storing it in the file name a.png
url = "https://media.geeksforgeeks.org/\
wp-content/uploads/20210224040124/ \
JSBinCollaborativeJavaScriptDebugging6-300x160.png"
urllib.request.urlretrieve(url, "geeksforgeeks.png")

# Opening the image and displaying it (to confirm its presence)
img = Image.open(r"geeksforgeeks.png")
img.show()
"""