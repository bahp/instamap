import re
import json
from pathlib import Path
import sys

# --- CONFIGURATION ---
MEDIA_DATA_ROOT = './gallery-dl/instagram/'
# Use a dynamic naming convention: {post_id}.caption.txt
CAPTION_SUFFIX = '.caption.txt'
GENERIC_CAPTION_FILENAME = 'caption.txt'

# Regex to match the post ID based on the two observed patterns:
# 1. Image: (postid)_(mediaid.ext.json) --> Groups 1 is postid
# 2. Video: (postid.mp4.json)           --> Groups 1 is postid
FILENAME_PATTERN = re.compile(r"^(\d+)(?:_.*)?\..*\.json$")


# ---------------------

def remove_caption_files(media_root_dir_str):
    """
    Removes all generic 'caption.txt' files recursively from the media root.

    Parameters
    ----------
    media_root_dir_str: String
        The root with the media files.
    """
    media_root_dir = Path(media_root_dir_str)

    if not media_root_dir.exists():
        print(f"❌ Error: Root media directory not found at {media_root_dir}. Check your path.")
        return

    print(f"1. Removing all generic '{GENERIC_CAPTION_FILENAME}' files...")
    count_removed = 0

    # Use rglob to find all generic caption files recursively
    for filepath in media_root_dir.rglob(GENERIC_CAPTION_FILENAME):
        try:
            filepath.unlink()  # Delete the file
            count_removed += 1
        except Exception as e:
            print(f"Warning: Failed to remove file {filepath}: {e}")

    print(f"   -> Removed {count_removed} generic '{GENERIC_CAPTION_FILENAME}' file(s).")


def create_caption_files(media_root_dir_str):
    """
    Loops the gallery-dl generated folder structure, identifies unique
    posts, extracts the shared caption and writes it into a file named
    {post_id}.caption.txt in the same post's directory.

    Parameters
    ----------
    media_root_dir_str: String
        The folder with the usernames and media files.
    """
    media_root_dir = Path(media_root_dir_str)

    if not media_root_dir.exists():
        print(f"❌ Error: Root media directory not found at {media_root_dir}. Check your path.")
        return

    print(f"\n2. Scanning media data and creating '{CAPTION_SUFFIX}' files...")

    # Dictionary to track the path to the FIRST JSON found for each post_id
    post_json_map = {}

    # 💡 rglob PATTERN 💡: Finds files ending in a media extension (.mp4, .jpg, etc.) followed by '.json'.
    media_metadata_pattern = '*.*.json'

    # Find all .json files recursively
    for filepath in media_root_dir.rglob(media_metadata_pattern):
        filename = filepath.name

        # --- Extract post_id using Regex ---
        match = FILENAME_PATTERN.match(filename)

        if not match:
            continue

        post_id = match.group(1)

        # If we haven't found a JSON for this post ID yet, store this path
        if post_id not in post_json_map:
            post_json_map[post_id] = filepath

    print(f"   -> Found {len(post_json_map)} unique posts across all users.")

    # 3. Third Pass: Extract caption and write file
    count_created = 0
    for post_id, json_path in post_json_map.items():
        # Create the new filename: postid.caption.txt
        caption_file_path = json_path.parent / f"{post_id}{CAPTION_SUFFIX}"

        # Note: We still check existence, but it's less likely to exist now
        if caption_file_path.exists():
            continue

        try:
            with json_path.open('r', encoding='utf-8') as f:
                media_json = json.load(f)
        except Exception:
            print(f"Warning: Failed to read/decode JSON for post {post_id} at {json_path}")
            continue

        caption = media_json.get('description', '').strip()

        if not caption:
            continue

        # Write the caption file
        try:
            caption_file_path.write_text(caption, encoding='utf-8')
            count_created += 1
        except Exception as e:
            print(f"Warning: Failed to write caption file for post {post_id}: {e}")

    print(f"\n3. Caption creation complete. Created {count_created} '{CAPTION_SUFFIX}' file(s).")






if __name__ == "__main__":

    # Clean up any previous generic caption files
    #remove_caption_files(MEDIA_DATA_ROOT)

    # Create the new, correctly named caption files
    create_caption_files(MEDIA_DATA_ROOT)