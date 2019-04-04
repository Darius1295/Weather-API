import datetime
import calendar
import pytz
from timezonefinder import TimezoneFinder


def get_datetime(timestamp):
    return datetime.datetime.fromtimestamp(timestamp, tz=pytz.UTC)


def get_weekday(my_datetime):
    if my_datetime.date() == datetime.date.today():
        return 'Today'
    else:
        return calendar.day_name[my_datetime.weekday()]


def get_timezone(my_datetime, longitude, latitude):
    my_tz = TimezoneFinder(in_memory=True).timezone_at(lng=longitude, lat=latitude)
    return my_datetime.astimezone(pytz.timezone(my_tz))


def get_time(date):
    return date.strftime('%H:%M')
