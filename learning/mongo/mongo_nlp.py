"""
"""

# Libraries
import re
import json
import pymongo
import pandas as pd

from src.utils import mongo
from flair.data import Sentence
from flair.nn import Classifier

# ----------------------------------------
# Mongo
# ----------------------------------------
def fair_nlp_entities_df(r):
    """"""
    aux = pd.DataFrame()
    entities = r['entities']
    for e in entities:
        lbl = pd.DataFrame(e['labels'])
        lbl['text'] = e['text']
        aux = pd.concat([aux, lbl])
    if not aux.empty:
        aux = aux.sort_values(by='confidence', ascending=False)
    aux = aux.reset_index(drop=True)
    return aux


def to_mongo_entities_df():
    """"""
    pass

def to_mongo(p, r):

    # Get top entity
    top = {}
    df = fair_nlp_entities_df(r)
    if not df.empty:
        df = df[df.value.isin(['LOC'])]
    if not df.empty:
        top = df.iloc[0].to_dict()

    # Return
    return {
        '_id': p['_id'],
        'bitacora': {
            'top_entity': top,
        },
        'model': {
            'library': 'flair',
            'task': 'ner',
            'desription': None
        },
        'results': r,
    }



def post_exists(p, collection):
    """"""
    return collection.find_one({'_id': p['_id']}) is not None

def post_extract_text(post):
    """"""
    # Extract text
    try:
        text = post['edge_media_to_caption']
        text = text['edges'][0] # check edges exis. # check array has elemtns
        text = text['node']['text']
        return text
    except Exception as e:
        print(post)
        print("INSIDE THE ERROR")
        # Return
        return 'empty'

def post_preprocess_text(text):
    """"""
    # Format text
    #text = text.strip()
    text = text.replace("#", '')
    text = text.replace(".", ". ")
    text = text.replace(",", ", ")
    # Return
    return text

def compute_post_ner(post, tagger):
    """

    .. note: For now, we are imputing the whole caption
             into the NER model. However, it might be better
             to split it in sentences nd do them independently.

             # Create sentences
             sentences = text.split("\n")
             # Remove empty
             sentences = list(filter(None, sentences))
             # Ensure it is an array
             if isinstance(sentences, str):
                sentences = [text]

    :param post:
    :param tagger:
    :return:
    """
    # Get text
    text = post_extract_text(post)
    text = post_preprocess_text(text)

    # Find entities
    sentence = Sentence(text)
    tagger.predict(sentence)

    # Convert to dictionary
    return sentence.to_dict(tag_type='ner')


# -----------------------------------------------------
# Main
# -----------------------------------------------------
# Create client
client = pymongo.MongoClient('mongodb://localhost:27017')

# Create database
database = client['bitacora_insta_db']

# Show
print("\nCollections:")
print(database.list_collection_names())

# Get collection weekly_demand
coll_posts = database.get_collection("posts")
coll_nlp = database.get_collection("b_post_nlp")

# Get post
post = coll_posts.find({})

# Create NER classifier
tagger = Classifier.load('ner')

#database.b_post_nlp.drop()
#print("Delete collection")

print("Total posts: %s" % coll_posts.count_documents({}))
print("Total NLP entries: %s" % coll_nlp.count_documents({}))

# Create results
results = []


# Loop
for p in post:
    # Check if post already exists
    if post_exists(p, coll_nlp):
        continue

    # Logging
    print("Extracting entities from... %s" % p['_id'])
    # Compute ner
    r = compute_post_ner(p, tagger)
    # Append results
    #results.append(to_mongo(p, r))
    # Insert
    r = coll_nlp.insert_one(to_mongo(p, r))
    #print(r)


#if results:
#    # Insert in batch.
#    #coll_nlp.insert_many(results, ordered=True)

# Delete
#database.b_post_nlp.drop()

"""
# It was there before, so we assume that it
# has been queried again because we have now
# downloaded the full data for the post
#pic.update_one({'_id': post_id}, {'$set': {'visited': True}})

print(json.dumps(results, indent=4))
for r in results:
    for e in r['entities']:
        print(e['text'], e['labels'][0])
"""