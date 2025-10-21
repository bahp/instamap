# Libraries
import json
import time
import random
import pickle
import instaloader

from pathlib import Path
from nested_lookup import nested_lookup

class Post:
    """This class...."""

    def exists(self):
        pass

    def get_caption(self):
        pass

    def get_shortcode(self):
        pass

    def extract_ner_flair(self):
        pass

    def extract_ner_spacey(self):
        pass

    def extract_ner_bert(self):
        pass

    def extract_ner_bard(self):
        pass

    def query_geolocation(self):
        pass


def get_caption(p):
    """Get the caption from the dictionary.

    .. note: The structure might be more complex. If missing information
             go back to the json and loop the various edges, getting the
             node text for each of them. The structure looks as follows:

            "edge_media_to_caption": {
                "edges": [
                    {
                        "node": {
                            "text": The caption
                        }
                    }
                ]
             }

    :param p:
    :return:
    """
    try:
        text = nested_lookup('edge_media_to_caption', p)[0]
        text = text['edges'][0]
        text = text['node']
        text = text['text']
        return text
    except Exception as e:
        return None

def get_shortcode(p):
    """Get the shortcode from the dictionary."""
    try:
        return nested_lookup('shortcode', p)[0]
    except Exception as e:
        return None


def create_folder_structure(path):
    """Creates the folder structure.

    posts
      _captions.json
      _posts.json
      |- shortcode_1
        |- caption.txt
        |- post.json
      |- shortcode_2
        |- caption.txt
        |- post.json

    .. note: Instaloader has a function to save to file directly
             if required. We are not using it to have a bit more
             of flexibility.

            # Add to cumulative
            if isinstance(obj, instaloader.structures.Post):
                instaloader.save_structure_to_file(obj, f)

    :param path:
    :return:
    """
    path_posts = Path(path) / 'posts'

    # Check there is post_list obj.

    # Load posts preview downloaded.
    with open(path / 'post_list.obj', 'rb') as f:
        obj_list = pickle.load(f)

    # Create path where posts will be saved
    path_posts.mkdir(parents=True, exist_ok=True)


    # -------------------------------
    # Option I: Save big file
    # -------------------------------
    # Create posts list
    #posts_dict = [o._asdict() for o in obj_list]
    posts_dict = [instaloader.get_json_structure(o) for o in obj_list]

    # Create a json file which has as keys the shortcodes
    # and as values the caption. This is in case we want
    # to load everything in one, instead of loading the
    # .txt directly
    captions = {
        get_shortcode(p): get_caption(p) for p in posts_dict
    }

    posts = {
        get_shortcode(p): p for p in posts_dict
    }

    # Save files
    with open(path / "_captions.json", "w") as f:
        json.dump(captions, f)

    with open(path / "_posts.json", "w") as f:
        json.dump(posts, f)


    # --------------------------------------
    # Option II: Save each post individually
    # --------------------------------------
    # Save captions to .txt file
    for k, v in captions.items():
        # Skip iteration
        if v is None:
            continue

        # Save caption to .txt file
        (path_posts / k).mkdir(parents=True, exist_ok=True)
        with open(path_posts / k / 'caption.txt', 'w') as f:
            f.write(v)

    # Save posts to json file.
    for k, v in posts.items():
        (path_posts / k).mkdir(parents=True, exist_ok=True)
        with open(path_posts / k / 'post.json', 'w') as f:
            json.dump(v, f, indent=4)




def extract_ner(path, method='bard', text_processing=False,
                force_reset=False):
    """Extracts entities from the caption.


    methods
    'flair'
    'bard'
    'spacy',
    'spacy-en_core_web_sm'
    'spacy-en_core_web_md'
    'spacy-en_core_web_lg'
    'spacy-en_core_web_trf'



    :param path:
    :param method:
    :return:
    """
    # Libraries
    from pathlib import Path
    from src.utils import text
    from src.utils import load
    from src.utils import ner
    from src.settings import DEFAULT_TAGGERS

    # Create posts paths
    path_posts = Path(path) / 'posts'

    # Load all captions
    with open(Path(path) / '_captions.json', "r") as f:
        captions = json.load(f)

    # Select the method
    tagger = DEFAULT_TAGGERS[method]

    # Number of items
    N = len(captions.keys())

    # Conduct text formatting
    for i, (k, v) in enumerate(captions.items()):
        print("%3d/%3d. Loading ... %s | " % (i, N, k), end="")

        # Skip iteration (no caption)
        if v is None:
            print("<%s>, there is no caption." % v)
            continue

        # Skip the iteration (NER already exists)
        if not force_reset and tagger.exists(path_posts / k):
            print("<%s> file already exists!" % tagger.FILENAME)
            continue

        # Edited text to support the algorithm.
        edited = tagger.format_text(txt=v, chain=None)
        # Identify the entities in the text.
        result = tagger.predict(edited)
        # Save into file
        tagger.save(result, path_posts / k)

        # There is some error
        if isinstance(tagger, ner.NERBard):
            if 'status_code' in result:
                if result['status_code'] != 200:
                    print("Error querying bard!")
                    break
            if result['content'].startswith('Response Error'):
                print(result['content'])
                break

            # Sleep
            time.sleep(random.randint(4, 8))

        # Log
        print("NER extraction completed!")





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

    print(matches)
    print(matches['entities'])

    # Find whether there is country information (text).
    countries = list(filter(lambda d: d.get('attr', '') == 'text', matches))
    if countries:
        return countries[0]['text']

    # Find whether there is country information (flag).
    countries = list(filter(lambda d: d.get('attr', '') == 'flag', matches))
    if countries:
        flag = countries[0]['text']
        return pycountry.countries.get(flag=flag).name

    return None

def query_add_country(matches):
    """"""
    from src.utils.ner import clean_text
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
            e['query'] = e['text'].lower()

    # In queries keep only letters and maybe punctuation?

    return matches



def create_entities_db(path, method):
    """"""
    # Libraries
    import glob
    import pandas as pd
    from src.utils.ner import clean_text
    from src.utils.ner import NERBard
    from src.utils.ner import NERFlair
    from src.utils.ner import NERRule
    from src.utils.tools import get_geolocations
    from src.settings import DEFAULT_TAGGERS

    # Get tagger
    tagger = DEFAULT_TAGGERS[method]

    # Define path to search
    path_posts = Path(path) / 'posts'
    search_expression = '{path}/**/{filename}'.format(
        path=path_posts, filename=tagger.FILENAME
    )

    ner_rule = NERRule()
    ner_flair = NERFlair()

    # Create DataFrame
    entities = pd.DataFrame()

    subdirs = [x for x in path_posts.iterdir() if x.is_dir()]
    searchf = glob.glob(search_expression, recursive=False)

    # Load all found entities
    for f in subdirs:

        # Create file names
        file1 = f / 'ner_rule.json'
        file2 = f / 'ner_flair.json'

        # Create empty frames
        r1 = pd.DataFrame()
        r2 = pd.DataFrame()

        # Retrieve information
        if file1.exists():
            r1 = ner_rule.from_json(file1, as_frame=True)
        if file2.exists():
            r2 = ner_flair.from_json(file2, as_frame=True)

        # Concatenate
        df = pd.concat([r1, r2])

        """
        # Load DataFrame
        r = tagger.from_json(f)
        # Include country name
        r = prepare_geolocation_query(r)
        #r = select_geolocation_query(r)

        df = pd.DataFrame(r)
        if df is None:
            continue
        if df.empty:
            continue
        """

        # Add additional information
        #df['shortcode'] = str(Path(f).parent.stem)
        df['shortcode'] = str(Path(f).stem)
        df['tagger'] = method

        # Add to DataFrame
        entities = pd.concat([entities, df])


    # .. note: Instead of filtering here, we will keep all the
    #          the entities in case they are useful in the
    #          future. The filter will be done right before
    #          querying the geographical locations API.
    #
    # Select entities to avoid redundancy.
    #entities = tagger.select_entities(entities,
    #    entity_types=['GPE', 'LOC'])
    # Just doing the rename
    #entities = tagger.select_entities(entities)
    #entities = entities.head(100)

    # Save
    entities.to_json(path / ('_entities_%s.json' % method),
        orient='records', indent=4)
    entities.to_json(path / '_entities.json',
                     orient='records', indent=4)



def create_geolocations_db(path, method):
    """Compute all the geolocations.


    Parameters
    ----------

    Returns
    -------
    """
    # Libraries
    import glob
    import pandas as pd
    from tqdm import tqdm
    from src.utils.ner import clean_text
    from src.utils.ner import NERBard
    from src.utils.ner import NERFlair
    from src.utils.tools import get_geolocations
    from src.settings import DEFAULT_TAGGERS

    # Activate
    tqdm.pandas()

    # Create tagger
    tagger = DEFAULT_TAGGERS[method]

    # Define paths
    #path_geo = Path(path) / ('_geolocations_%s.json' % method)
    #path_entities = Path(path) / ('_entities_%s.json' % method)

    path_geo = Path(path) / '_geolocations.json'
    path_entities = Path(path) / '_entities.json'

    # Load entities
    entities = pd.read_json(path_entities, orient='records')

    # Select entities to avoid redundancy.
    #entities = tagger.select_entities(entities,
    #    entity_types=['GPE', 'LOC'])

    # Filter locations
    if not entities.empty:
        if 'value' in entities:
            codes = [None, 'GPE', 'LOC']
            entities = entities[entities.value.isin(codes)]

    # Format location
    if not 'location' in entities:
        entities['location'] = entities.text
    entities.location = entities.location.fillna(entities.text)
    entities.location = entities.location.str.lower()
    entities.location = entities.location.apply(clean_text)

    # Remove duplicates. In the concatenation, the first frame
    # is the NERRule and the second one the FlairRule. Thus,
    # duplications from second are removed.
    entities = entities.drop_duplicates(subset=['location'])

    # Filter by selecting only those bounding boxes
    # that do not contain each other if possible. Otherwise
    # the smaller although might be containing.


    if entities.empty:
        print("The entities are empty!")
        return

    # Load or create geographical locations database
    DB_GEO = pd.DataFrame()
    if path_geo.exists():
        DB_GEO = pd.read_json(path_geo, orient='index')

    entities['query'] = entities.location

    # Keep only those that do not already exist in DB_GEO.
    # Note that we allow to have the same entry if the
    # query has been done with bard?
    if not DB_GEO.empty:
        entities = entities[~entities['query'].isin(DB_GEO['query'])]


    # -------------------------
    # Query locations
    # -------------------------
    # Query vector
    q = entities['query']
    if 'full_address' in entities: # When? Bard?!!!!!
        q = entities.full_address

    # Query the locations
    r = get_geolocations(q)

    # Create the DataFrame
    db_new = pd.json_normalize(
        r.apply(lambda x: x.raw if x else {})
    )

    PARAM = 'query'

    # Include the entity (text) and format
    db_new[PARAM] = entities[PARAM].values
    #db_new['tagger'] = method
    db_new = db_new.set_index('query', drop=False)

    # Concatenate
    DB_GEO = pd.concat([DB_GEO, db_new])
    DB_GEO = DB_GEO.set_index(PARAM, drop=False)

    # Save overall file
    DB_GEO.to_json(path_geo, orient='index', indent=4)




def create_summary(path, method):
    """"""
    import glob
    import pandas as pd
    from src.utils.ner import clean_text
    from src.settings import DEFAULT_TAGGERS

    # Get the tagger
    tagger = DEFAULT_TAGGERS[method]

    COL = 'location'

    # Define paths
    path_posts = Path(path) / 'posts'
    path_db_post = Path(path) / '_posts.json'
    #path_db_ent = Path(path) / ('_entities_%s.json' % method)
    #path_db_geo = Path(path) / ('_geolocations_%s.json' % method)
    path_db_ent = Path(path) / '_entities.json'
    path_db_geo = Path(path) / '_geolocations.json'


    # Load databases
    DB_GEO = pd.read_json(path_db_geo, orient='index')
    DB_ENT = pd.read_json(path_db_ent, orient='records')

    DB_GEO = DB_GEO.add_prefix('geo_')
    DB_ENT = DB_ENT.add_prefix('ent_')

    print(DB_GEO.shape)
    print(DB_ENT.shape)
    print(DB_GEO.columns)
    print(DB_ENT.columns)

    DB_GEO['query'] = DB_GEO.geo_query.str.lower()
    DB_ENT['query'] = DB_ENT.ent_location.str.lower()

    DB_GEO = DB_GEO[~DB_GEO['query'].isna()]
    DB_ENT = DB_ENT[~DB_ENT['query'].isna()]

    DB_GEO['query'] = DB_GEO['query'].apply(clean_text)
    DB_ENT['query'] = DB_ENT['query'].apply(clean_text)


    # Merge them
    summary = DB_ENT.merge(DB_GEO,
         how='left', left_on='query', right_on='query')

    print(summary.shape)
    print(summary)
    print(summary.columns)

    # -------------------
    # Cleaning (optional)
    # -------------------
    # Possible ways to clean and/or filter.
    # 1. sort by confidence and place_rank
    # 2. keep top N based on these order
    # 3. The mode
    # 4. Compute the mean? careful

    # Remove those without coordinates
    summary = summary.dropna(how='any',
        subset=['geo_lat', 'geo_lon', 'ent_shortcode'])

    # Remove duplicates
    summary = summary.drop_duplicates(
        subset=['ent_shortcode', 'query']
    )

    # ----------------------
    # Show some useful info
    # ----------------------
    #print(summary)
    #print(summary.columns)
    #print(summary['class'].unique())
    #print(summary['type_y'].unique())



    summary.to_json(path / '_summary.json',
        orient='records', indent=4)
    summary.to_csv(path / '_summary.csv')



    # Create summary
    #summary = entries.merge(DB_GEO,
    #    how='left', left_on='text', right_on='text')


    """
    # Results
    results = pd.DataFrame()
    results = []

    # Loop
    entries = pd.DataFrame()

    pattern_fair = '**/fair_ner.json'
    pattern_bard = '**/bard_ner.json'

    # Loop through all the computed NER.
    for f in glob.glob(search_expression, recursive=False):
        print(f)

        # Load file
        with open(f, 'r') as file:
            response = json.load(file)

        # Extract json
        #data_json = response_extract_json(response['content'])

        #if data_json is None:
         #   continue

        #print(data_json)
        #if 'locations' in data_json:
        #    data_json = data_json['locations']

        # Get entities
        df = tagger.from_json(filepath=f, as_dataframe=True)
        #df = pd.DataFrame.from_records(data_json)

        print(df)

        # Basic checks
        if df is None:
            continue
        if df.empty:
            continue

        # Add data
        df['shortcode'] = str(Path(f).parent.stem)

        # Concatenate
        entries = pd.concat([entries, df], ignore_index=True)

    print(entries)
    print(entries.columns)

    if isinstance(tagger, NERBard):
        entries = entries.rename(columns={
            'name': 'text',

        })


    #print(entries.type.value_counts().head(20))
    


    entries.to_json(path / '_summary.json',
                    orient='records', indent=4)
    entries.to_csv(path / '_summary.csv')

    # Format entries
    entries['text'] = entries.text.str.lower()

    # Merge with geographic locations
    DB_GEO = pd.read_json(path_db_geo, orient='index')
    print(DB_GEO)

    # Create summary
    summary = entries.merge(DB_GEO,
        how='left', left_on='text', right_on='text')

    print(summary.columns)

    # Show unique values for information
    #for c in ['value', 'class', 'addresstype']:
    #    print(c, summary[c].unique())

    aux = summary[['place_rank', 'addresstype']].drop_duplicates()

    print(aux)

    # -------------------
    # Cleaning (optional)
    # -------------------
    # .. note: Organizations might be relevant too?
    # .. note: Other NER algorithms used different labels.



    # Keep only locations
    #summary = summary[summary.value.isin(['LOC'])]
    # Keep only those that have certain information
    #summary = summary.dropna(how='any',
    #                         subset=['lat', 'lon', 'shortcode'])
    # Remove duplicates
    summary = summary.drop_duplicates(
        subset=['shortcode', 'text']
    )

    # Possible ways to filter.
    # 1. sort by confidence and place_rank
    # 2. keep top N based on these order
    # 3. The mode
    # 4. Compute the mean? careful

    # print(summary)
    # summary = summary.groupby(by='shortcode')
    # print(summary)

    print(summary['class'].unique())
    print(summary['type'].unique())

    # Save
    summary.to_json(path / '_summary.json', orient='records', indent=4)
    summary.to_csv(path / '_summary.csv')
    """