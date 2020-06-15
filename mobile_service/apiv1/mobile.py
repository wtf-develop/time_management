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


# SQL query MUST be optimized - later
def getTotalIdsString(user_id: int, devid: int) -> str:
    links = getLinkedDevices(user_id, devid)
    own = getOwnDevices(user_id, devid)
    tasks = getLinkedTasks(user_id, devid)
    result = []
    sql = '''
    select group_concat(globalid separator ',') as val, max(update_time) as time, sum(serial) as serial from tasks
    where state=20 and
    (
    (id in (''' + ','.join(tasks) + '''))
    or
    (type=0 and devid in (''' + (','.join(list(set().union(links['0'], own['0'])))) + '''))
    or
    (type=1 and devid in (''' + (','.join(list(set().union(links['1'], own['1'])))) + '''))
    or
    (type=2 and devid in (''' + (','.join(list(set().union(links['2'], own['2'])))) + '''))
    or
    (type=3 and devid in (''' + (','.join(list(set().union(links['3'], own['3'])))) + '''))
    )
    '''
    mydb.execute(sql)
    row = mydb.fetchone()
    if (row is None):
        return {'val': '', 'time': 0, 'serial': 0}
    if 'val' not in row:
        return {'val': '', 'time': 0, 'serial': 0}
    if row['val'] is None:
        return {'val': '', 'time': 0, 'serial': 0}
    return row
    # myown device will get all data that its owned


def getLinkedDevices(user_id: int, devid: int) -> dict:
    result = {'0': [], '1': [], '2': [], '3': [], 'all': []}

    links = db.getUserLinkedDevices(
            user_id=user_id, devid=devid, incomming=True, outgoing=False)

    for key, value in links['all']:
        result['all'].append({'id': value, 'name': links['names'][value]})

    for value in links['in']['0']:
        result['0'].append(value['src'])
    for value in links['in']['1']:
        result['1'].append(value['src'])
    for value in links['in']['2']:
        result['2'].append(value['src'])
    for value in links['in']['3']:
        result['3'].append(value['src'])

    if len(result['0']) < 1:
        result['0'].append(0)
    if len(result['1']) < 1:
        result['1'].append(0)
    if len(result['2']) < 1:
        result['2'].append(0)
    if len(result['3']) < 1:
        result['3'].append(0)
    if len(result['all']) < 1:
        result['all'].append({'id': 0, 'name': ''})
    return result


def getOwnDevices(user_id: int, devid: int) -> dict:
    result = db.getUserOwnDevices(user_id, devid)

    if len(result['0']) < 1:
        result['0'].append(0)
    if len(result['1']) < 1:
        result['1'].append(0)
    if len(result['2']) < 1:
        result['2'].append(0)
    if len(result['3']) < 1:
        result['3'].append(0)
    if len(result['all']) < 1:
        result['all'].append(0)
    return result


def getLinkedTasks(user_id: int, devid: int) -> list:
    result = db.getUserLinkedTasks(user_id, devid)
    if len(result) < 1:
        result.append(0)
    return result


def log(message: str, tag: str = '  info'):
    utils.log(message, tag, 'mobile')


def elog(message: str, tag: str = 'error'):
    utils.log(message, tag, 'mobile_error')
