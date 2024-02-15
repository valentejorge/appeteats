"""Module providing a format data from database"""
from datetime import datetime


def format_opening_hours(data):
    """format date from database"""
    restaurant_time = []

    week = {
        0: "monday", 1: "tuesday", 2: "wednesday",
        3: "thursday", 4: "friday", 5: "saturday", 6: "sunday"
    }

    for day in data:
        if day.opening_time is not None or day.closing_time is not None:
            formatted_day = {
                "open": day.open,
                "day_of_week": week[day.day_of_week].capitalize(),
                "opening_time": day.opening_time.strftime("%H:%M"),
                "closing_time": day.closing_time.strftime("%H:%M")
            }
        else:
            formatted_day = {
                "open": day.open,
                "day_of_week": week[day.day_of_week].capitalize(),
                "opening_time": '00:00',
                "closing_time": '00:00'
            }
        restaurant_time.append(formatted_day)

    return restaurant_time


def restaurant_is_open(day_time_data):
    """check if the restaurant is opening"""
    def time_to_seconds(t):
        return t.hour * 3600 + t.minute * 60 + t.second

    date = datetime.now()
    hours = date.time()
    weekday = date.weekday()

    today = day_time_data[weekday]

    if today.opening_time is None or today.closing_time is None:
        return False

    open_time = time_to_seconds(today.opening_time)
    close_time = time_to_seconds(today.closing_time)
    hours = time_to_seconds(hours)

    if close_time < open_time:
        close_time += 24 * 3600

    if open_time <= hours <= close_time:
        return True

    return False
