# Libraries
import pymongo

def collection_exists(db, name):
    collist = db.list_collection_names()
    if name in collist:
        return True
    return False

def create_collection(db, name):
    if not collection_exists(db, name):
        db.create_collection(name)