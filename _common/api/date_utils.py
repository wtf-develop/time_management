from datetime import datetime
from datetime import timedelta
from datetime import timezone


__timezones = {}


def getTimestamp(timezone_offset: int = 0, year: int = None, month: int = None, day: int = None, hour: int = None,
                 minute: int = None, seconds: int = 0, ms: int = 1) -> dict:
    timezone_obj = None
    if (timezone_offset in __timezones):
        timezone_obj = __timezones[timezone_offset]
    else:
        timezone_obj = timezone(timedelta(minutes=timezone_offset), 'My Own Timezone')
        __timezones[timezone_offset] = timezone_obj
    today = datetime.now(timezone_obj)
    if year is not None:
        today = today.replace(year=year)
    if month is not None:
        today = today.replace(month=month)
    if day is not None:
        today = today.replace(day=day)
    if hour is not None:
        today = today.replace(hour=hour)
    if minute is not None:
        today = today.replace(minute=minute)
    if seconds is not None:
        today = today.replace(second=seconds)
    if ms is not None:
        today = today.replace(microsecond=ms)
    obj = today.timetuple()
    return {'year': obj.tm_year,
            'month': obj.tm_mon,
            'day': obj.tm_mday,
            'hour': obj.tm_hour,
            'minute': obj.tm_min,
            'tz_offset': timezone_offset,
            'tz_obj': timezone_obj,
            'timestamp': int(today.timestamp() * 1000),
            }


def getStartDayTime(timezone_offset: int) -> dict:
    return getTimestamp(timezone_offset=timezone_offset, hour=0, minute=0, seconds=0)