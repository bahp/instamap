"""

MongoDB Community: https://www.mongodb.com/docs/manual/tutorial/install-mongodb-on-os-x/
https://www.analyticsvidhya.com/blog/2020/08/query-a-mongodb-database-using-pymongo/
https://armstar.medium.com/mongodb-with-python-on-mac-for-absolute-beginners-d9f9d791d03c

o run MongoDB (i.e. the mongod process) manually as a background process, run:

For macOS running Intel processors:

    mongod --config /usr/local/etc/mongod.conf --fork

For macOS running on
Apple Silicon processors:

    mongod --config /opt/homebrew/etc/mongod.conf --fork

brew services start mongodb-community

"""

# Libraries
import json
import pickle
import pymongo
import pandas as pd

from nested_lookup import nested_lookup


# ---------------------------------------
# Mongo
# ---------------------------------------

def extract_post_details(p, keys):
    """"""
    d = p.__dict__
    details = {}
    for k in keys:
        details[k] = nested_lookup(k, d)
    return details


# Load
with open('../../post_list.obj', 'rb') as f:
    obj = pickle.load(f)

#for p in obj:
#    print(extract_post_details(p, ['shortcode']))


# -------------------------------------
# Main
# -------------------------------------
def to_mongo(p):
    d = p.asdict()
    d['_id'] = nested_lookup('shortcode', d)[0]
    d['source'] = 'instaloader'
    return d

def collection_exists(db, name):
    collist = db.list_collection_names()
    if name in collist:
        return True
    return False

def create_collection(db, name):
    if not collection_exists(db, name):
        database.create_collection(name)

def post_exists(p, collection):
    """"""
    return collection.find_one({'_id': p['_id']}) is not None

# Create client
client = pymongo.MongoClient('mongodb://localhost:27017')

# Create database
database = client['bitacora_insta_db']

# Create collections
create_collection(database, 'posts')
create_collection(database, 'b_post')
create_collection(database, 'b_post_nlp')
create_collection(database, 'b_post_geo')

# Show
print("\nCollections:")
print(database.list_collection_names())

# ---------
# Insert
# ---------
# Load list of posts preview downloaded
with open('../../post_list.obj', 'rb') as f:
    obj_list = pickle.load(f)

# Convert to list of dictionaries
posts_dict = [o._asdict() for o in obj_list]
for p in posts_dict:
    p['_id'] = nested_lookup('shortcode', p)[0]
    p['source'] = 'instaloader'

# Get collection weekly_demand
coll_posts = database.get_collection("posts")

# Count number of documents
N = coll_posts.count_documents({})

# Show
print("Total posts: %s" % N)

# .. note: For some reason it is not able to ignore
#          when a key exists and raises and error.
#          Thus, we will use findAndUpdate instead.

# Insert the data into the collection
#pic.insert_many(posts_dict, ordered=True)

# Loop
for p in posts_dict: #[:N+5]:
    # Check if post already exists
    if post_exists(p, coll_posts):
        continue

        # It was there before, so we assume that it
        # has been queried again because we have now
        # downloaded the full data for the post
        coll_posts.update_one(
            {'_id': p['_id']},
            {'$set': {'visited': True}}
        )

    # Logging
    print("Saving post... %s" % p['_id'])

    # Save
    r = coll_posts.insert_one(p)



# Get number of documents
N = coll_posts.count_documents({})

# Show
print("Total posts: %s" % N)