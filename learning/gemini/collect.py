# Libraries
from pathlib import Path
import json


# Get all of them and put them in a single file
search_path = Path('./../../data/bernardhp/')
#search_path = Path('./data/bernardhp')
output_filename = '_geolocations_gemini.json'
output_path = search_path / output_filename

print(f"Searching in path: {search_path}")
# Use .rglob() which means "recursive glob"
files_list = sorted(list(search_path.rglob('location_gemini.json')))
print(f"Found {len(files_list)} files.")

# Loop over all the files.
all_locations = []
for i, f in enumerate(files_list):
    shortcode = f.parent.stem

    try:
        # 1. Load the JSON file
        with open(f, 'r', encoding='utf-8') as file:
            locations_in_this_file = json.load(file)

        # 2. Add the shortcode to each location in the list
        if isinstance(locations_in_this_file, list):
            for location_item in locations_in_this_file:
                if isinstance(location_item, dict):
                    location_item['shortcode'] = shortcode

            # 3. Append the modified list to our main list
            all_locations.extend(locations_in_this_file)
        else:
            print(f"\nWarning: Skipping file {f} (not a list).")

    except json.JSONDecodeError:
        print(f"\nWarning: Skipping file {f} (invalid JSON).")
    except Exception as e:
        print(f"\nWarning: Skipping file {f} (Error: {e}).")

# --- Save the Final Combined File ---
try:
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(all_locations, f, indent=4)

    print(f"\nSuccessfully combined {len(all_locations)} locations from {len(files_list)} files.")
    print(f"Saved to: {output_path}")

except Exception as e:
    print(f"\nError saving final file: {e}")
