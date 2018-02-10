from flask import Flask, request, Response, send_from_directory
import json

import template
import timestamp
import datas

app = Flask('graffle')

# Hardcoded params and labels
params = [
  ("temp" , "Temperature (&#176;C)", True),
  ("humidity", "Humidity (%RH)", True),
  ("co2_ppm", "Carbon Dioxide (Parts Per Million)", False),
  ("voc_ppb", "Volatile Organic Compounds (Parts Per Billion)", False),
  ("core_temp", "CPU Temp (???)", False),
]

@app.route('/')
def index():
  first, last = datas.get_time_range()
  dates = timestamp.get_days_in_range(first, last)
  dates.reverse()
  for date in dates:
    date.update({
      "uri" : "/day/%d/%02d/%02d" % (date["year"], date["month"], date["day"]),
      "plot_uri" : "/plot/day/%d/%02d/%02d" % (date["year"], date["month"], date["day"]),
    })
  nodes = [{"name" : node, "uri" : "/latest/%s" % node} for node in sorted(datas.get_nodes())]

  return template.render("templates/index.html", {
    "nodes" : nodes,
    "dates" : dates,
    "params" : json.dumps(params),
  })

@app.route('/js/<path:path>')
def send_js(path):
  return send_from_directory("js", path)

@app.route('/latest/<node>')
def latest_json(node):
  data = json.dumps(datas.get_latest(node))
  return Response(data, mimetype='application/json')

@app.route('/day/<int:year>/<int:month>/<int:day>')
def day_json(year, month, day):
  # 24 hour window
  start = int(timestamp.get_timestamp(year, month, day))
  end = start + (24 * 60 * 60)

  # Get the data
  data = datas.get_range(start, end)
  return Response(json.dumps(data), mimetype='application/json')

# Format data for Flot
def format_plot(node, param, label, data):
  return {
    "label" : "%s %s" % (node, label),
    "param" : param,
    "data" : [
      [p["timestamp"] * 1000, p["data"][param]]
      for p in data
      if "node" in p and
        str(p["node"]) == str(node) and
        "timestamp" in p and
        "data" in p and
         param in p["data"]
      ]
  }

@app.route('/plot/day/<int:year>/<int:month>/<int:day>')
def day_plot(year, month, day):
  # 24 hour window
  start = int(timestamp.get_timestamp(year, month, day))
  end = start + (24 * 60 * 60)

  # Get the data
  data = datas.get_range(start, end)

  # Get the list of nodes
  nodes = datas.get_nodes()

  # Format the appropriate plots for Flot
  plots = []
  for node in nodes:
    for param in params:
      plots.append(format_plot(node, param[0], param[1], data))

  return Response(
    json.dumps({
      "pretty" : timestamp.get_pretty_day(year, month, day),
      "year" : year,
      "month" : month,
      "day" : day,
      "nodes" : nodes,
      "params" : json.dumps(params),
      "raw_plots" : plots,
    }),
    mimetype='application/json'
  )

@app.route('/graph/day/<int:year>/<int:month>/<int:day>')
def day_graph(year, month, day):
  # 24 hour window
  start = int(timestamp.get_timestamp(year, month, day))
  end = start + (24 * 60 * 60)

  # Get the data
  data = datas.get_range(start, end)

  # Get the list of nodes
  nodes = datas.get_nodes()

  # Format the appropriate plots for Flot
  params = ["temp", "humidity", "co2_ppm", "voc_ppb", "core_temp"]
  plots = []
  for node in nodes:
    for param in params:
      plots.append(format_plot(node, param, param, data))

  return template.render("templates/graph.html", {
    "pretty" : timestamp.get_pretty_day(year, month, day),
    "year" : year,
    "month" : month,
    "day" : day,
    "nodes" : nodes,
    "raw_plots" : plots,
    "plots" : json.dumps(plots),
  })

if (__name__ == "__main__"):
  app.run(host="0.0.0.0", port=80, threaded=True)
