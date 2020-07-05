import inspect
import os
import random
import re
import string
import sys
import time
import zlib

currentdir = os.path.dirname(os.path.abspath(
        inspect.getfile(inspect.currentframe())))
sys.path.insert(0, os.path.dirname(os.path.dirname(currentdir)))

from _common.api import _settings
from _common.api import auth


def getServerVersion() -> str:
    return "0.3-beta"


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


__hard_chars = set(string.ascii_letters + string.digits + ',-_&')
__global_ids_chars = set(string.ascii_letters + string.digits + ',-&')
__float_chars = set(string.digits + '-.')
__int_chars = set(string.digits + '-')
__digits_chars = set(string.digits)
__ip_chars = set(string.digits + '.:')

def clearIp(s: str) -> str:
    global __hard_chars
    if len(s) < 1:
        return ''
    s = ''.join(filter(lambda x: x in __ip_chars, s))
    return s

def clearStringHard(s: str) -> str:
    global __hard_chars
    if len(s) < 1:
        return ''
    s = ''.join(filter(lambda x: x in __hard_chars, s))
    return s

def clearGlobalIds(s: str) -> str:
    global __global_ids_chars
    if len(s) < 1:
        return ''
    s = ''.join(filter(lambda x: x in __global_ids_chars, s))
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
