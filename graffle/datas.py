from bson import json_util
import json
import pymongo
import time
import timestamp

namemap = {}
macmap = {}

def to_json(data):
  return json.loads(json_util.dumps(data))

def connect():
  # Connect with read only account
  client = pymongo.MongoClient('mongodb://climate_reader:climate_reader@ds115198.mlab.com:15198/climate')
  return client.climate

def refresh_ids():
  for mapping in client.v0_3_idmapping.find():
    try:
      name = mapping["name"]
      mac = mapping["mac"]
      macmap[mac] = name
      namemap[name] = mac
    except:
        pass

def get_nodes():
  return to_json(client.v0_3_idmapping.distinct("name", {}, {}))

def get_time_range():
  first = client.v0_3.find().sort("timestamp", pymongo.ASCENDING)[0]
  last = client.v0_3.find().sort("timestamp", pymongo.DESCENDING)[0]
  return first.get("timestamp", 0), last.get("timestamp", int(time.time()))

def translate(record):
  record["data"] = {

  }

def get_latest(node):
  mac = namemap.get(node)
  data = to_json(client.v0_3.find({"sensor_mac" : mac}).sort("timestamp", pymongo.DESCENDING)[0])
  data["node"] = node
  return data
  
def get_range(start, end):
  # Grab the sweet data
  cursor = client.v0_3.find({
    "$and" : [
      {"timestamp" : { "$gt" : start } },
      {"timestamp" : { "$lt" : end } },
    ]
  })

  # Convert the timestamps to trick Flot into displaying correct times
  data = []
  for item in cursor:
    item["node"] = macmap.get(item["sensor_mac"])
    item["timestamp"] = timestamp.localise(item["timestamp"])
    data.append(item)

  return to_json(data)

client = connect()

refresh_ids()
