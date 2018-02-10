from datetime import datetime

def to_timestamp(dt):
  return (dt - datetime(1970, 1, 1)).total_seconds()

def get_timestamp(year, month, day):
  return int(to_timestamp(datetime(year, month, day)))

def get_start_of_day(timestamp):
  dt = datetime.fromtimestamp(timestamp)
  return get_timestamp(dt.year, dt.month, dt.day)

def get_days_in_range(start, end):
  # Round start time down and end time up to the nearest day
  start = get_start_of_day(start)
  end = get_start_of_day(end) + 24 * 60 * 60

  # Iterate over every day in the range
  days = []
  for timestamp in range(start, end, 24 * 60 * 60):
    dt = datetime.fromtimestamp(timestamp)
    days.append({
      "year" : dt.year,
      "month" : dt.month,
      "day" : dt.day,
      "pretty" : dt.strftime("%a %B %d %Y")
    })

  return days
