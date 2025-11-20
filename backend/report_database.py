# the report that loads after the image is uploaded
# pulling the report from the database, need to create the database 

import os 
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from dotenv import load_dotenv
from datetime import datetime
from bson.objectid import ObjectId 

load_dotenv()

uri = os.getenv("MONGODB_URI")
db_name = os.getenv("MONGODB_DB_NAME")

print(f"URI: {uri}")
print(f"DB Name: {db_name}")

client = None
db = None
predictions_collection = None

if not uri or not db_name:
    print("MONGODB_URI or MONGODB_DB_NAME not set; database disabled.")
else:
    try:
        client = MongoClient(uri)
        db = client[db_name]
        predictions_collection = db["predictions"]

        # Send a ping to confirm a successful connection
        try:
            client.admin.command('ping')
            print("Pinged your deployment. You successfully connected to MongoDB!")
        except Exception as e:
            print(f"MongoDB ping failed: {e}")
    except Exception as e:
        print(f"Failed to connect to MongoDB: {e}")
        client = None
        db = None
        predictions_collection = None

# save report
def save_report(report):
    # Insert a report to the database and return its ID.
    if predictions_collection is None:
        print("Database not configured - cannot save report")
        return None

    try:
        result = predictions_collection.insert_one(report)
        return str(result.inserted_id)
    except Exception as e:
        print(f"Failed to save report to database: {e}")
        return None

# get a specific report
def get_report(report_id):
    if predictions_collection is None:
        return None

    try:
        obj_id = ObjectId(report_id)
    except:
        return None

    doc = predictions_collection.find_one({"_id": obj_id})
    if not doc:
        return None

    # convert ObjectId to string
    doc["id"] = str(doc["_id"])
    del doc["_id"]
    return doc

# list reports
def list_reports(limit=20):
    if predictions_collection is None:
        return []

    cursor = predictions_collection.find().sort("_id", -1).limit(limit)

    results = []
    for doc in cursor:
        # convert ObjectId to string and remove internal _id
        doc["id"] = str(doc["_id"])
        del doc["_id"]
        results.append(doc)

    return results 
        
    