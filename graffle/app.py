from flask import Flask
import json

import timestamp
import datas

app = Flask('graffle')

@app.route('/')
def index():
  return "Welcome to the stone of graffle"

@app.route('/latest/<node>')
def latest(node):
  data = datas.get_latest(node)
  print data
  return data

@app.route('/day/<year>/<month>/<day>')
def day(year, month, day):
  # 24 hour window
  start = int(timestamp.get_timestamp(int(year), int(month), int(day)))
  end = start + (24 * 60 * 60)

  # Get the data
  data = datas.get_range(start, end)
  print data
  return data

if (__name__ == "__main__"):
  app.run(host="0.0.0.0", port=80)

