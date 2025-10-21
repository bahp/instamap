# Libraries
import glob
import json
import pandas as pd

from src.utils import AttrDict
from src.utils import Fetch

# Constants
PATH = 'test'

# Variables
smmry = pd.DataFrame()


# Loop finding all json files
for i, f in enumerate(glob.glob('%s/**/*.json' % PATH, recursive=True)):
    print("%4d. Loading... %s" % (i, f))

    # Load data
    with open(f) as json_file:
        data = json.load(json_file)

    # Create fetcher
    L = Fetch(data)



    # Normalize and combine
    smmry = pd.concat([smmry, L.json_normalize()])
    #smmry = pd.concat([smmry, pd.json_normalize(data)])

print(smmry)

#smmry.to_csv('%s/posts.csv' % PATH)
#print(smmry.columns)
#print(smmry['_node.display_resources'])

