# Libraries
import glob
import json
import pandas as pd
from pathlib import Path


from src.settings import DEFAULT_TAGGERS
from src.utils.ner import clean_text
from src.utils.ner import select_entities_from_df
from src.utils.ner import NERRule
from src.utils.ner import NERFlair


# ----------------------------------
# Methods
# ----------------------------------
def get_country_name(matches):
    """

    .. note: To improve, instead of selecting the first country
             that appears, double check that all the entries for
             a country are referring to the same country. And
             think what to do if many different countries found.

    Parameters
    ----------
    matches: list of dicts
        List of dictionaries with match information.
    """
    # Libraries
    import pycountry

    # Find whether there is country information (text).
    countries = list(filter(lambda d: d.get('attr', '') == 'text', r))
    if countries:
        return countries[0]['text']

    # Find whether there is country information (flag).
    countries = list(filter(lambda d: d.get('attr', '') == 'flag', r))
    if countries:
        flag = countries[0]['text']
        return pycountry.countries.get(flag=flag).name

    return None

def query_add_country(matches):
    """"""
    # Libraries
    import pycountry
    from nested_lookup import nested_lookup

    # Get mentioned country
    country = get_country_name(matches)
    if country is None:
        return matches

    # Add query information
    for entry in matches:
        location = nested_lookup("location", entry)
        if location:
            country = country.lower()
            location = clean_text(location[0])
            if not country in location:
                entry['query'] = '%s, %s' % (location, country)

    # A flag entry should have the name of the country as query
    # Can be done in a datframe much more cleaner
    # df['year'] = df['date'].apply(lambda x: x.year)
    for entry in matches:
        if (entry.get('rule', None) == 'country'):
           if (entry.get('attr', None) == 'flag'):
                entry['query'] = pycountry.countries.get(flag=entry['text']).name



    # Return
    return matches


def prepare_geolocation_query(matches):
    """"""
    ##
    matches = query_add_country(matches)
    for e in matches:
        if not 'query' in e:
            e['query'] = e['text']


    return matches

def select_geolocation_query(matches):
    """"""
    if not matches:
        return None

    # Create DataFrame
    df = pd.DataFrame(matches)
    df['query'] = df['query'].str.lower()
    df = df.drop_duplicates(subset=['query'])

    # Count types of regexp
    counts = df.rule.value_counts()

    # Keep bullets
    if 'bullets' in counts:
        df = df[~df.rule.isin(['country'])]
    if 'icon' in counts:
        df = df[~df.rule.isin(['country'])]

    return df



def compute_levenshtein_matrix(vector):
    """Compute distance matrix."""
    # Libraries
    from scipy.spatial.distance import cdist
    from Levenshtein import ratio
    # Format
    matrix = cdist(
        vector.reshape(-1, 1),
        vector.reshape(-1, 1),
        lambda x, y: ratio(x[0], y[0]))
    # Return
    return matrix


# ----------------------------------
# Load captions
# ----------------------------------
# These methods return a dictionary in which the key
# corresponds to the shortcode of the pot and the value
# contains the caption.

# ----------------------------------
# Text Formatting
# ----------------------------------
# Select the shortcodes
PATH = Path('./data/borgodeiborghi/posts/')
PATH = Path('./data/bernardhp/posts')



# -----------------------------------
# Single example
# -----------------------------------
# Define shortcode
shortcode = 'CzBYpc5ocQb' #'CprnXDRgpBB'
shortcode = 'CzD6fazOqTe'
#shortcode = 'CvE3TlxLgKU'
#shortcode = 'B5NqBLMJGZM'


# Define full post path
fullpath = PATH / shortcode

ner_rule = NERRule()
ner_flair = NERFlair()

with open(PATH / shortcode / 'caption.txt', 'r') as f:
    r0 = f.read()

# Load NERRule
r1 = ner_rule.from_json(
    filepath=fullpath / 'ner_rule.json',
    as_frame=True
)
r2 = ner_flair.from_json(
    filepath=fullpath / 'ner_flair.json',
    as_frame=True
)


# Show
print(r0)
print(r1)
print(r2)

# Filter keep only locations
r2 = r2[r2.value.isin(['LOC'])]

# Show filtered
print("\n\nFlair filtered LOC")
print(r2)



# -----------------------------
# Filter entities
# -----------------------------
# Possible options:
#   1. Add country to location if 'flag' or 'text'.
#
# FLAIR:
#   1. Keep only GDP and LOC.
#   2. Keep only confidence > 0.80
#
#
# Combined:
#   1. String similarity Levenshtein
#   2. Index of one contained in the other
#   3. One is contained in another.

# Concatenate
r = pd.concat([r1, r2])

# Format location
if not 'location' in r:
    r['location'] = r.text
r.location = r.location.fillna(r.text)
r.location = r.location.str.lower()
r.location = r.location.apply(clean_text)

# Remove punctuation
# Remove weird symbols like "?

# If it is a very long sentence and there is no other
# element extracted (e.g. from flair) with a location
# in those indexes
r['len'] = r.location.str.len()

# Remove duplicates. In the concatenation, the first frame
# is the NERRule and the second one the FlairRule. Thus,
# duplications from second are removed.
r = r.drop_duplicates(subset=['location'])


def filter_by_distance(v, threshold=0.5):
    """Computes tht distance between all the entries and
       for those pairs with a distance >= threshold, it
       discards one of them."""
    import numpy as np
    matrix = compute_levenshtein_matrix(v)
    df = pd.DataFrame(data=matrix, index=v, columns=v)
    idx = np.argwhere(np.triu(matrix, 1)>threshold)
    return v[idx[:,1]]


def filter_by_contained():
    """Checks whether each of the entries is contained in
       any other entry and removes the one that is contained.
       (the shorter entry)"""
    pass

def filter_by_text_position():
    """Checks the position in the text (start, end) and
       removes those in which one is contained in the other.
    """
    pass

def filter_by_length():
    """If the string is too long it is very likely that it
       is not a location. We could also check for the long
       string whether a location (start, end) is contained
       within."""
    pass




idxs = filter_by_distance(r.location.values)
r = r[~r.location.isin(idxs)]

print("\n==> Rule")
print(r1)
print("\n==> Flair")
print(r2)
print("\n==> Final Result:")
print(r)


import sys
sys.exit()







# Define tagger
#tagger = DEFAULT_TAGGERS['spacy-trf']
tagger = DEFAULT_TAGGERS['rule']

# Define pattern
pattern = '%s/**/%s' % (PATH, tagger.FILENAME)
pattern = '%s/**/ner*.json' % (PATH)
# ChcpJTJItWy

# Conduct text formatting
for i, f in enumerate(glob.glob(pattern, recursive=True)):
    print("%s. Loading... %s" % (i, f))

    # -------------------------
    # Single
    # -------------------------
    # From json directly
    #r = tagger.from_json(f)

    # Include country name
    #r = prepare_geolocation_query(r)
    #r = select_geolocation_query(r)

    # -------------------------
    # Multiple
    # -------------------------

    continue

    # Converting to pandas dataframe



    # Load entities
    r = tagger.from_json(f, as_dataframe=True)

    if r is None:
        continue
    if r.empty:
        continue

    print(r)

    r = tagger.select_entities(r,
        entity_types=['GPE', 'LOC'])
    if 'groupdict' in r:
        r = r.drop(columns='groupdict')
    print(r)
    print("\n\n")


    # Filter those with location but no info

    # Adding context with country information
    # if only one country found by flag or text
    # if the country word does not appear in the query
    # include it at the end!








