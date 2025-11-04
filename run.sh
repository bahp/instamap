#!/bin/bash
# This is a shell script to run gallery-dl with your specified options

# -- Display a simple greeting --
echo "==============================="
echo "Running script (Linux/macOS)"
echo "==============================="
echo

echo "Current Date and Time: $(date)"

# === Configuration ===
USERNAME="bernardhp"
POST_TYPE="saved"

# use -v for verbose
# use -w for warning
# use --no-download to avoid download media

# === Run gallery-dl (download metadata) ===
echo "Running gallery-dl..."

# Extract gallery automatically from browser
#gallery-dl -w "https://www.instagram.com/$USERNAME/$POST_TYPE/" \
#    --cookies-from-browser firefox \
#    --write-metadata --no-download \
#    --download-archive ./gallery-dl/archive.sqlite3 \
#    --skip abort:15 | grep "[download]"

# Load cookies from .txt file
gallery-dl -w "https://www.instagram.com/$USERNAME/$POST_TYPE/" \
    --cookies "cookies.txt" \
    --write-metadata --no-download \
    --download-archive ./gallery-dl/archive.sqlite3

#gallery-dl -v "https://www.instagram.com/$USERNAME/$POST_TYPE/" \
#    --cookies-from-browser firefox \
#    --write-metadata --no-download \
#    -o extractor.archive=./gallery-dl/archive.sqlite3 | grep "[download]"

# === Run Gemini (extract location)
python create_caption_files.py
python extract_locations_gemini.py
python merge_metadata.py
python convert_json2js.py

# -- Wait for the user to finish reading --
read -p "Press Enter to continue..."
