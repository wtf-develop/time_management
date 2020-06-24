import random
import re
import string
import time
import zlib
from datetime import datetime
from datetime import timedelta
from datetime import timezone

from _common.api import _settings
from _common.api import auth


def getServerVersion() -> str:
    return "0.1"


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


def removeDoubleSpaces(s: str) -> str:
    return ' '.join(s.strip().split())


def removeQuotes(s: str) -> str:
    return s.replace('"', '').replace("'", '').replace('`', '').strip()


def removeNonUTF(s: str) -> str:
    return bytes(s, 'utf-8').decode('utf-8', 'ignore')


def clearUserLogin(login: str) -> str:
    login = stripTags(login)
    login = removeQuotes(login)
    login = removeNonUTF(login)
    login = login.replace('\\', '').replace(
            '/', '').replace('<', '').replace('>', '').replace('[', '').replace(
            ']', '').replace('{', '').replace('}', '').replace('%', '').replace(',', '')
    login = removeDoubleSpaces(login).lower()
    return login


__hard_chars = set(string.ascii_letters + string.digits + ',-_')
__float_chars = set(string.digits + '-.')
__int_chars = set(string.digits + '-')
__digits_chars = set(string.digits)


def clearStringHard(s: str) -> str:
    global __hard_chars
    if len(s) < 1:
        return ''
    s = ''.join(filter(lambda x: x in __hard_chars, s))
    return s


def clearFloat(s: str) -> str:
    global __float_chars
    if len(s) < 1:
        return ''
    s = ''.join(filter(lambda x: x in __float_chars, s))
    return s


def clearInt(s: str) -> str:
    global __int_chars
    if len(s) < 1:
        return ''
    s = ''.join(filter(lambda x: x in __int_chars, s))
    return s


def clearDigits(s: str) -> str:
    global __digits_chars
    if len(s) < 1:
        return ''
    s = ''.join(filter(lambda x: x in __digits_chars, s))
    return s


tag_html = None


def stripTags(s: str) -> str:
    global tag_html
    if tag_html is None:
        tag_html = re.compile(r'(<!--.*?-->|<[^>]*>)')
    return tag_html.sub('', s)


def bitTest(number: int, bit_index: int) -> bool:
    if number & (1 << bit_index):
        return True
    return False


def bitSet(number: int, bit_index: int) -> int:
    return number | (1 << bit_index)


def bitClear(number: int, bit_index: int) -> int:
    return number & (~(int(1 << bit_index)))


def array2bits(array: list) -> int:
    res = 0
    for i in range(len(array)):
        myval = 0

        try:
            myval = int(array[i])
        except Exception:
            res = bitClear(res, i)
            continue

        if myval == 1:
            res = bitSet(res, i)
        else:
            res = bitClear(res, i)
    return res


def bits2array(intval: int, bitscount: int = 32) -> list:
    result = [0] * bitscount
    for i in range(bitscount):
        if bitTest(intval, i):
            result[i] = 1
        else:
            result[i] = 0
    return result


__letters = string.ascii_lowercase + string.digits


def rand_string(strlength: int) -> str:
    rand_str = ''.join(random.choice(__letters) for i in range(strlength))
    return rand_str.lower()


# result not depend from simbols order. Good!
def crc32(s: str) -> int:
    return zlib.crc32(s.encode(encoding="utf-8", errors="ignore"))


# convert keys for database
def replace_keys(data: dict, keymap: dict) -> dict:
    for key in keymap:
        value = keymap[key]
        if key in data:
            data[value] = data.pop(key, None)
    # and return updated fields
    return data


def log(message: str, tag: str = '  info', file_postfix: str = 'web'):
    if _settings.enable_logging:
        try:
            ip = auth.req_ip.ljust(39)
            tag = tag[:6].rjust(6)
            mtime = time.localtime()
            log_time = time.strftime('%H:%M:%S', mtime)
            log_date = time.strftime('%Y-%m-%d', mtime)
            path = _settings.logs_path + log_date + '_' + file_postfix + '.log'
            flog = open(path, "a")
            flog.write(log_time + ' ' + ip + ' ' +
                       tag + ': ' + message + "\r\n")
            flog.close()
        except Exception:
            pass


def debug(s):
    if not _settings.debug:
        return
    print("Content-Type: text/html;charset=utf-8")
    print("Expires: Wed, 11 May 1983 17:30:00 GMT")
    print("Cache-Control: no-store, no-cache, must-revalidate")
    print("Cache-Control: post-check=0, pre-check=0")
    print("Pragma: no-cache")
    print("")
    print("")
    print("-------<br>\n")
    print(s)
    print("\n<br>-------<br/>\n")
