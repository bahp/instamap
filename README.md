# 📍 InstaMap — Visualize Instagram Posts on a Map

![Version](https://img.shields.io/badge/version-1.0.0-blue?style=flat-square&logo=github)
![GitHub Actions](https://img.shields.io/github/actions/workflow/status/yourusername/instamap/main.yml?style=flat-square&logo=github)
![Python](https://img.shields.io/badge/python-3.11+-brightgreen?style=flat-square&logo=python&logoColor=white)
![License](https://img.shields.io/badge/license-MIT-lightgrey?style=flat-square&logo=open-source-initiative)
![Leaflet](https://img.shields.io/badge/Leaflet-199900?style=flat-square&logo=leaflet&logoColor=white)

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

## 🔐 Setup  

### 1. Export Your Instagram Cookie  

1. Log in to Instagram in your web browser (firefox).  
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


## 🗺️ How to Import KML into Google Maps

1.  Generate your map on Instamap.
2.  Open the left side panel and click the  **"Export to Google Maps"** button to save the `.kml` file. 
3.  Go to [Google My Maps](https://www.google.com/mymaps).
4.  Click the **"+ Create a New Map"** button.
5.  In the top-left panel (under "Untitled layer"), click the **"Import"** link.
6.  Select the `.kml` file you just downloaded from your computer.
7.  Your map, with all its custom icons and data, will be loaded and displayed.
8.  It will also be available on your Google Maps App!


#### 📍 Custom Icon Generation

This project does not use the default Google Maps pins. Instead, it uses custom-generated 
PNG icons to style placemarks based on their type.

### How it Works

1.  **Generator:** The `web/generate_icons.html` file is a standalone browser tool. When you open 
    this file locally, it will:
    * Read the style configurations from `settings.js`.
    * Use the Font Awesome font and unicodes to draw icons onto an HTML canvas.
    * Save these icons as individual PNG files, bundled into a `markers.zip` for download.

2.  **Configuration:** The icon designs (color and Font Awesome icon) are controlled by 
    the `MARKER_STYLE` object inside `settings.js`.

3.  **Storage:** The generated PNG icons (e.g., `village.png`, `tourism.png`) must be 
    uploaded to the `web/static/img/markers/` directory in your repository.

4.  **Usage:** The KML export function is built to point to the public GitHub URL 
    for these files (e.g., `...github.io/.../static/img/markers/village.png`). Google Maps 
    then loads these images as the icons.

### ⚠ Important Notes & Troubleshooting

* **Default Colors/Icons Will Not Work:** The KML file is configured to use **image URLs only**. 
    The old method of setting a `<color>` on a default pin is not supported by google maps and
    hence not used for this workflow.
    
* **Unicode is Required:** For the `create_icons.html` generator to work, each entry in the
    `MARKER_STYLE` object *must* have a `unicode` property (e.g., `unicode: '\uf51d'`). This 
    is the unique code for the Font Awesome icon.
    
* **"Some Icons Are Not Working" (Fix):** If you see a blank icon or a default circle for some 
   types, it means the `unicode` property for that type in `settings.js` is either **missing 
   or incorrect**. To fix it:
    1.  Find the icon you want on the [Font Awesome 6](https://fontawesome.com/icons) website.
    2.  Click the icon to see its details.
    3.  Copy its Unicode value (e.g., `f51d`).
    4.  Add it to the `MARKER_STYLE` object in `settings.js`, like `unicode: '\uf51d'`.

---
