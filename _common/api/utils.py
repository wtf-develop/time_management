import re
import sys
import random
import string
import zlib


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
    mykey = -1
    for key, value in array:
        mykey = -1
        myval = 0
        try:
            mykey = int(key)
        except Exception as ex:
            continue
        if mykey < 0:
            continue

        try:
            myval = int(value)
        except Exception as ex:
            res = bitClear(res, key)
            continue

        if myval == 1:
            res = bitSet(res, mykey)
        else:
            res = bitClear(res, mykey)
    return res


def bits2array(intval: int, bitscount: int = 32) -> list:
    result = [0] * bitscount
    for i in range(bitscount):
        if bitTest(intval, i):
            result[i] = 1
        else:
            result[i] = 0
    return result


__letters = string.ascii_lowercase


def rand_string() -> str:
    rand_str = ''.join(random.choice(__letters) for i in range(9))


# result not depend from simbols order. Good!
def crc32(s: str) -> int:
    return zlib.crc32(s.encode(encoding="utf-8", errors="ignore"), 2)


# convert keys for database
def replace_keys(data: dict, keymap: dict) -> dict:
    for key, value in keymap.items():
        if(key in data):
            data[value] = data.pop(key, None)
    # and return updated fields
    return data


def debug(s):
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
