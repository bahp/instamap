
import re
import pandas as pd
import numpy as np

from pathlib import Path

#
path = './data/bernardhp/_summary.csv'

# Tokyo
lat = 35.652832
lon = 139.839478


files = Path()

# Create dataframe
df = pd.DataFrame(path)

"""
df['shortcode'] = x
df['random'] = np.random.rand(len(x), 1)
df['lat'] = df.random + lat
df['lon'] = df.random + lon

print(df)

df.to_json('records.json', orient='records', indent=4)
"""