import sys
import datetime
import time
import json
import random
import string


from _common.api import auth
from _common.api._settings import mydb_connection, mydb
from _common.api import utils
from _common.api import db


# SQL query MUST be optimized later
def getTotalIdsString(user_id: int, devid: int, chanel0: int, chanel1: int, chanel2: int, chanel3: int) -> str:
    links = db.getLinkedDevices(devid)
    own = db.getOwnDevices(user_id, devid, chanel0, chanel1, chanel2, chanel3)
    tasks = db.getLinedTasks(devid)
    result = []
    sql = '''
    select group_concat(globalid separator '+') as val from tasks
    where state=20 and
    (
    (id in (''' + ','.join(tasks) + '''))
    or
    (type=0 and devid in (''' + (','.join(links['0'])) + '''))
    or
    (type=1 and devid in (''' + (','.join(links['1'])) + '''))
    or
    (type=2 and devid in (''' + (','.join(links['2'])) + '''))
    or
    (type=3 and devid in (''' + (','.join(links['3'])) + '''))
    or
    (type in (''' + chanel0 + ',' + chanel1 + ',' + chanel2 + ',' + chanel3 + ''')
     and devid in (''' + (','.join(own['all'])) + '''))
    )
    '''
    mydb.execute(sql)
    row = mydb.fetchone()
    if(row is None):
        return ''
    if 'val' not in row:
        return ''
    if row['val'] is None:
        return ''
    return row['val']
    # myown device will get all data that its owned
