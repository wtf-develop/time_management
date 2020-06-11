import sys
import datetime
import time
import json
import random
import string
import zlib

from _common.api import auth
from _common.api._settings import mydb_connection, mydb
from _common.api import utils


# result not depend from simbols order. Good!
def crc32(s: str) -> int:
    return zlib.crc32(s.encode(encoding="utf-8", errors="ignore"))


def getTotalIdsString(devid: int) -> str:
    if(devid < 1):
        sql = '''select globalid
        from tasks as t
        left join devices as d on d.uid=''' + auth.user_id + ''' and d.id=t.devid
        left join
        where t.state=20
        '''

    return ''
