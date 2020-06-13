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
                except Exception:
                    return -2
        else:
            if not(isinstance(value, str)):
                try:
                    data[key] = str(value)
                except Exception:
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
        except Exception:
            return -11
        return data['id']
    else:
        sql = 'insert into tasks ' + __build_insert(data)
        try:
            mydb.execute(sql)
        except Exception:
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
        'in': {
            '0': [], '1': [], '2': [], '3': [],
            'all': {}  # map of all external-ids - senders
        },
        'out': {
            '0': [], '1': [], '2': [], '3': [],
            'all': {}  # map of all external-ids - receivers
        },
        'all': {},  # map of all external-ids, without own ids
        'names': {},  # simply map of all names with login
    }

    addsql = ''
    if devid > 0:
        addsql = ' and d2.id=' + str(devid) + ' '

    if incomming:
        # get external devices that send info to user  id - src (ext-dev), dst - user device
        sql = '''select u.login,d2.name as dst_name,s.dst,d.name,d.id,s.chanel0,s.chanel1,s.chanel2,s.chanel3
                from devices as d
                inner join sync_devices as s on s.src=d.id
                inner join devices as d2 on s.dst=d2.id and d2.`uid`=''' + str(user_id) + addsql + ''' and d2.`state`>0
                inner join users as u on d.uid=u.id
                where d.state>0
                '''

        # utils.debug(sql)
        mydb.execute(sql)
        rows = mydb.fetchall()
        result_all = result['all']
        result_names = result['names']

        result_in = result['in']
        result_in_all = result_in['all']
        obj = {}
        for row in rows:
            result_names[row['id']] = {  # external
                'device': row['name'],
                'user': row['login']
            }
            result_names[row['dst']] = {
                'device': row['dst_name']
            }
            result_all[row['id']] = row['id']
            result_in_all[row['id']] = row['id']
            obj = {'src': row['id'], 'dst': row['dst']}
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
        sql = '''select u.login,d2.name as src_name,s.src,d.name,d.id,s.chanel0,s.chanel1,s.chanel2,s.chanel3 from devices as d
            inner join sync_devices as s on s.dst=d.id
            inner join devices as d2 on s.src=d2.id and d2.`uid`=''' + str(user_id) + addsql + ''' and d2.`state`>0
            inner join users as u on d.uid=u.id
            where d.state>0
            '''
        # utils.debug(sql)
        mydb.execute(sql)
        rows = mydb.fetchall()
        result_out = result['out']
        result_out_all = result_out['all']
        for row in rows:
            result_names[row['id']] = {  # external
                'device': row['name'],
                'user': row['login']
            }
            result_names[row['src']] = {
                'device': row['src_name']
            }
            result_all[row['id']] = row['id']
            result_out_all[row['id']] = row['id']
            obj = {'src': row['src'], 'dst': row['id']}
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

    sql = '''select d.id,d.name,chanel0,chanel1,chanel2,chanel3
    from devices d
    where d.uid=''' + str(user_id) + ''' and d.state>0
    '''

    if devid > 0:
        sql = '''select d.id,d.name,
            CASE WHEN d.chanel0<d2.chanel0 then d.chanel0 else d2.chanel0 end as chanel0,
            CASE WHEN d.chanel1<d2.chanel1 then d.chanel1 else d2.chanel1 end as chanel1,
            CASE WHEN d.chanel2<d2.chanel2 then d.chanel2 else d2.chanel2 end as chanel2,
            CASE WHEN d.chanel3<d2.chanel3 then d.chanel3 else d2.chanel3 end as chanel3
            from devices d
            inner join devices d2 on d.uid=d2.uid and d2.id=''' + str(devid) + ''' and d2.state>0
            where d.uid=''' + str(user_id) + ''' and d.id!=''' + str(devid) + ''' and d.state>0
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


def getUserLinkedTasks(user_id: int, devid: int = 0) -> list:
    result = []

    addsql = ''
    if devid > 0:
        addsql = ' and d.id=' + str(devid) + ' '
    sql = '''select t.id
        from tasks as t
        inner join sync_tasks as s on t.id=s.tid
        inner join devices as d on d.id=s.dst and d.uid=''' + str(uid) + addsql + ''' and d.state>0
    '''

    mydb.execute(sql)
    rows = mydb.fetchall()
    # myown device will get all data that its owned

    for row in rows:
        result.append(row['id'])

    if len(result) < 1:
        result.append(0)
    return result
