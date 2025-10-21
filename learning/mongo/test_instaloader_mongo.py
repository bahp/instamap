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

from nested_lookup import nested_lookup

def extract_post_details(p, keys):
    """"""
    d = p.__dict__
    details = {}
    for k in keys:
        details[k] = nested_lookup(k, d)
    return details

# Load
with open('post.obj', 'rb') as f:
    obj = pickle.load(f)

# Show
#print(obj)
#print(dir(obj))
#print(obj.__dict__)

print(obj.__dict__)
print(obj._asdict())

# Delete the key <_context> because it contains an
# InstaloaderContext object which is not json serializable.
#d = obj.__dict__
#d.pop('_context')
#print(json.dumps(d, indent=4))


#print(extract_post_details(obj, ['shortcode', 'text']))


# Database with posts
# Database with b_post
# Database with b_post_nlp
# Database with b_post_geo

# Load
with open('../../post_list.obj', 'rb') as f:
    obj = pickle.load(f)

#for p in obj:
#    print(extract_post_details(p, ['shortcode']))


# -------------------------------------
# Mongo
# -------------------------------------
# Libraries
import pymongo



def collection_exists(db, name):
    collist = db.list_collection_names()
    if name in collist:
        return True
    return False

def create_collection(db, name):
    if not collection_exists(db, name):
        database.create_collection(name)


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
pic = database.get_collection("posts")

# Count number of documents
N = pic.count_documents({})

# .. note: For some reason it is not able to ignore
#          when a key exists and raises and error.
#          Thus, we will use findAndUpdate instead.

# Insert the data into the collection
#pic.insert_many(posts_dict, ordered=True)

# Loop
for p in posts_dict[:N+5]:
    post_id = p['_id']

    r = pic.find_one({'_id': post_id})
    if r is None:
        print("It does not exist!")
        r = pic.insert_one(p)

    # It was there before, so we assume that it
    # has been queried again because we have now
    # downloaded the full data for the post
    pic.update_one({'_id': post_id}, {'$set': {'visited': True}})

    print(p)
    print("\n\n")
    print(r)
    #print(type(p))
    #print(p)
    #print(p['_id'])
    #pic.update_one({'_id': p['_id']}, p, upsert=True)

# .. note: How can we make it to add the record
#          if it does not exist using something
#          like writer result but in update many
#pic.update_many(filter={},
#    #update={'$inc': {'updated': True}},
#    update={'$set': posts_dict},  #'$mod'
#    upsert=True)

# Using findAndUpdate is a better option, if we download
# the list on a later stage, some information such as
# likes will be updated.
#for p in posts_dict:

"""
    pic.find_one_and_update(
        {'_id': p._id},
        {'$set': {"Branch": 'ECE'}},
                        return_document=ReturnDocument.AFTER)
"""


#print(pic.find_one())

# get the count of total data points
#print(pic.count())
#pic.find().count()
#print(pic.find())
#print(pic.find().count())
print("\n\n\n\n")
print(pic.count_documents({}))

# Delete collection
#database.posts_instaloader.drop()