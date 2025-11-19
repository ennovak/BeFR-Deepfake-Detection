# the report that loads after the image is uploaded
# pulling the report from the database, need to create the database 

import os 
from pymongo import MongoClient
from pymongo.server_api import ServerApi
from dotenv import load_dotenv
from datetime import datetime
from bson.objectid import ObjectId 

load_dotenv()

uri = os.getenv("uri")
DB_NAME = os.getenv("DB_NAME")

db = None
predictions_collection = None
client = None

if uri and DB_NAME:
    client = MongoClient(uri, server_api=ServerApi('1'))
    db = client[DB_NAME]
    predictions_collection = db["predictions"]
    
    # Send a ping to confirm a successful connection
    try:
        client.admin.command('ping')
        print("Pinged your deployment. You successfully connected to MongoDB!")
    except Exception as e:
        print(f"MongoDB connection warning: {e}")
else:
    print("Warning: MongoDB not configured. Database features disabled.")

# save report
def save_report(report):
	#Insert a report to the database and returns its ID.
	result = predictions_collection.insert_one(report)
	return str(result.inserted_id)

# get a specific report
def get_report(report_id):
    try:
        obj_id = ObjectId(report_id)
        doc = predictions_collection.find_one({"_id": obj_id})
        if not doc:
            return None
        # convert ObjectId to string
        doc["id"] = str(doc["_id"])
        del doc["_id"]
        return doc          
    except:
        return None
    
# list reports
def list_reports(limit=20):
    cursor = predictions_collection.find().sort("_id", -1).limit(limit)

    results = []
    for doc in cursor:
        doc["id"] = str(doc["id"])
        del doc["_id"]
        results.append(doc)
    
    return results 
        
    