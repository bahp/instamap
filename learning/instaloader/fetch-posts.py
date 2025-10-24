"""

Description:

This script connects to Instagram using the library
instaloader and downloads the posts that the user has
in saved.

Running instaloader from terminal:

$ instaloader --login=bernardhp :saved
    --dirname-pattern={target}/{shortcode}

$ instaloader --login=bernardhp :saved
    --filename-pattern={shortcode}/item

$ instaloader --login=bernardhp :saved
    --filename-pattern={shortcode}/item
    --no-videos --no-video-thumbnails
    --geotags

$ instaloader --login=bernardhp :saved
    --dirname-pattern=test
    --filename-pattern={shortcode}/item
    --no-videos --no-video-thumbnails
    --slide=1 --no-pictures --geotags

"""
# Libraries
import json
import pickle

from time import sleep
from pathlib import Path
from random import randint

from instaloader import Instaloader
from instaloader import Profile
from instaloader import Post


USER = 'bahp.dev'
PROFILE = 'discoverearth'
PROFILE = 'japan_walker_'
PROFILE = 'jukananan727'
COLLECTION = Path('./outputs/')

# Get instance
L = Instaloader()
L.download_pictures = False
L.download_videos = False
L.download_video_thumbnails = False
L.download_geotags = True
L.save_metadata = True
L.compress_json = False
L.download_comments = False

# The authentication is only necessary if querying
# own saved posts, or maybe posts from private accounts
# which you are following. For public accounts, it
# is not necessary.

# Login user
#if USER is None:
#    USER = input("Input username: ")

try:
    L.load_session_from_file(USER)
except FileNotFoundError:
    L.interactive_login(USER)

# Get profile
profile = Profile.from_username(L.context, PROFILE)

# -------------------------------
# Download post json information
# -------------------------------

try:
    # Create directory if it does not exist
    (COLLECTION / PROFILE).mkdir(parents=True, exist_ok=True)

    # Get saved posts
    #post_list = []
    #for saved_posts in profile.get_saved_posts():
    #    post_list.append(saved_posts)

    # Get wall posts.
    post_list = []
    for i,posts in enumerate(profile.get_posts()):
        post_list.append(posts)
        if i > 100:
            break

    # Show information
    print("Total posts...%s" % len(post_list))

    # Save
    with open(COLLECTION / PROFILE / 'post_list.obj', 'wb') as f:
        pickle.dump(post_list, f)

except IndexError:
    print("You have no saved posts yet.")


# -----------------------------
# Download post data
# -----------------------------
# Review this code as it has not been executed. Check
# the documentation page for instaloader for the
# available functions and some examples.

"""
# Define shortcode
shortcode = 'B-cWU3Xh_vl'

# Get post from shortcode.
post = Post.from_shortcode(L.context, shortcode)

#
#posts.save_structure_to_file(structure, filename)¶


#loader.download_post(p, 'saved-collection/%s' % str(p))

# Download post
L.download_post(post, COLLECTION / shortcode)
"""
