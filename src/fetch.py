# Libraries
import sys
import pickle

from tqdm import tqdm
from pathlib import Path


def fetch_posts_instaloader(profile_name,
                            user_saved_posts=False,
                            n_posts=1e4,
                            output_path=None):
    """"""
    # Libraries
    from instaloader import Instaloader, Profile

    # Default name of metadata object.
    FILENAME = 'post_list.obj'

    # Create instance
    L = Instaloader()
    L.download_pictures = False
    L.download_videos = False
    L.download_video_thumbnails = False
    L.save_metadata = True
    L.compress_json = False
    L.download_geotags = True
    L.download_comments = False

    # Loading saved posts needs authentication
    if user_saved_posts:
        try:
            L.load_session_from_file(profile_name)
        except FileNotFoundError:
            L.interactive_login(profile_name)

    # Get profile
    profile = Profile.from_username(L.context, profile_name)

    # Select method to use
    if user_saved_posts:
        method = profile.get_saved_posts
    else:
        method = profile.get_posts

    # Get posts
    post_list = []
    for i,post in tqdm(enumerate(method()), desc='Downloading...'):
        post_list.append(post)
        if i > n_posts:
            break

    # Logging
    print("[Bitacora] Profile: {profile} | # Posts: {n_posts}" \
          .format(profile=profile_name,
                  n_posts=len(post_list)))

    # Save
    if output_path is not None:
        # Define full path
        fullpath = Path(output_path)
        # Create directory if it does not exist
        fullpath.mkdir(parents=True, exist_ok=True)
        # Dump list as pickle file
        with open(fullpath / FILENAME, 'wb') as f:
            pickle.dump(post_list, f)

    # Return
    return post_list



class InstaloaderFetcher:
    """"""
    def __init__(self):
        pass

    def fetch(self):
        pass