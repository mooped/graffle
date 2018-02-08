from bson import json_util
import pymongo
import time

def get_latest(node):
  # Connect with read only account
  #client = pymongo.MongoClient('mongodb://climate_reader:climate_reader@ds115198.mlab.com:15198/climate', ssl=True)
  client = pymongo.MongoClient('ds115198.mlab.com', port=15198, username='climate_reader', password='climate_reader', authSource='climate')
  db = client.climate

  return json_util.dumps(db.v0_1.find({"node" : node}).sort("timestamp", pymongo.DESCENDING)[0])
  
def get_range(start, end):
  # Connect with read only account
  #client = pymongo.MongoClient('mongodb://climate_reader:climate_reader@ds115198.mlab.com:15198/climate', ssl=True)
  client = pymongo.MongoClient('ds115198.mlab.com', port=15198, username='climate_reader', password='climate_reader', authSource='climate')
  db = client.climate

  # Grab the sweet data
  cursor = db.v0_1.find({
    "$and" : [
      {"timestamp" : { "$gt" : start } },
      {"timestamp" : { "$lt" : end } },
    ]
  })

  return json_util.dumps([item for item in cursor])

