import time
from datetime import datetime

def uts2dts(uts:float)->datetime:
  """Unix timestamp to datetime"""
  dts = datetime.fromtimestamp(uts)
  return dts

def dts2uts(dts:datetime)->float:
  """datetime to Unix timestamp"""
  secs = int(dts.timestamp())
  frac = dts.microsecond / 1_000_000
  return secs+frac


if __name__ == '__main__':
  # 1. Unix timestamp to datetime
  # Get the current time in Unix timestamp
  current_time = time.time()
  print(f'Current time in Unix timestamp: {current_time}')

  # Convert the Unix timestamp into a datetime object
  dt = datetime.fromtimestamp(current_time)

  print(f'{dt.weekday()+1} {dt.month} {dt.day} {dt.hour}:{dt.minute}:{dt.second}.{dt.microsecond/1_000_000} {dt.year}')
  print(dt.strftime("%a %m %d %H:%M:%S.%f %Y"))

  # 2. Datetime to Unix timestamp
  # Get the current time as datetime
  now = datetime.now()

  # convert the datetime into Unix timestamp
  uts = dts2uts(now)
  print(uts)

  # !!!NOTE: POSIX timestamp
  print(now.timestamp())

