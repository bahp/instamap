
import re
import pandas as pd
import numpy as np

from pathlib import Path

# Read summary
path = '../../data/bernardhp/_summary.csv'
path = '../../data/bernardhp/posts'

# Tokyo
lat = 35.652832
lon = 139.839478

# Extract stems
files = list(Path(path).glob('**/post.json'))
stems = [f.parent.stem for f in files]

# Create DataFrame
df = pd.DataFrame()
df['shortcode'] = stems
df['lat'] = lat + np.random.rand(len(stems), 1) * 5
df['lon'] = lon + np.random.rand(len(stems), 1) * 5


print(df)

df.to_json('records.json', orient='records', indent=4)