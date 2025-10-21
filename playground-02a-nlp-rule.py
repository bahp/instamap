"""

"""
# Libraries
import os
import sys
import itertools
import numpy as np

from pathlib import Path
from src.utils import text
from src.utils import load
from src.utils import ner

"""
This is a summary of shortcodes for the instagram posts which contain 
certain characteristic that can be exploited to extract better locations. 
These are the following:

Icons
-----
Some captions include an icon that refers to the location at the 
beginning or the end of the location. This can be used to extract 
the address neatly.

    e.g. CMEXWMMB1d0
    🌍 LOC : 🇮🇹 #campobasso

    e.g. CxQ1tJ8rV9w
    🌍 LOC : Pietrapertosa 🇮🇹 #basilicata (Potenza)
    
    e.g. CnUFPmav67B
    Location🚩: Zurich


Flags
-----
Some captions include a flag icon which can be used to support
the geolocation query by appending it to any other location found,
or use it as a location if no other is found.

    e.g. CnCE-efPy8W

Bulletpoints
------------
In the captions, many users list the locations in bullet points.
Find all the locations which appear listed after a number, or any 
other type of bullet point. Note that they might be in the same
line or in a different line or not.

    e.g. Cy-hYVzPemK
    1,Magome Juku  2,Takayama 3,Nakano 4,Konkaikomyo-ji

    e.g. CzD6fazOqTe
    1. Our Lady of the Rocks Island
    2. Tivat Bay
    3. Sveti Stefan
    4. Lake Piva
    5. Perast
    6. Bay of Kotor
    7. Lovcen
    8. Fortress Kanli Kula in Herceg Novi
    9. Kotor
    10. Kotor

Hashtags
--------

Address
-------

Country names
-------------
Some captions have country names, or also acronyms.

    e.g.
    uk = United Kingdom

"""

SHORTCODE_CLASSES = {
    'bulletpoints': [
        'CzBYpc5ocQb', 'CvE3TlxLgKU', '11111111'
    ],
    'icons': [
        'CxQ1tJ8rV9w', 'CytHvWGIh8M', 'CnUFPmav67B', 'CvIEfZVNIDm',
        'CylhhZXM5mO', 'Cy6EgYltiFv', 'CyubKljvvNy', 'CytMiMBtB6c',
        'CwsXj8kNSQh', 'Cyxz2rhNscp', 'CyknIJtI2k6', 'CylDyTNtVZc',
        'CykUIy8oIrw', 'CyTf-iOIWjq', 'CwcLq14s4Mk', 'CyQWtpzru19',
        'CyQnvkOtqzx', 'CyEJ3mLIUV1', 'CyLtbl6twpu', 'Ct6C0desz3b',
        'CyGDGR3sv7z', 'CxRC5lZoKHm', 'Cx3yIHTocBA', 'CxNzc1IIitt',
        'Cql5SkNrB_I', 'CxL0HHYIfb5', 'CxXX44btaHb'
    ],
    'flags': [
        'CvE3TlxLgKU', 'Cy-hYVzPemK', 'CxQ1tJ8rV9w', 'CzBYpc5ocQb',
        'CyRLr01sj8i', 'CysEVwgqeS8', 'Cy6EgYltiFv'
    ],
    'todo': [
        'B5ewgDhKQth', 'B5NqBLMJGZM', 'CT0MZIoqMTD', 'Cqf9NeWDl_O',
        'CWgX4BGINBa' #missing?
    ],
    'usernames': [
        'CH-0EoOJSBr'
    ],
    'hashtags': [
        'Cy3hRvYoEQt', 'Cym0t2ftWMN', 'CmAfZ_gDbDn' # indonesia in hash
    ],
    'address': [
        'Ct6C0desz3b'
    ],
    'multiple_countries': [
        'CpQYsAiq7um', 'CUUHXpjMF_k', 'CIuvmTGD3pO'
    ],
    'punctuation': [
        'CiPjVQcq_Qt'
    ],
    'country_improves_geotag': [
        'CyTxJsgtpTv'
    ]
}


# ----------------------------------
# Load captions
# ----------------------------------
# These methods return a dictionary in which the key
# corresponds to the shortcode of the pot and the value
# contains the caption.

PATH = Path('./data/bernardhp/')

# Load file with all captions
captions = load.load_file_with_all_captions(
    filepath=PATH / '_captions.json'
)

"""
# Load specific captions
captions = load.load_captions_by_shortcode(
    shortcode_list=[
        '12345678',
        'B-cWU3Xh_vl',
        'B-fMHQ9hrSR'
    ], path=PATH / 'posts'
)

# Load captions from SHORTCODES_CLASSES
shortcodes = [v for k, v in SHORTCODE_CLASSES.items()]
captions = load.load_captions_by_shortcode(
    shortcode_list=itertools.chain(*shortcodes),
    path=PATH / 'posts'
)

# Load specific captions
captions = load.load_captions_by_shortcode(
    shortcode_list=SHORTCODE_CLASSES['bulletpoints'],
    path=PATH / 'posts'
)
"""



# ----------------------------------
# Text Formatting
# ----------------------------------
# Select the shortcodes
SHORTCODES = captions

# Create classifier
tagger_rule = ner.NERRule()
tagger_flair = ner.NERFlair()

# Conduct text formatting
for i,(k,v) in enumerate(SHORTCODES.items()):

    # Create sentence
    r1 = tagger_rule.predict(v)
    r2 = tagger_flair.predict(v)

    # Create DataFrames
    df1 = tagger_rule.to_frame(r1)
    df2 = tagger_flair.to_frame(r2)

    # Show
    print("="*80)
    print(k)
    print(v)
    print("\n")
    print(df1)
    print(df2)

    print("Press any key to continue...")
    input()
