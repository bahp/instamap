# Libraries
import pandas as pd
from pathlib import Path

# -------------------------------------------------
# Functions
# -------------------------------------------------

def overlap_area(box1, box2):
    """"""
    # Extract coordinates of the bounding boxes
    x1, y1, w1, h1 = box1
    x2, y2, w2, h2 = box2
    # Calculate the overlap along the x-axis
    overlap_x = max(0, min(x1 + w1, x2 + w2) - max(x1, x2))
    # Calculate the overlap along the y-axis
    overlap_y = max(0, min(y1 + h1, y2 + h2) - max(y1, y2))
    # Calculate the area of overlap
    overlap_area = overlap_x * overlap_y
    # Return
    return overlap_area

def check_overlap(box1, box2):
    """"""
    # Extract coordinates of the bounding boxes
    x1, y1, w1, h1 = box1
    x2, y2, w2, h2 = box2
    # Check for overlap along the x-axis
    x_overlap = (x1 < x2 + w2) and (x1 + w1 > x2)
    # Check for overlap along the y-axis
    y_overlap = (y1 < y2 + h2) and (y1 + h1 > y2)
    # Return True if there is overlap along both axes
    return x_overlap and y_overlap

def bounding_box_area(box):
    """"""
    # Extract coordinates of the bounding box
    x1, y1, x2, y2 = box
    # Calculate width and height from the coordinates
    width = abs(x2 - x1)
    height = abs(y2 - y1)
    # Calculate the area of the bounding box
    area = width * height
    # Return
    return area


def bounding_box_format(box):
    """"""
    import ast
    box = ast.literal_eval(box)
    box = [float(num) for num in box]
    return box



# Select path
PATH = Path('./data/bernardhp/')

# Columns
COLUMNS = [
    'text',
    'confidence',
    'importance',
    'place_id',
    'lat',
    'lon',
    'class',
    'type',
    'place_rank',
    'addresstype',
    'display_name'
]

# Load summary
df = pd.read_csv(PATH / '_summary.csv')

# Show
print(df)


# -------------------------------------
# Example 1
# -------------------------------------
# A single post ends up having too many locations
# and creating a mess in the map. Try to identify
# which location is more accurate.

# Interesting shortcode
shortcodes = ['CyvItQMMGc6'] # multi-image
shortcodes = ['CGaiVQvBp5t']
shortcodes = ['Cu9gio6MN6N']
shortcodes = ['Cxj-ncYitkY']
shortcodes = ['CuZyZp0sRUP']

# Filter
aux = df[df.shortcode.isin(shortcodes)]

import ast
#
print(aux.columns)
print(aux[COLUMNS])

# Convert string to list
aux.boundingbox = aux.boundingbox.apply(bounding_box_format)

aux['area'] = aux.boundingbox.apply(bounding_box_area)

print(aux[COLUMNS + ['area']])
box1 = aux.boundingbox.values[0]
box2 = aux.boundingbox.values[1]

if check_overlap(box1, box2):
    print("Bounding boxes overlap.")
    overlap_area_value = overlap_area(box1, box2)
    print(f"Overlap area: {overlap_area_value}")
else:
    print("Bounding boxes do not overlap.")

# Load json
import json

p = PATH / 'posts' / 'CuZyZp0sRUP' / 'post.json'
with open(p, 'r') as f:
    data = json.load(f)
print(json.dumps(data, indent=4))

shortcodes = [
    'CyvItQMMGc6',
    'CGaiVQvBp5t',
    'Cu9gio6MN6N',
    'Cxj-ncYitkY',
    'CuZyZp0sRUP',
    'CJJcb_Hhpao',
    'CYGh_OUtqfo',
    'CyOnnwrtVBv'
]

for s in shortcodes:
    p = PATH / 'posts' / s / 'post.json'
    with open(p, 'r') as f:
        data = json.load(f)
    print(s, data['node']['__typename']) # GraphSidecar

    geo = df[df.shortcode.isin([s])]
    print(geo[COLUMNS])




