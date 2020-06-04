import re


def removeDoubleSpaces(s: str):
    return ' '.join(s.strip().split())


def removeQuotes(s: str):
    return s.replace('"', '').replace("'", '').replace('`', '').strip()


def removeNonUTF(s: str):
    return bytes(s, 'utf-8').decode('utf-8', 'ignore')


def clearUserLogin(login: str):
    login = stripTags(login)
    login = removeQuotes(login)
    login = removeNonUTF(login)
    login = login.replace('\\', '').replace('/', '')
    login = removeDoubleSpaces(login)
    return login


tag_html = None


def stripTags(s: str):
    global tag_html
    if tag_html is None:
        tag_html = re.compile(r'(<!--.*?-->|<[^>]*>)')
    return tag_html.sub('', s)


def bitTest(number: int, bit_index: int):
    if number & (1 << bit_index):
        return True
    return False


def bitSet(number: int, bit_index: int):
    return number | (1 << bit_index)


def bitClear(number: int, bit_index: int):
    return number & (~(int(1 << bit_index)))


def array2bits(array: list):
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


def bits2array(intval: int, bitscount: int = 32):
    result = [0] * bitscount
    for i in range(bitscount):
        if bitTest(intval, i):
            result[i] = 1
        else:
            result[i] = 0
    return result