def format_opening_hours(data):
    restaurant_time = []

    week = {
        0: "monday", 1: "tuesday", 2: "wednesday",
        3: "thursday", 4: "friday", 5: "saturday", 6: "sunday"
    }

    for day in data:
        f = {
                "open": day.open,
                "day_of_week": week[day.day_of_week],
                "opening_time": day.opening_time.strftime("%H:%M"),
                "closing_time": day.closing_time.strftime("%H:%M")
            }
        restaurant_time.append(f)

    return restaurant_time
