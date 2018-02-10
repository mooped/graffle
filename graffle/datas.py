from bson import json_util
import json
import pymongo
import time

def to_json(data):
  return json.loads(json_util.dumps(data))

def connect():
  # Connect with read only account
  client = pymongo.MongoClient('mongodb://climate_reader:climate_reader@ds115198.mlab.com:15198/climate')
  return client.climate

client = connect()

def get_nodes():
  return to_json(client.v0_1.distinct("node", {}, {}))

def get_time_range():
  first = client.v0_1.find().sort("timestamp", pymongo.ASCENDING)[0]
  last = client.v0_1.find().sort("timestamp", pymongo.DESCENDING)[0]
  return first.get("timestamp", 0), last.get("timestamp", int(time.time()))

def get_latest(node):
  return to_json(client.v0_1.find({"node" : node}).sort("timestamp", pymongo.DESCENDING)[0])
  
def get_range(start, end):
  # Grab the sweet data
  cursor = client.v0_1.find({
    "$and" : [
      {"timestamp" : { "$gt" : start } },
      {"timestamp" : { "$lt" : end } },
    ]
  })

  return to_json([item for item in cursor])
