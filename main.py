# Libraries
from pathlib import Path

from src.utils.ner import NERFlair
from src.utils.ner import NERBard
from src.bitacora import create_folder_structure
from src.bitacora import extract_ner
from src.bitacora import create_entities_db
from src.bitacora import create_geolocations_db
from src.bitacora import create_summary

# Configuration
#PROFILE_NAME = 'discoverearth'
#PROFILE_NAME = 'borgodeiborghi'
PROFILE_NAME = 'bernardhp'
#PROFILE_NAME = 'japan_walker_'
PROFILE_NAME = 'jukananan727'

# Create path to save profile data
path_profile_data = Path('./data') / PROFILE_NAME

# Configuration
FLAG_FETCH = True
FLAG_FOLDER = True
FLAG_NER = True
FLAG_GEO = True
FLAG_SUMMARY = True

# Select NER method
NER_METHOD = 'rule'

# Step 0: Download posts metadata
# -------------------------------
# .. note: When downloading information from a public Instagram
#          account there is no need for login details. However, when
#          downloading saved_posts by an account, credentials are
#          required.

if FLAG_FETCH:
    
    # Libraries
    from src.fetch import fetch_posts_instaloader
    
    # Fetch instagram account metadata
    fetch_posts_instaloader(
        profile_name=PROFILE_NAME,
        user_saved_posts=False,
        n_posts=20,
        output_path=path_profile_data
    )


# Step 1: Create folder structure
# --------------------------------
# .. note: For this method to work, there needs to be a folder with
#          a <post_list.obj> which contains all the posts metadata
#          downloaded using the instaloader library.
#
# The following structure is created:
#   data/bernardhp
#     |- _captions.json
#     |- _posts.json
#     |- posts
#           |- shortcode_1
#               | - caption.txt
#               | - post.json
#           |- shortcode_2
#               | - caption.txt
#               |- post.json

if FLAG_FOLDER:
    
    # Generate folder structure
    create_folder_structure(path=path_profile_data)



# Step 2: Extract entities from the caption
# -----------------------------------------
# .. note: There might be many entities that can be extracted from
#          the caption. Our focus is on locations, either countries,
#          cities, towns, specific addresses or restaurant names.

if FLAG_NER:

    # The method options are:
    #   1. 'flair'
    #   2. 'bard'
    #   3. 'spacy',
    #   4. 'spacy-sm'
    # spacy-lg
    # spacy-trf

    # Extract entities information
    extract_ner(path=path_profile_data,
                method=NER_METHOD,
                text_processing=None,
                force_reset=False)


# Step 3: Populate geolocation database
# -------------------------------------
if FLAG_GEO:

    create_entities_db(
        path=path_profile_data,
        method=NER_METHOD
    )
    
    create_geolocations_db(
        path=path_profile_data,
        method=NER_METHOD
    )


if FLAG_SUMMARY:

    # Explain
    create_summary(path=path_profile_data, method=NER_METHOD)

    # ------------------------------------
    # Copy static webapp
    # ------------------------------------
    # Libraries
    import os
    import json
    import shutil

    def create_static_web_app(src_dir, dst_dir):
        """Clone the static web app."""
        if not Path(dst_dir).exists():
            # Getting all the files in source
            files = os.listdir(src_dir)
            # Copy folder tree
            shutil.copytree(src_dir, dst_dir)

    def hack_json_to_js(src, dst):
        """Copy the .json into a .js file."""
        # Create data javascript.
        with open(src, 'r') as f:
            json_data = json.load(f)
        js_data = 'var data=%s' % json.dumps(json_data)
        with open(dst, 'w') as f:
            f.write(js_data)

    # Path to source directory
    src_dir = './src/apps/web'
    dst_dir = path_profile_data / 'web'

    # Copy static map app
    create_static_web_app(
        src_dir=src_dir,
        dst_dir=dst_dir
    )

    # Create a data.js file
    hack_json_to_js(
        src=path_profile_data / '_summary.json',
        dst=dst_dir / 'data.js')

