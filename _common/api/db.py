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
database_keymap = {
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
    data = __replace_keys(data)
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
        data['globalid'] = timestampstr + '-' + __rand_string() + \
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


__letters = string.ascii_lowercase


def __rand_string() -> str:
    rand_str = ''.join(random.choice(__letters) for i in range(9))


# convert keys for database
def __replace_keys(data: dict) -> dict:
    for key, value in database_keymap.items():
        if(key in data):
            data[value] = data.pop(key, None)
    # and return updated fields
    return data
