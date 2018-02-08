from datetime import datetime

def to_timestamp(dt):
  return (dt - datetime(1970, 1, 1)).total_seconds()

def get_timestamp(year, month, day):
  return to_timestamp(datetime(year, month, day))

