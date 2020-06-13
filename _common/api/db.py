import sys
import datetime
import time
import json
import random
import string


from _common.api._settings import mydb_connection, mydb
from _common.api import utils


#
# Functions for storing data for different tables
# This functions are used in many places of project
# and changes may broke everything
#
tasks_keymap = {
    'order': 'ordr',
    'device_id': 'devid',
    'defered': 'defered_interval',
    'duration': 'duration_time',
    'start': 'start_time',
    'done': 'done_time',
    'utc': 'utc_flag',
    'isUTC': 'utc_flag'

}


# return id or 0 - error, anything < 0 is  also error
def saveTask(data: dict) -> int:
    # do all necessary checks and convert types
    data = utils.replace_keys(data, tasks_keymap)
    required = set(['devid', 'title', 'desc', 'type'])
    if not(required.isubset(data.keys())):
        return -1
    # Convert all values only to Integers and Strings.
    # Other primitive types except float - it's a big lying
    int_fields = set(['id', 'devid', 'type', 'alarm_type', 'state', 'priority',
                      'ordr', 'start_time', 'done_time', 'duration_time',
                      'repeat_type', 'repeat_value', 'defered_interval', 'year',
                      'month', 'day', 'hour', 'minute', 'timezone', 'utc_flag'])
    for key, value in data:
        if(key in int_fields):
            if not(isinstance(value, int)):
                try:
                    data[key] = int(value)
                except Exception as ex:
                    return -2
        else:
            if not(isinstance(value, str)):
                try:
                    data[key] = str(value)
                except Exception as ex:
                    return -3

    if(data['devid'] < 1):
        return -4

    if data['type'] == 0:  # timer
        required = set(['alarm_type', 'start_time', 'repeat_type',
                        'repeat_value', 'defered_interval', 'year', 'month',
                        'day', 'hour', 'minute', 'timezone', 'utc_flag'])
        if not(required.isubset(data.keys())):
            return -5
    elif data['type'] == 1:  # for the whole day
        required = set(['start_time', 'duration_time', 'repeat_type',
                        'repeat_value', 'year', 'month', 'day', 'timezone'])
        if not(required.isubset(data.keys())):
            return -6
    elif data['type'] == 2:  # notes
        required = set(['state', 'priority', 'ordr'])
        if not(required.isubset(data.keys())):
            return -7

    elif data['type'] == 3:  # geo based reminders
        required = set(['start_time', 'repeat_type',
                        'repeat_value', 'locations'])
        if not(required.isubset(data.keys())):
            return -8
    else:
        return -9  # not supported task type

    timestampstr = str(int(time.time() * 1000))

    if('id' not in data) or (data['id'] < 1):  # new record in tasks
        data['id'] = 0
        data['globalid'] = timestampstr + '-' + utils.rand_string() + \
            str(data['type'] + str(data['devid']))
        data['created'] = timestampstr  # dont change this later never!

    if('globalid' not in data) or (len(data['globalid']) < 10):
        # Error globalid must always present!
        # if its new record - it will be updated by prev condition
        # ->> if('id' not in data) or (data['id'] < 1) <<-
        return -10

    # always update time after any changes
    data['update_time'] = timestampstr
    if(data['id'] > 0):  # dont change this values!
        data.pop('created', None)
        data.pop('globalid', None)

    sql = ''
    if(data['id'] > 0):
        sql = 'update tasks set ' + \
            __build_update(data) + ' where id=' + data['id']
        try:
            mydb.execute(sql)
        except Exception as ex:
            return -11
        return data['id']
    else:
        sql = 'insert into tasks ' + __build_insert(data)
        try:
            mydb.execute(sql)
        except Exception as ex:
            return -12
        data['id'] = mydb_connection.insert_id()
        return data['id']

    return 0


def __build_update(data: dict) -> str:
    result = ""
    for key, value in data.items():
        if (key == 'id') or (key == 'globalid') or (key == 'created'):  # ignore this fields
            continue
        if(isinstance(value, str)):
            result = result + key + '="' + \
                mydb_connection.escape_string(value) + '",'
        elif(isinstance(value, int)):
            result = result + key + '=' + str(value) + ','
    return result.strip(", ")


def __build_insert(data: dict) -> str:
    prefix = ""
    postfix = ""
    for key, value in data.items():
        if (key == 'id'):  # ignore this fields
            continue
        if (isinstance(value, str)):
            prefix = prefix + key + ','
            postfix = postfix + '"' + \
                mydb_connection.escape_string(value) + '",'

        elif(isinstance(value, int)):
            prefix = prefix + key + ','
            postfix = postfix + str(value) + ','
    # return last part of insert statement
    return '(' + prefix.strip(", ") + ') values (' + postfix.strip(", ") + ')'


def getUserLinkedDevices(user_id: int, devid: int = 0, incomming: bool = True, outgoing: bool = True) -> dict:
    result = {
        'in': {'0': [], '1': [], '2': [], '3': [], 'all': []},
        'out': {'0': [], '1': [], '2': [], '3': [], 'all': []},
        'all': {},
        'names': {}}

    addsql = ''
    if devid > 0:
        addsql = ' and d2.id=' + str(devid) + ' '

    if incomming:
        # get external devices that send info to user  id - src (ext-dev), dst - user device
        sql = '''select d2.name as dst_name,s.dst,d.name,d.id,s.chanel0,s.chanel1,s.chanel2,s.chanel3 from devices as d
                inner join sync_devices as s on s.src=d.id
                inner join devices as d2 on s.dst=d2.id and d2.`uid`=''' + str(user_id) + addsql + ''' and d2.`state`>0
                where d.state>0
                '''

        # utils.debug(sql)
        mydb.execute(sql)
        rows = mydb.fetchall()
        result_all = result['all']
        result_names = result['names']

        result_in = result['in']
        obj = {}
        for row in rows:
            result_names[row['id']] = row['name']  # external
            result_names[row['dst']] = row['dst_name']
            result_all[row['id']] = {'id': row['id'], 'name': row['name']}
            obj = {'src': row['id'], 'dst': row['dst']}
            result_in['all'].append(obj)
            if(row['chanel0'] == 0):
                result_in['0'].append(obj)
            if(row['chanel1'] == 1):
                result_in['1'].append(obj)
            if(row['chanel2'] == 2):
                result_in['2'].append(obj)
            if(row['chanel3'] == 3):
                result_in['3'].append(obj)

    if outgoing:
        # get external devices that receive info from user  id - desctination (ext-dev), src - user device
        sql = '''select d2.name as src_name,s.src,d.name,d.id,s.chanel0,s.chanel1,s.chanel2,s.chanel3 from devices as d
            inner join sync_devices as s on s.dst=d.id
            inner join devices as d2 on s.src=d2.id and d2.`uid`=''' + str(user_id) + addsql + ''' and d2.`state`>0
            where d.state>0
            '''

        # utils.debug(sql)
        mydb.execute(sql)
        rows = mydb.fetchall()
        result_out = result['out']
        for row in rows:
            result_names[row['id']] = row['name']  # external
            result_names[row['src']] = row['src_name']
            result_all[row['id']] = {'id': row['id'], 'name': row['name']}
            obj = {'src': row['src'], 'dst': row['id']}
            result_out['all'].append(obj)
            if(row['chanel0'] == 0):
                result_out['0'].append(obj)
            if(row['chanel1'] == 1):
                result_out['1'].append(obj)
            if(row['chanel2'] == 2):
                result_out['2'].append(obj)
            if(row['chanel3'] == 3):
                result_out['3'].append(obj)

    return result


def getUserOwnDevices(user_id: int, devid: int = 0) -> dict:
    result = {'0': [], '1': [], '2': [], '3': [], 'all': []}

    addsql = ''
    if devid > 0:
        addsql = ' and d.id=' + str(devid) + ' '

    sql = '''select d.id,d.name,chanel0,chanel1,chanel2,chanel3
    from devices d
    where d.uid=''' + str(user_id) + addsql + ''' and d.state>0
    '''
    mydb.execute(sql)
    rows = mydb.fetchall()

    # myown device will get all data that its owned
    for row in rows:
        result['all'].append(row)
        if(row['chanel0'] == 0):
            result['0'].append(row['id'])
        if(row['chanel1'] == 1):
            result['1'].append(row['id'])
        if(row['chanel2'] == 2):
            result['2'].append(row['id'])
        if(row['chanel3'] == 3):
            result['3'].append(row['id'])
    return result


def getUserLinkedTasks(devid: int) -> list:
    result = []
    sql = '''select d.id
    from sync_tasks s, tasks t
    where s.dst=''' + str(devid) + ''' and s.tid=t.id and t.state=20'''

    mydb.execute(sql)
    rows = mydb.fetchall()
    # myown device will get all data that its owned

    for row in rows:
        result.append(row['id'])

    if len(result) < 1:
        result.append(0)
    return result
