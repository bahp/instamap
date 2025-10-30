# 📍 InstaMap — Visualize Your Saved Instagram Posts on a Map  

![InstaMap Logo](https://img.shields.io/badge/InstaMap-v1.0-blue?style=for-the-badge&logo=mapbox)
![GitHub Actions](https://img.shields.io/github/actions/workflow/status/yourusername/instamap/main.yml?style=for-the-badge&logo=github)
![Python Version](https://img.shields.io/badge/python-3.11+-blue?style=for-the-badge&logo=python)
![License: MIT](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)
![Made with Leaflet](https://img.shields.io/badge/Made%20with-Leaflet-199900?style=for-the-badge&logo=leaflet)

---

**InstaMap** is an automated tool that downloads your saved Instagram 
posts using **[gallery-dl](https://github.com/mikf/gallery-dl)**, extracts 
their geolocation data, and displays them on an interactive **Leaflet** map.
Each post is embedded directly on the map at its corresponding location, 
allowing you to explore your saved content geographically.  

The project also uses **Gemini** (Google’s generative AI) to analyze post 
captions and identify additional locations mentioned in the text — adding 
extra context and depth to your map.  

All steps — from downloading posts to generating and deploying the 
interactive map — are almost fully automated via **GitHub Actions**.  

![App Screenshot](screenshot.png)

---

## 🚀 Features  

- 🖼️ **Downloads saved Instagram posts** via `gallery-dl`  
- 📍 **Extracts geolocation data** from Instagram metadata  
- 🧠 **Uses Gemini AI** to detect extra locations mentioned in captions  
- 🗺️ **Generates an interactive Leaflet map** with embedded Instagram posts  
- ⚙ **Runs automatically on GitHub Actions** — no local setup needed  
- 🔒 **Uses secure GitHub Secrets** for authentication with Instagram  

---

## 🧩 How It Works  

1. **Authentication**  
   - Instagram recently limited automated logins using usernames and passwords.  
   - `gallery-dl` now requires a **browser session cookie** for authentication.  
   - You’ll export this cookie from your browser and add it as a **GitHub Secret**.  

2. **Data Extraction**  
   - `gallery-dl` downloads your saved posts using the provided cookie.  
   - Each post’s metadata is parsed for location data.  

3. **AI Location Enrichment**  
   - The **Gemini API** analyzes captions to find additional mentioned locations.  

4. **Map Generation**  
   - Posts are plotted on a **Leaflet** map.  
   - Each marker displays an **Instagram embed** of the post.  

5. **Automation via GitHub Actions**  
   - A scheduled workflow runs the entire process automatically.  
   - The generated map is committed or deployed (e.g., via GitHub Pages).  

---

## 🔐 Setup  

### 1. Export Your Instagram Cookie  

1. Log in to Instagram in your web browser.  
2. Open the browser’s **Developer Tools → Application → Cookies**.  
3. Copy the value of the `sessionid` cookie.  

### 2. Add It as a GitHub Secret  

In your repository:  
1. Go to **Settings → Secrets and variables → Actions → New repository secret**  
2. Create a new secret:  
   - **Name:** `INSTAGRAM_SESSIONID`  
   - **Value:** your copied cookie  

### 3. Add Your Gemini API Key  

If you’re using Gemini to extract caption locations:  
1. Create another GitHub Secret:  
   - **Name:** `GEMINI_API_KEY`  
   - **Value:** your Gemini key  

---



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

Once media files and initial metadata are downloaded, Python scripts execute 
tasks to clean, enrich, and merge the data.

### Step 2.1: Create Caption Files

This step converts the full caption data contained within the raw `.json` 
metadata into separate, easily readable text files (e.g., `post_shortcode/caption.txt`).

**Command:**
`$ python create_caption_files.py`

### Step 2.2: Extract Locations using Gemini API

This crucial step leverages the Gemini API's intelligence capabilities 
to analyze post text and/or images, identifying, extracting, and standardizing 
geographical locations.

**Command:**
`$ python extract_locations_gemini.py`

### Step 2.3: Merge Metadata

This step combines the raw `gallery-dl` metadata with the newly extracted 
location data from the Gemini script, creating a unified, enriched master 
metadata file.

**Command:**
`$ python merge_metadata.py`

### Step 2.4: Convert Data for Web Visualization

The final enriched data is converted from its current format (e.g., JSON) 
into a JavaScript-compatible file format (e.g., a `.js` file with an array 
variable) for easy loading and plotting on a Leaflet web map.

**Command:**
`$ python convert_json2js.py`