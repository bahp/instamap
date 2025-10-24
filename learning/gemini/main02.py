# Libraries
import os
import re
import json
import time
import random

from google import genai
from pathlib import Path
from tqdm import tqdm

from google.api_core import exceptions as google_exceptions



# ------------------------------------------------
#            Load GOOGLE_API_KEY
# ------------------------------------------------
try:
    API_KEY = os.environ["GOOGLE_API_KEY"]
    client = genai.Client(api_key=API_KEY)

except KeyError:
    print("Error: GOOGLE_API_KEY environment variable not set.")
    print("Please set the variable and try again.")
    exit()
except Exception as e:
    print(f"Error initializing the model: {e}")
    exit()


# -----------------------------------------------------------------
# Configure variables
# -----------------------------------------------------------------

# --- The Prompt ---
prompt_template = """
You are a geography and data extraction expert.
I will give you a social media post caption.
Extract *all* specific geographic locations from the caption.

The caption may contain multiple locations, often in a list where each line 
is prepended with an icon (📍, 📷, 🗺️), numbers (1., 2.), or letters (a., b.). 
They might also be included in the hashtags.

Return ONLY a single, valid JSON *list*.
Each object in the list must have the following nine keys:
1. "title": The concise name of the location (max 5 words).
2. "subtitle": A brief description (max 10 words).
3. "lat": The latitude.
4. "lon": The longitude.
5. "type": The specific type of location (e.g., 'river', 'forest', 'cave', 'national park', 'city', 'building', 'restaurant').
6. "class": The generic classification (e.g., 'amenity', 'place', 'man_made', 'natural').
7. "confidence": A numerical score (e.g., 0.0 to 1.0) indicating your certainty in the extracted location and its details.
8. "rank": A numerical rank indicating the location's geographic scale (1=most specific, 9=broadest). Use this hierarchy:
    1: POI/Building (e.g., 'Eiffel Tower', 'castle', 'restaurant')
    2: Site/Neighborhood (e.g., 'Tikal National Park', 'SoHo', 'Central Park')
    3: Town/Village
    4: City
    5: County/Province (e.g., 'Petén Department')
    6: State/Region (e.g., 'California', 'Tuscany')
    7: Country
    8: Supranational Region / Large Natural Feature (e.g., 'The Alps', 'Scandinavia')
    9: Continent
9. "page": The numerical order of appearance if the location is part of an explicit list (e.g., "1. Paris", "2. Rome", or "📍 Paris", "📍 Rome"). Start from 1. If not part of an explicit list, set this to null.

Try to be as specific as possible. For example, if the caption says "This impressive Maya temple in Tikal is called the Great Jaguar", extract the "Great Jaguar Temple" (Rank 1) in "Tikal" (Rank 2), not just "Tikal".
If a location is mentioned but too broad (e.g., "England"), find the coordinates for the main subject mentioned (e.g., Stonehenge, Rank 2).
If you cannot find any specific locations, return an empty list [].

Caption: "{caption}"
"""

prompt_template = """
You are a geography and data extraction expert.
I will give you a social media post caption.
Your goal is to extract the specific geographic location(s) the post is *primarily* about.

**Core Rules:**
1.  **Most Specific Rule:** A caption usually refers to *one primary location*. If multiple locations are mentioned in a nested hierarchy (e.g., "El Prado Museum, Madrid, Spain"), extract **only the most specific one** (i.e., "El Prado Museum").
    * **Crucially**: Although you *do not* extract the more generic locations (like "Madrid" or "Spain" in this example), you **must use them as context** to properly and accurately find the latitude and longitude of the specific location.
2.  **Broader Location Rule:** If the caption only provides a broader location (e.g., "Loved visiting Madrid!"), then extract that location ("Madrid").
3.  **Explicit List Exception:** The *only* time you should extract multiple locations is if the caption contains an **explicit list** of *different* locations. These are often prepended with an icon (📍, 📷, 🗺️), numbers (1., 2.), or letters (a., b.). In this case, extract *every* location in that list.
4.  Check hashtags for potential locations, following the same rules.

Return ONLY a single, valid JSON *list*.
Each object in the list must have the following nine keys:
1.  `"title"`: The concise name of the location (max 5 words).
2.  `"subtitle"`: A brief description (max 10 words).
3.  `"lat"`: The latitude.
4.  `"lon"`: The longitude.
5.  `"type"`: The specific type of location (e.g., 'river', 'forest', 'cave', 'national park', 'city', 'building', 'restaurant').
6.  `"class"`: The generic classification (e.g., 'amenity', 'place', 'man_made', 'natural').
7.  `"confidence"`: A numerical score (e.g., 0.0 to 1.0) indicating your certainty in the extracted location and its details.
8.  `"rank"`: A numerical rank indicating the location's geographic scale (1=most specific, 9=broadest). Use this hierarchy:
    1: POI/Building (e.g., 'Eiffel Tower', 'castle', 'restaurant')
    2: Site/Neighborhood (e.g., 'Tikal National Park', 'SoHo', 'Central Park')
    3: Town/Village
    4: City
    5: County/Province (e.g., 'Petén Department')
    6: State/Region (e.g., 'California', 'Tuscany')
    7: Country
    8: Supranational Region / Large Natural Feature (e.g., 'The Alps', 'Scandinavia')
    9: Continent
9.  `"page"`: The numerical order of appearance *only* if the location is part of an explicit list (e.g., "1. Paris", "2. Rome", or "📍 Paris", "📍 Rome"). Start from 1. If not part of an explicit list, set this to `null`.

**Examples of Logic:**
* If caption is "This impressive Maya temple in Tikal is called the Great Jaguar", extract *only* the "Great Jaguar Temple" (Rank 1).
* If caption is "Just landed in Madrid, Spain!", extract *only* "Madrid" (Rank 4).
* If caption is "My trip: 1. Paris 2. Rome", extract *both* "Paris" (page: 1) and "Rome" (page: 2).
* If a location is mentioned but too broad (e.g., "England"), try to find the coordinates for the main subject mentioned (e.g., Stonehenge, Rank 2). If no specific subject is given, extract the broad location ("England", Rank 7).

If you cannot find any specific locations, return an empty list `[]`.

Caption: "{caption}"
"""

# --- The model --
model_name = 'gemini-2.5-flash'
#model_name = 'gemini-pro'
caption_filename = 'caption.txt'
location_filename = 'location_gemini.json'
MAX_RETRIES = 5  # Try a maximum of 5 times

REWRITE = False

# Set the total number of times to try
MAX_ATTEMPTS = 5

# Set the base wait time (in seconds) for exponential backoff
# Used only for ServerErrors (5xx)
BASE_WAIT_TIME = 2


# Define the folder to search
search_path = Path('./../../data/bernardhp/')
print(f"Searching in path: {search_path}")

# Use .rglob() which means "recursive glob"
files_list = sorted(list(search_path.rglob('caption.txt')))
print(f"Found {len(files_list)} files.")

# Loop over all the files.
for i, f in enumerate(files_list):
   # if i>5:
   #     break

    # Locations have been extracted already
    if not REWRITE:
        if (f.parent / location_filename).exists():

            # Open and load the JSON file
            with open(f.parent / location_filename, 'r') as fj:
                data = json.load(fj)

            print(f"{i:4}/{len(files_list)}. Post already processed: {f.parent.stem} | {len(data)} location(s) found.")
            continue

    # Read caption
    with open(f, 'r') as ft:
        caption = ft.read()

    print(f"{i:4}/{len(files_list)}. Processing caption <{f.parent.stem}>: ", end='')
    prompt = prompt_template.format(caption=caption)

    # --- Start Retry Loop ---
    for attempt in range(MAX_ATTEMPTS):
        try:
            print(f"--- Attempt {attempt + 1} of {MAX_ATTEMPTS} ---")

            # Use the client to generate content
            response = client.models.generate_content(
                model=model_name,
                contents=prompt
            )

            # If successful, parse the JSON
            response_text = response.text.strip() \
                .replace("```json", "").replace("```", "")
            data_list = json.loads(response_text)

            # Save
            with open(f.parent / location_filename, 'w', encoding='utf-8') as fo:
                json.dump(data_list, fo, indent=4)
            print(f"Extracted {len(data_list)} location(s).")

            # 2. Use time.sleep() to pause
            wait_duration = random.uniform(1.5, 5.5)
            print(f"Now waiting for {wait_duration:.2f} seconds...")
            time.sleep(wait_duration)

            # If successful, break out of the retry loop
            break

        except google_exceptions.InvalidArgument as e:
            # This block specifically catches the 400 Invalid API Key error.
            print(f"Error: Invalid argument. Full error: {e}")
            import sys
            sys.exit()


        except google_exceptions.ResourceExhausted as e:
            # This block specifically catches the 429 Quota Exceeded error
            print(f"Error: Quota exceeded. Full error: {e}")

            if attempt == MAX_ATTEMPTS - 1:
               print("Last attempt failed. No more retries.")
               break  # Exit loop

            # --- Parse the error message to get the wait time ---
            error_message = str(e)
            match = re.search(r"Please retry in ([\d.]+)s", error_message)

            if match:
                wait_time = float(match.group(1))
                print(f"Waiting for {wait_time:.2f} seconds as suggested by the API...")
                time.sleep(wait_time)
                # You would typically put this in a loop to retry the request
                # print("Retrying now...")
            else:
                # Fallback if the error message format ever changes
                print("Could not parse retry time. Waiting 60 seconds as a fallback.")
                time.sleep(60)

        except genai.errors.ServerError as e:
            print(f"Error: ServerError. Full error: {e}")

            # Check if we're on the last attempt
            if attempt == MAX_ATTEMPTS - 1:
                print("Last attempt failed. No more retries.")
                break  # Exit loop

            # --- This is the "Exponential Backoff" ---
            # attempt 0: 2^0 * 2 = 2s
            # attempt 1: 2^1 * 2 = 4s
            # attempt 2: 2^2 * 2 = 8s
            # ...plus a random 'jitter' to prevent all clients retrying at once
            wait_time = (BASE_WAIT_TIME ** attempt) + random.uniform(0, 1)

            print(f"Waiting {wait_time:.2f}s before next retry...")
            time.sleep(wait_time)

            """
            # This catches the 503 error
            if attempt < MAX_RETRIES - 1:
                wait_time = 2 ** attempt  # Exponential backoff (1, 2, 4, 8 seconds)
                print(f"  > Model overloaded (503). Retrying in {wait_time} second(s)...")
                time.sleep(wait_time)
            else:
                print(f"Error: Failed to process caption after {MAX_RETRIES} attempts.")
                print(f"  > Last error: {e}")
            """

        except json.JSONDecodeError:
            # Don't retry if JSON is bad
            print(f"Error: Could not decode JSON from response: {response.text}")
            break  # Exit loop
        except Exception as e:
            # For any other error, we don't want to retry
            print(f"An unexpected error occurred: {e}")
            print(e.code)
            if e.code == '400':
                print("EHHH")
            import sys
            sys.exit()
            break  # Exit loop
    # --- End Retry Loop ---




# Get all of them and put them in a single file
search_path = Path('./../../data/bernardhp/')
output_filename = '_geolocations_gemini.json'
output_path = search_path / output_filename

print(f"Searching in path: {search_path}")
# Use .rglob() which means "recursive glob"
files_list = sorted(list(search_path.rglob('location_gemini.json')))
print(f"Found {len(files_list)} files.")

"""
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
"""
