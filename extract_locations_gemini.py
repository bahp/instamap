# Libraries
import os
import re
import json
import time
import random
import sys

from google import genai
from google.genai.errors import ClientError, ServerError
from pathlib import Path

# ------------------------------------------------
#            Load GOOGLE_API_KEY
# ------------------------------------------------
try:
    API_KEY = os.environ["GOOGLE_API_KEY"]  # os is implicitly available here or needs to be imported
    client = genai.Client(api_key=API_KEY)

except KeyError:
    print("Error: GOOGLE_API_KEY environment variable not set.")
    sys.exit(1)
except Exception as e:
    print(f"Error initializing the model: {e}")
    sys.exit(1)

# -----------------------------------------------------------------
# Configure variables
# -----------------------------------------------------------------

# --- The Prompt (Using the detailed, specific version provided) ---
prompt_template = """
You are a geography and data extraction expert.
I will give you a social media post caption.
Your goal is to extract the specific geographic location(s) the post is *primarily* about.

**Core Rules:**
1.  **Most Specific Rule:** Extract **only the most specific location** mentioned. Use broader locations only for context.
2.  **Broader Location Rule:** Extract the broader location if no specific POI is given.
3.  **Explicit List Exception:** Extract **multiple locations** only if they form an **explicit list**.
4.  Check hashtags for potential locations.

Return ONLY a single, valid JSON *list*.
Each object in the list must have the following nine keys:
1.  `"title"`: The concise name of the location (max 5 words).
2.  `"subtitle"`: A brief description (max 10 words).
3.  `"lat"`: The latitude.
4.  `"lon"`: The longitude.
5.  `"type"`: The specific type of location (e.g., 'river', 'forest', 'city', 'building').
6.  `"class"`: The generic classification (e.g., 'amenity', 'place', 'natural').
7.  `"confidence"`: A numerical score (0.0 to 1.0).
8.  `"rank"`: Location hierarchy (1: POI/Building to 9: Continent).
9.  `"page"`: Numerical order if part of an explicit list (start from 1), otherwise `null`.

If you cannot find any specific locations, return an empty list `[]`.

Caption: "{caption}"
"""

prompt_template = """
You are a geography and data extraction expert.
I will give you a social media post caption.
Your goal is to extract the specific geographic location(s) the post is *primarily* about.

**Core Rules for Specificity and Relevance:**
1.  **Most Specific Rule (Primary Focus):** A caption usually refers to *one primary location*. If multiple locations are mentioned in a nested hierarchy (e.g., "El Prado Museum, Madrid, Spain"), extract **ONLY the single, most specific Point of Interest (POI)** (i.e., "El Prado Museum"). Use broader context (like "Madrid" or "Spain") *only* to accurately find the POI's coordinates.
2.  **Broader Location Rule (Last Resort):** **ONLY** extract a broad location (Rank 4 or higher, e.g., 'City', 'Country') if **NO specific POI (Rank 1-3)** or discernible subject matter is present in the caption.
3.  **Explicit List Exception (Multiple Locations):** The *only* time you should extract multiple locations is if the caption contains an **EXPLICIT LIST** of *different* locations. This includes text prepended with **icons (📍, 📷, 🗺️), bullet points,** numbers (1., 2.), or letters (a., b.). In this case, extract *every* location listed.
4.  **Conditional Hashtag Check (Secondary Source):** **ONLY** consider hashtags for location extraction if the main body of the caption (Rules 1-3) does not yield any valid location. If used, apply Rules 1-3 to the hashtags.

---

**Output and Cascading Confidence Logic:**
Return **ONLY** a single, valid JSON *list*. The list must adhere to the following cascading confidence criteria:

* **Priority 1 (High Confidence):** Attempt to extract all locations that meet the **Final Guardrail** and have a **confidence score of 0.8 or higher.**
* **Priority 2 (Lower Confidence Fallback):** If the list resulting from Priority 1 is **EMPTY**, then return the best available location(s) with a **confidence score between 0.5 and 0.79.**
* If no location meets even the 0.5 confidence threshold, return an empty list `[]`.

**Final Guardrail (Universal Constraint):** All extracted locations **MUST NOT** be non-geographic entities, names of people, brands, common nouns, or places with vague/non-resolvable coordinates.

Each object in the list **MUST** have the following ten keys:

1.  `"title"`: The concise name of the location (max 5 words).
2.  `"subtitle"`: A brief description (max 10-15 words).
3.  `"lat"`: The latitude.
4.  `"lon"`: The longitude.
5.  `"type"`: The specific type of location (e.g., 'river', 'forest', 'city', 'building', 'restaurant').
6.  `"class"`: The generic classification (e.g., 'amenity', 'place', 'natural').
7.  `"confidence"`: A numerical score (0.0 to 1.0).
8.  `"rank"`: Location hierarchy (1=most specific, 9=broadest):
    * 1: POI/Building
    * 2: Site/Neighborhood/Park
    * 3: Town/Village
    * 4: City
    * 5: County/Province
    * 6: State/Region
    * 7: Country
    * 8: Supranational Region / Large Natural Feature
    * 9: Continent
9.  `"page"`: Numerical order of appearance *only* if the location is part of an explicit list (start from 1), otherwise `null`.
10. **`"hierarchy"`: A list of names representing the full geographic context, from most specific to broadest (e.g., `["El Prado Museum", "Madrid", "Spain"]`).**

Caption: "{caption}"""

# --- Script Configuration --
model_name = 'gemini-2.5-flash'

# --- INPUT/OUTPUT FILENAMES ---
caption_filename_glob = '*.caption.txt' # The input files
location_filename_suffix = 'locations.gemini.json' # The output file suffix

# Set this path to the root of your data (e.g., where the 'username' folders are)
search_path = Path('./gallery-dl/')

# Force to reload all captions.
REWRITE = False

# Set the total number of times to try
MAX_ATTEMPTS = 5
BASE_WAIT_TIME = 2

# Flag to stop execution
stop_execution = False
# -----------------------------------------------------------------


def remove_old_location_files(media_root_dir_str):
    """
    Removes all existing Gemini location files using flexible glob patterns
    to clean up previous runs (both generic and post_id named).
    """
    media_root_dir = Path(media_root_dir_str)

    if not media_root_dir.exists():
        return

    print("1. Cleaning up old Gemini location files...")
    count_removed = 0

    # 1. Pattern for generic files: locations_gemini.json
    for filepath in media_root_dir.rglob(location_filename_suffix):
        try:
            filepath.unlink()
            count_removed += 1
        except Exception:
            pass

    # 2. Pattern for post_id named files: *.locations_gemini.json
    for filepath in media_root_dir.rglob(f'*.{location_filename_suffix}'):
        if filepath.name != location_filename_suffix:  # Avoid double counting the generic file
            try:
                filepath.unlink()
                count_removed += 1
            except Exception:
                pass

    print(f"   -> Removed {count_removed} previous Gemini location file(s).")






# --- MAIN EXECUTION ---
if __name__ == "__main__":

    # Run the cleanup first
    #remove_old_location_files(search_path)

    print(f"\n2. Searching for caption files in path: {search_path}")

    # Find all the new *.caption.txt files recursively.
    files_list = sorted(list(search_path.rglob(caption_filename_glob)))
    print(f"Found {len(files_list)} posts to process.")

    n_posts = len(files_list)

    for i, f in enumerate(files_list):
        # f is the path to the current [post_id].caption.txt file

        # --- Derive output filename: [post_id].locations_gemini.json ---
        post_id = f.stem.split('.')[0]  # Extracts post_id from "postid.caption.txt"
        output_file_path = f.parent / f"{post_id}.{location_filename_suffix}"

        # Skip logic check (only needed if REWRITE=False, though we cleaned up)
        if not REWRITE and output_file_path.exists():
            try:
                with output_file_path.open('r') as fj:
                    data = json.load(fj)
                print(f"{i:4}/{n_posts}. [READY] Post processed <{f.parent.stem}/{post_id}> | {len(data)} location(s) found.")
                continue
            except json.JSONDecodeError:
                print(f"{i:4}/{n_posts}. [CORRUPT] Location file corrupted. Reprocessing post <{f.parent.stem}>...")
            except Exception:
                pass

        try:
            print(f"{i:4}/{n_posts}. [NEW] Processing post <{f.parent.stem}/{post_id}>... Attempt ", end='')
            with f.open('r', encoding='utf-8') as ft:
                caption = ft.read()

            prompt = prompt_template.format(caption=caption)
        except Exception as e:
            print(f"[Error] Could not read file: {e}")
            continue

        # --- Start Retry Loop ---
        for attempt in range(MAX_ATTEMPTS):
            try:
                prefix = ", " if attempt > 0 else ""
                print(f"{prefix}{attempt + 1}/{MAX_ATTEMPTS} ", end='')

                # API Call
                response = client.models.generate_content(
                    model=model_name,
                    contents=prompt
                )

                # --- Successful Response ---
                response_text = response.text.strip() \
                    .replace("```json", "").replace("```", "")
                data_list = json.loads(response_text)

                # Save the successful result in the same folder
                with output_file_path.open('w', encoding='utf-8') as fo:
                    json.dump(data_list, fo, indent=4)
                print(f" | {len(data_list)} location(s) found.", end='')

                # Wait a random duration
                wait_duration = random.uniform(1.5, 5.5)
                print(f" | Waiting for {wait_duration:.2f} seconds...")
                time.sleep(wait_duration)

                break  # Exit retry loop

            except ClientError as e:
                # Handling 4xx errors
                if e.code == 400:
                    if any(msg in str(e) for msg in ["API key not valid", "API key expired"]):
                        print("\n[Fatal Error] Invalid/Expired API Key. Stopping.")
                        stop_execution = True;
                        break
                    print(f"\n[Error] Unrecoverable 400 error: {e} Skipping post.");
                    break

                elif e.code == 429:
                    print(f"[Error] Quota exceeded (429).")
                    if attempt == MAX_ATTEMPTS - 1:
                        print("Last attempt failed. No more attempts. Stopping.")
                        stop_execution = True;
                        break

                    error_message = str(e)
                    match = re.search(r"Please retry in ([\d.]+)s", error_message)
                    wait_time = float(match.group(1)) + 10 if match else 180.0
                    text = 'suggested by the API' if match else 'fallback'
                    print(f"Waiting for {wait_time:.2f} seconds {text}.")
                    time.sleep(wait_time)

                else:
                    print(f"\n[Fatal Error] Unhandled ClientError ({e.code}). Stopping execution.")
                    stop_execution = True;
                    break

            except ServerError as e:
                # Handling 5xx errors
                print(f"[Error] ServerError (5xx): {e}")
                if attempt == MAX_ATTEMPTS - 1:
                    print("Last attempt failed. No more retries. Stopping.")
                    stop_execution = True;
                    break

                # --- This is the "Exponential Backoff" ---
                # attempt 0: 2^0 * 2 = 2s
                # attempt 1: 2^1 * 2 = 4s
                # attempt 2: 2^2 * 2 = 8s
                # ...plus a random 'jitter' to prevent all clients retrying at once
                wait_time = (BASE_WAIT_TIME * (2 ** attempt)) + random.uniform(0, 1)

                print(f"Waiting {wait_time:.2f}s before next retry (Exponential Backoff)...")
                time.sleep(wait_time)

            except json.JSONDecodeError as e:
                print(f"\n[Error] Could not decode JSON from response. Skipping post.")
                break

            except Exception as e:
                print(f"\n[Fatal Error] An unexpected error occurred: {e}. Stopping execution.")
                stop_execution = True;
                break

        if stop_execution:
            break