# Libraries
import json
from pathlib import Path

folder = Path('../../data/bernardhp/')
#folder = Path('./data/bernardhp/')

folder = Path('.')
# Define your input and output filenames
json_filename = folder / 'data.json'  # Your source .json file
js_filename = folder / 'web' / 'data.js'     # The .js file you want to create

try:
    # 1. Read the content of the .json file
    with open(json_filename, 'r', encoding='utf-8') as f:
        json_content = f.read()

    # 2. Create the JavaScript variable string
    js_content = f"var data = {json_content};"

    # 3. Write the new string to the .js file
    with open(js_filename, 'w', encoding='utf-8') as f:
        f.write(js_content)

    print(f"Successfully converted {json_filename} to {js_filename}")

except FileNotFoundError:
    print(f"Error: The file '{json_filename}' was not found.")
except Exception as e:
    print(f"An error occurred: {e}")
