import time

def datetime_to_timestamp(datetime):
    return int(time.mktime(datetime.timetuple()))

