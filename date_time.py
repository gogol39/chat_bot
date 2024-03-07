import datetime

def get_current_datetime():
    current_datetime = datetime.datetime.now()
    return current_datetime

def get_formatted_datetime():
    current_datetime = get_current_datetime()
    current_datetime += datetime.timedelta(hours=3)
    formatted_datetime = current_datetime.strftime("%Y-%m-%d %H:%M:%S")
    return formatted_datetime
