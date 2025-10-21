from google import genai
import os
import json
import time  # Import the time module for sleeping

try:
    # --- 1. Configuration ---
    API_KEY = os.environ["GOOGLE_API_KEY"]
    API_KEY = "AIzaSyAUqop8uRbk_Tien5Dy2H7-bKlRK7RR4Mc"
    client = genai.Client(api_key=API_KEY)

except KeyError:
    print("Error: GOOGLE_API_KEY environment variable not set.")
    print("Please set the variable and try again.")
    exit()
except Exception as e:
    print(f"Error initializing the model: {e}")
    exit()

# --- 2. Your Captions ---
captions_list = [
    "Lost in time beneath the captivating Stonehenge arches at golden hour ✨ 📍England 🏴󠁧󠁢󠁥󠁮󠁧󠁿 #DiscoverEngland",
    "Grabbing a slice of the best pizza in New York! Nothing beats this view. 🍕 📍Grimaldi's, Brooklyn",
    "Amazing day in Paris! 🇫🇷\n📷 The Louvre\n📍Eiffel Tower\n🗺️ Notre Dame Cathedral",
    "Just a quiet day at the museum, staring at the Mona Lisa. It's smaller than I thought! 🎨 #Louvre #Paris"
]

# --- 3. The Prompt ---
prompt_template = """
You are a geography and data extraction expert.
I will give you a social media post caption.
Extract *all* specific geographic locations from the caption.

The caption may contain multiple locations, often in a list where each line 
is prepended with an icon like 📍, 📷, or 🗺️. They might also be included in
the hashtags.

Return ONLY a single, valid JSON *list*.
Each object in the list must have the following four keys:
1. "title": A short, catchy title for the map pin (max 5 words).
2. "subtitle": A brief description (max 10 words).
3. "lat": The latitude.
4. "lon": The longitude.

If a location is mentioned but too broad (e.g., "England"), find the coordinates 
for the main subject (e.g., Stonehenge).
If you cannot find any specific locations, return an empty list [].

Caption: "{caption}"
"""

# --- 4. Process the Captions (NEW: with retry logic) ---
all_locations_data = []
model_name = 'gemini-2.5-flash'
MAX_RETRIES = 5  # Try a maximum of 5 times

print("Starting to process captions...")
for caption in captions_list:
    print(f"\nProcessing caption: '{caption[:50]}...'")
    prompt = prompt_template.format(caption=caption)

    # --- Start Retry Loop ---
    for attempt in range(MAX_RETRIES):
        try:
            # Use the client to generate content
            response = client.models.generate_content(
                model=model_name,
                contents=prompt
            )

            # If successful, parse the JSON
            response_text = response.text.strip().replace("```json", "").replace("```", "")
            data_list = json.loads(response_text)

            if data_list:
                all_locations_data.extend(data_list)
                print(f"Success: Extracted {len(data_list)} location(s).")
            else:
                print("Success: No locations found in this caption.")

            # If successful, break out of the retry loop
            break

        except genai.errors.ServerError as e:
            # This catches the 503 error
            if attempt < MAX_RETRIES - 1:
                wait_time = 2 ** attempt  # Exponential backoff (1, 2, 4, 8 seconds)
                print(f"  > Model overloaded (503). Retrying in {wait_time} second(s)...")
                time.sleep(wait_time)
            else:
                print(f"Error: Failed to process caption after {MAX_RETRIES} attempts.")
                print(f"  > Last error: {e}")

        except json.JSONDecodeError:
            print(f"Error: Could not decode JSON from response: {response.text}")
            break  # Don't retry if JSON is bad
        except Exception as e:
            print(f"Error processing caption: {e}")
            break  # Don't retry for other errors
    # --- End Retry Loop ---

# --- 5. Show the Final Result ---
print("\n--- All Extracted Data (from all captions) ---")
print(json.dumps(all_locations_data, indent=2))

# --- 6. Save the Data to a JSON File ---
output_filename = "locations_data.json"
try:
    with open(output_filename, 'w', encoding='utf-8') as f:
        json.dump(all_locations_data, f, indent=4)
    print(f"\nSuccessfully saved all {len(all_locations_data)} locations to {output_filename}")
except IOError as e:
    print(f"Error: Could not write to file {output_filename}: {e}")