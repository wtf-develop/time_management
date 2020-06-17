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
from _common.api import headers


# SQL query MUST be optimized - later
def getTotalIdsString(user_id: int, devid: int, cross: str = '', extend: bool = False) -> str:
    links = getLinkedDevices(user_id, devid)
    own = getOwnDevices(user_id, devid)  # except myself
    tasks = getLinkedTasks(user_id, devid)
    cross = utils.clearHard(cross)
    add_fields = ''
    if extend:
        add_fields = ' *,'
    if len(cross) > 0:
        cross = ' and globalid in (' + ("'" + "','".join(cross.split(',')) + "'") + ') '
    sql = '''
    select ''' + add_fields + '''globalid as fval, update_time as ftime, `serial` as fserial from tasks
    where state=20 ''' + cross + ''' and
    (
    (devid=''' + str(devid) + ''')
    or
    (id in (''' + ','.join(str(x) for x in tasks) + '''))
    or
    (type=0 and devid in (''' + (','.join(str(x) for x in list(set().union(links['0'], own['0'])))) + '''))
    or
    (type=1 and devid in (''' + (','.join(str(x) for x in list(set().union(links['1'], own['1'])))) + '''))
    or
    (type=2 and devid in (''' + (','.join(str(x) for x in list(set().union(links['2'], own['2'])))) + '''))
    or
    (type=3 and devid in (''' + (','.join(str(x) for x in list(set().union(links['3'], own['3'])))) + '''))
    )
    order by serial,update_time
    '''
    result = {'val': '', 'time': 0, 'serial': 0, 'count': 0, 'db': []}
    try:
        mydb.execute(sql)
    except Exception as ex:
        utils.log(utils.clearUserLogin(str(ex)), 'error', 'sql')
        return None

    rows = mydb.fetchall()

    val_arr = []
    count = 0
    max_time = 0
    serial = 0
    for row in rows:
        val_arr.append(row['fval'])
        count = count + 1
        temp = int(row['ftime'])
        serial = serial + int(row['fserial'])
        if temp > max_time:
            max_time = temp
        if extend:
            row.pop('fval',None)
            row.pop('ftime', None)
            row.pop('fserial', None)
            result['db'].append(row)

    result['val'] = ','.join(val_arr)
    result['time'] = max_time
    result['count'] = count
    result['serial'] = serial
    return result
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


# except myself
def getOwnDevices(user_id: int, devid: int) -> dict:
    result = db.getUserOwnDevices(user_id, devid)  # except myself

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


if not (auth.isMobile):  # check that this request from mobile application
    headers.jsonAPI(False)
    elog('Only from mobile uid:' + auth.user_id)
    headers.errorResponse('Wrong type')
