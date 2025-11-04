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

## 🔐 Quick Setup  

### 1.1 Setting Up Instagram Authentication

This project requires your Instagram session cookies to download private content or 
to avoid rate-limiting. You must provide these cookies as a GitHub Actions Secret.
This process is **manual** and **cannot be automated** due to Instagram's security 
measures. You will need to repeat these steps every few weeks when your session cookie 
expires and the action starts to fail.

#### Step 1: Export Your `cookies.txt` File

1.  **Install a Cookie Exporter Extension:**
    We recommend using an open-source, local-only extension like:
    * **Chrome/Edge:** [Get cookies.txt LOCALLY](https://chromewebstore.google.com/detail/get-cookiestxt-locally/cclelndahbckbenkjhflpdbgdldlbecc)
    * **Firefox:** [cookies.txt](https://addons.mozilla.org/en-US/firefox/addon/cookies-txt/)

2.  **Export Your Cookies:**
    * Log in to [instagram.com](https://www.instagram.com) on your browser.
    * Click the cookie extension's icon in your toolbar.
    * Click the "Export" or "Export as .txt" button to download the `cookies.txt` file for the current site.

#### Step 2: Convert the Cookie File to Base64

To store the cookie file safely in GitHub, you must convert it to a Base64 string.

1.  Open a terminal (like PowerShell, Terminal, or bash).
2.  Navigate to the directory where you saved your `cookies.txt` file.
3.  Run the command for your operating system:

    * **On macOS or Linux:**
        ```bash
        base64 cookies.txt
        ```

    * **On Windows (in PowerShell):**
        ```powershell
        [Convert]::ToBase64String([IO.File]::ReadAllBytes("cookies.txt"))
        ```
4.  This will output a single, very long string of text. **Copy this entire string** to your clipboard.

#### Step 3: Add the Secret to GitHub

1.  In your GitHub repository, go to **Settings** > **Secrets and variables** > **Actions**.
2.  Click the **New repository secret** button.
3.  **Name:** `IG_COOKIE_64`
4.  **Value:** Paste the single long Base64 string you just copied.
5.  Click **Add secret**.

The GitHub Action will now be able to authenticate as you. If the action fails in the 
future, the first thing you should do is generate and update this secret with a fresh 
cookie.


### 1.2 Setting your Gemini API Key

If you’re using Gemini to extract caption locations, you'll need a Google AI API key.

1.  **Get Your Key:**
    * Go to [Google AI Studio](https://aistudio.google.com/app/apikey).
    * Click "**Create API key**" and copy the key.

2.  **Add the Secret to GitHub:**
    * In your repository, go to **Settings** > **Secrets and variables** > **Actions**.
    * Click **New repository secret**.
    * **Name:** `GOOGLE_API_KEY`
    * **Value:** Paste your API key.


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


#### 3.1 Custom Icon Generation

A significant limitation of Google My Maps' KML importer is that it **ignores most KML styling 
tags**, including `<color>` and references to default icons. While the KML standard supports 
these features, Google Maps will not render them, resulting in all placemarks reverting to a 
default pin.

The *only* reliable method to customize placemark icons in Google My Maps is to use image URLs.

This project's workflow is built around this limitation. We do not use default pins. Instead, 
we use a custom script to generate unique PNG icons for every placemark type. These generated 
icons are hosted in this repository (in `web/static/img/markers/`), allowing them to be 
publicly accessed via GitHub. The KML export function is then configured to point directly to 
these public image URLs (e.g., `...github.io/.../static/img/markers/village.png`), which Google
 Maps can correctly load.

#### 3.2 How to Generate the Icons

The icons are created using a standalone browser tool included in this repository.

1.  **Generator:** Open the `web/generate_icons.html` file in your local browser.
2.  **Configuration:** The tool reads its configuration from the `MARKER_STYLE` object in `settings.js`.
3.  **Export:** When you click the button, the tool uses the Font Awesome font to draw the configured icons onto an HTML canvas and downloads them as individual PNG files, bundled into a `markers.zip`.
4.  **Storage:** You must unzip this file and upload the new or updated PNG icons to the `web/static/img/markers/` directory in this repository and commit the changes.

#### 3.3 Important Notes & Troubleshooting

* **Unicode is Required:** For the `web/generate_icons.html` generator to work, each entry in the `MARKER_STYLE` object *must* have a `unicode` property (e.g., `unicode: '\uf51d'`). This is the unique code for the Font Awesome icon.
* **"Some Icons Are Not Working" (Fix):** If you see a blank icon or a default circle in your generated PNGs, it means the `unicode` property for that type in `settings.js` is either **missing or incorrect**. To fix it:
    1.  Find the icon you want on the [Font Awesome 6](https://fontawesome.com/icons) website.
    2.  Click the icon to see its details.
    3.  Copy its Unicode value (e.g., `f51d`).
    4.  Add it to the `MARKER_STYLE` object in `settings.js`, like `unicode: '\uf51d'`.

---
