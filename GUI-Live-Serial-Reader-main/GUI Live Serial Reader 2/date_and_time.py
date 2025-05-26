from datetime import datetime

def get_trial_date():
    date = datetime.now()
    year = date.year
    month = date.strftime("%B")
    day = date.day
    hour = date.hour
    minute = date.minute
    second = date.second
    trial_date = [f"Date: {month} {day}, {year} - Time: {hour}:{minute}.{second}"]
    return trial_date