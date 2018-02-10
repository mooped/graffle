from flask import Flask
import json

import template
import timestamp
import datas

app = Flask('graffle')

@app.route('/')
def index():
  first, last = datas.get_time_range()
  dates = timestamp.get_days_in_range(first, last)
  dates.reverse()
  for date in dates:
    date.update({
      "uri" : "/day/%d/%2d/%2d" % (date["year"], date["month"], date["day"])
    })
  nodes = [{"name" : node, "uri" : "/latest/%s" % node} for node in sorted(datas.get_nodes())]

  return template.render("templates/index.html", {
    "nodes" : nodes,
    "dates" : dates,
  })

@app.route('/latest/<node>')
def latest(node):
  data = json.dumps(datas.get_latest(node))
  return data

@app.route('/day/<year>/<month>/<day>')
def day(year, month, day):
  # 24 hour window
  start = int(timestamp.get_timestamp(int(year), int(month), int(day)))
  end = start + (24 * 60 * 60)

  # Get the data
  data = datas.get_range(start, end)
  return json.dumps(data)

if (__name__ == "__main__"):
  app.run(host="0.0.0.0", port=80, threaded=True)
