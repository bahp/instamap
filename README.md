# 🤖 Automated Instagram Archival with gallery-dl and GitHub Actions

This guide outlines the process for automating `gallery-dl` to download 
your saved Instagram posts and/or metadata into a GitHub repository, while 
ensuring videos are skipped and files are properly organized.

## 1. Data Download & Filtering (gallery-dl)

The core archival tool is `gallery-dl`, executed on a scheduled basis. 

> ⚠ **Note:** The browser needs to be closed for the cookie extraction to work properly.

> ⚠ **Note:** It seems that automatic cookie extraction does not work for chrome

**Initial/Manual Download Commands:**

| Target | Command | Notes | 
|  ----- | ----- | ----- | 
| **Instagram Saves** (Specific User) | `$ gallery-dl -v "https://www.instagram.com/bernardhp/saved/" --cookies-from-browser firefox --write-metadata --filter "date >= datetime(YYYY, MM, DD) or abort()"` | Uses Firefox, includes date filtering, and writes comprehensive metadata (`.json`). | 
| **Twitter Media** | `$ gallery-dl https://twitter.com/username/media --filter "date >= datetime(2025, 9, 28) or abort()"` | Downloads all media from a user's timeline, filtered by date. | 
| **Instagram Saves** (Archiving setup) | `$ gallery-dl -v "https://www.instagram.com/bernardhp/saved/" --cookies-from-browser chrome --write-metadata -o extractor.archive='./gallery-dl/archive.sqlite3'` | Sets up the archive database to only download new content on subsequent runs. | 


## 2. Post-Processing and Data Enrichment

Once media files and initial metadata are downloaded, Python scripts execute tasks to clean, enrich, and merge the data.

### Step 2.1: Create Caption Files

This step converts the full caption data contained within the raw `.json` metadata into separate, easily readable text files (e.g., `post_shortcode/caption.txt`).

**Command:**
`$ python create_caption_files.py`

### Step 2.2: Extract Locations using Gemini API

This crucial step leverages the Gemini API's intelligence capabilities to analyze post text and/or images, identifying, extracting, and standardizing geographical locations.

**Command:**
`$ python extract_locations_gemini.py`

### Step 2.3: Merge Metadata

This step combines the raw `gallery-dl` metadata with the newly extracted location data from the Gemini script, creating a unified, enriched master metadata file.

**Command:**
`$ python merge_metadata.py`

### Step 2.4: Convert Data for Web Visualization

The final enriched data is converted from its current format (e.g., JSON) into a JavaScript-compatible file format (e.g., a `.js` file with an array variable) for easy loading and plotting on a Leaflet web map.

**Command:**
`$ python convert_json2js.py`