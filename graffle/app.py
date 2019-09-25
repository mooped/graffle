from flask import Flask, request, Response, send_from_directory
import json

import template
import timestamp
import datas

app = Flask('graffle')

# Hardcoded params, labels, limits, and axes
params = [
  ("si7007", "temperature" , "Temperature (&#176;C)", True, 15.0, 35.0, 1),
  ("si7007", "humidity", "Humidity (%RH)", False, 0.0, 100.0, 2),
  ("ccs811", "co2_ppm", "Carbon Dioxide (Parts Per Million)", False, 400.0, 8192.0, 3),
  ("ccs811", "voc_ppb", "Volatile Organic Compounds (Parts Per Billion)", False, 0.0, 1187.0, 4),
  ("core", "internal_temperature", "CPU Temp (???)", False, 0.0, 255.0, 5),
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
    "autoplot" : dates[0]["plot_uri"] if len(dates) > 0 else "",
  })

@app.route('/js/<path:path>')
def send_js(path):
  return send_from_directory("js", path)

@app.route('/latest/<node>')
def latest_json(node):
  data = json.dumps(datas.get_latest(node))
  return Response(data, mimetype='application/json')

@app.route('/refresh_ids')
def refresh_ids():
  datas.refresh_ids()
  return Response(json.dumps({"status" : "ok"}), mimetype='application/json')

@app.route('/slack/temp', methods=['POST'])
def slack_temp():
  node = request.form['text']
  response = { "text" : "Oops! Something went wrong!" }
  try:
    data = datas.get_latest(node)
    response = {
      "response_type" : "in_channel",
      "text" : "The temperature at %s is %2.2f degrees Celcius. Humidity is %2.2f%% RH." % (node, data.get("si7007", {}).get("temp", -1), data.get("si7007", {}).get("humidity", -1)),
    }
  except:
    try:
      nodes = datas.get_nodes()
      response = {
        "response_type" : "in_channel",
        "text" : "Valid nodes:",
        "attachments" : [
          {
            "text" : ", ".join(nodes)
          }
        ]
      }
    except:
      pass
  return Response(json.dumps(response), mimetype='application/json')

@app.route('/day/<int:year>/<int:month>/<int:day>')
def day_json(year, month, day):
  # 24 hour window
  start = int(timestamp.get_timestamp(year, month, day))
  end = start + (24 * 60 * 60)

  # Get the data
  data = datas.get_range(start, end)
  return Response(json.dumps(data), mimetype='application/json')

# Format data for Flot
def format_plot(node, param, data):
  plot = {
    "label" : "%s %s" % (node, param[2]),
    "param" : param[0] + "-" + param[1],
    "data" : [
      [p["timestamp"] * 1000, p.get(param[0], {}).get(param[1], {})]
      for p in data
      if "node" in p
        and str(p["node"]) == str(node)
        and "timestamp" in p
        and param[0] in p
        and param[1] in p.get(param[0])
        and p.get(param[0]).get(param[1]) >= param[4]
        and p.get(param[0]).get(param[1]) <= param[5]
      ],
    "yaxis" : param[5]
  }
  return plot

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
      plots.append(format_plot(node, param, data))

  return Response(
    json.dumps({
      "pretty" : timestamp.get_pretty_day(year, month, day),
      "year" : year,
      "month" : month,
      "day" : day,
      "nodes" : nodes,
      "raw_params" : params,
      "raw_plots" : plots,
    }),
    mimetype='application/json'
  )

if (__name__ == "__main__"):
  app.run(host="0.0.0.0", port=80, threaded=True)
