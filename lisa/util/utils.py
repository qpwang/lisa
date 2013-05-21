import time
import datetime

def datetime_to_timestamp(datetime):
    return int(time.mktime(datetime.timetuple()))

def timestamp_to_datetime(timestamp):
    return datetime.datetime.fromtimestamp(timestamp)

