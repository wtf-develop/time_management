import sys
import datetime
import time
import json
import mysql.connector
from _common.api import auth
from _common.api._settings import mydb_connection, mydb
from _common.api import utils


#
# Functions for storing data for different tables
# This functions are used in many places of project
# and changes may broke everything
#

def saveTask(data: dict):
    # do all necessary checks and convert types
    required = set(['title', 'desc', 'type', 'devid'])
    if not(required.isubset(data.keys())):
        return 1
    int_fields = ['id', 'devid', 'type', 'alarm_type', 'state', 'priority',
                  'ordr', 'start_time', 'done_time', 'duration_time',
                  'repeat_interval', 'defered_interval', 'year', 'month',
                  'day', 'hour', 'minute', 'timezone', 'isUTC']
    for key in int_fields:
        if(key in data):
            try:
                data[key] = int(data[key])
            except Exception as ex:
                return 2

    if data['type'] == 0:  # timer
        required = set(['alarm_type', 'start_time', 'repeat_interval',
                        'defered_interval', 'year', 'month',
                        'day', 'hour', 'minute', 'timezone', 'isUTC'])
        if not(required.isubset(data.keys())):
            return 3
    elif data['type'] == 1:  # for the whole day
        required = set(['start_time', 'duration_time', 'repeat_interval',
                        'year', 'month', 'day', 'timezone'])
        if not(required.isubset(data.keys())):
            return 4
    elif data['type'] == 2:  # notes
        required = set(['state', 'priority', 'ordr'])
        if not(required.isubset(data.keys())):
            return 5

    elif data['type'] == 3:  # geo based reminders
        required = set(['start_time', 'repeat_interval', 'json'])
        if not(required.isubset(data.keys())):
            return 6
    else:
        return 7
    return 0
