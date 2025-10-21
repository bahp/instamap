# Libraries
import os
import sys
import itertools
import numpy as np

from flair.data import Sentence
from flair.nn import Classifier

from pathlib import Path
from src.utils import text
from src.utils import load
from src.utils.ner import NERFlair

# .. note: This is a summary of shortcodes for the instagram
#          posts which contain certain characteristic that can
#          be exploited to extract better locations. These are
#
# - bulletpoints:
# - icons:
# - hashtaghs:
#- address

SHORTCODE_CLASSES = {
    'bulletpoints': [
        'CzBYpc5ocQb',
        'CvE3TlxLgKU',
        '1111'
    ],
    'icons': [
        'CxQ1tJ8rV9w',
        'CytHvWGIh8M'
    ],
    'todo': [
        'B5ewgDhKQth',
        'B5NqBLMJGZM'
    ],
    'hashtags': [
        'Cy3hRvYoEQt',
        'Cym0t2ftWMN'
    ],
    'address': [
        'Ct6C0desz3b'
    ]
}


# ----------------------------------
# Load captions
# ----------------------------------
# These methods return a dictionary in which the key
# corresponds to the shortcode of the pot and the value
# contains the caption.

# Load file with all captions
captions = load.load_file_with_all_captions(
    filepath='./data/bernardhp/data/_captions.json'
)

# Load specific captions
captions = load.load_captions_by_shortcode(
    shortcode_list=[
        '12345678',
        'B-cWU3Xh_vl',
        'B-fMHQ9hrSR'
    ], path='./data/bernardhp/data/'
)

# Load captions from SHORTCODES_CLASSES
shortcodes = [v for k, v in SHORTCODE_CLASSES.items()]
captions = load.load_captions_by_shortcode(
    shortcode_list=itertools.chain(*shortcodes),
    path='./data/bernardhp/data/'
)


# ----------------------------------
# Text Formatting
# ----------------------------------
# Select the shortcodes
SHORTCODES = captions

# Create classifier
tagger = Classifier.load('ner')

# Conduct text formatting
for i,(k,v) in enumerate(SHORTCODES.items()):

    # Edited text
    edited = text.format_text_chain(text=v,
        chain=[
            (text.bulletpoints_to_location, {}),
            (text.icon_to_location, {}),
            (text.new_line_to_end_sentence, {}),
            (text.remove_multiple_spaces, {})
        ])

    # Create sentence
    sentence = Sentence(edited)
    tagger.predict(sentence)

    # Get json result
    r = sentence.to_dict(tag_type='ner')
    df = NERFlair().entities_to_dataframe(r)

    # Show
    text.show(i=i, post_id=k, text1=v, text2=edited, result=df)
