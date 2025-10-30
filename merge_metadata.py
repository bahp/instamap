# Libraries
from pathlib import Path
import json
import re
import sys
from typing import List, Dict, Any

# --- CONFIGURATION ---
# Set this to your actual root data path: e.g., './gallery-dl/instagram/'
search_path = Path('./gallery-dl/instagram/')
output_filename = 'data.json'
#output_path = search_path / output_filename
output_path = Path('./') / output_filename

# --- Filename Patterns ---
# This glob finds ALL double-extension JSON files (Media metadata AND Gemini output)
# We will exclude the Gemini output inside the loop.
MEDIA_METADATA_GLOB = '*.*.json'

# The name of the location file *suffix* (e.g., postid.locations.gemini.json)
LOCATION_FILE_SUFFIX = 'locations.gemini.json'

# Regex to extract post_id from media metadata filenames
# Matches (postid)(_mediaid...)?(.ext.json) --> Group 1 is the postid
# This helps parse postid_mediaid.ext.json OR postid.mp4.json
FILENAME_PATTERN = re.compile(r"^(\d+)(?:_.*)?\..*\.json$")


# ---------------------


def merge_enriched_locations(root_path: Path):
    """
    Iterates through every media metadata file, finds the corresponding post-level
    location data, and merges everything into a single output list where each
    entry represents one media item, enriched with location data.
    """
    if not root_path.exists():
        print(f"❌ Fatal Error: Search path does not exist at {root_path}")
        sys.exit(1)

    print(f"1. Starting merge process in: {root_path}")

    all_merged_entries: List[Dict[str, Any]] = []
    processed_count = 0

    # 1. Loop through ALL double-extension JSON files recursively
    for media_metadata_path in root_path.rglob(MEDIA_METADATA_GLOB):
        filename = media_metadata_path.name

        # --- CRITICAL FIX: EXCLUDE GEMINI OUTPUT FILES ---
        # If the file ends with the location suffix, skip it immediately.
        if filename.endswith(LOCATION_FILE_SUFFIX):
            continue

        # --- A. Extract Post ID and Load Media Metadata (Expected: DICTIONARY) ---

        # Match post_id
        match = FILENAME_PATTERN.match(filename)
        if not match:
            # Skip files that don't match the standard media naming convention
            continue

        post_id = match.group(1)

        try:
            with media_metadata_path.open('r', encoding='utf-8') as f:
                media_data = json.load(f)
        except Exception:
            print(f"Warning: Skipping corrupted media metadata: {media_metadata_path}")
            continue

        # Ensure media data is a dictionary before merging
        if not isinstance(media_data, dict):
            print(f"Warning: Skipping file {media_metadata_path}. Expected DICTIONARY, found list/other.")
            continue

        # --- B. Find and Load Gemini Locations (Expected: LIST) ---

        # Construct the EXACT name of the location file for lookup
        location_filename = f"{post_id}.{LOCATION_FILE_SUFFIX}"
        location_file_path = media_metadata_path.parent / location_filename

        gemini_locations = []
        if location_file_path.exists():
            try:
                with location_file_path.open('r', encoding='utf-8') as f:
                    location_content = json.load(f)

                    # Ensure location data is a list
                    if isinstance(location_content, list):
                        gemini_locations = location_content
                    else:
                        print(f"Warning: Location file {location_file_path} content is not a LIST ([]).")

            except Exception:
                # File exists but is corrupt
                print(f"Warning: Failed to load (corrupt) Gemini locations: {location_file_path}")

        # --- C. Create Merged Entry ---

        merged_entry = media_data  # Start with the media dictionary

        # Add the Gemini locations list as a single attribute
        merged_entry['gemini_locations'] = gemini_locations

        # Add file paths for utility/debugging
        merged_entry['media_metadata_path'] = str(media_metadata_path)
        merged_entry['gemini_locations_path'] = str(location_file_path) if gemini_locations else None

        all_merged_entries.append(merged_entry)
        processed_count += 1

        if processed_count % 1000 == 0:
            print(f"   -> Processed {processed_count} files...")

    print(f"\n2. Finished processing. Total media files merged: {processed_count}")

    # 3. Save the Final Combined File
    print(f"3. Saving final combined file to: {output_path}")
    try:
        with output_path.open('w', encoding='utf-8') as f:
            json.dump(all_merged_entries, f, indent=2)

        print(f"\nSuccessfully combined {len(all_merged_entries)} entries.")

    except Exception as e:
        print(f"\nError saving final file: {e}")
        sys.exit(1)


# --- DRIVER CODE ---
if __name__ == "__main__":
    merge_enriched_locations(search_path)