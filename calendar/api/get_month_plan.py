#!/usr/local/bin/python3
import inspect
import os
import sys
import time

currentdir = os.path.dirname(os.path.abspath(
        inspect.getfile(inspect.currentframe())))
sys.path.insert(0, os.path.dirname(os.path.dirname(currentdir)))
from _common.api.auth import _GET
from _common.api import headers
from _common.api import db
from _common.api import auth
from _common.api import date_utils
from _common.api._settings import mydb

headers.jsonAPI()

devid = 0
timezone_offset = 0
if not (_GET is None) and ('devid' in _GET) and not (_GET['devid'] is None) and not (_GET['devid'][0] is None):
    devid = int(_GET['devid'][0])

if not (_GET is None) and ('timezone' in _GET) and not (_GET['timezone'] is None) and not (_GET['timezone'][0] is None):
    timezone_offset = int(_GET['timezone'][0])

if devid < 1:
    devid = 0

sql_filter = db.buildSqlPermissionfilter(auth.user_id, devid, True)
timestamp_int = int(time.time() * 1000)
time_endinterval = timestamp_int + 300 * 24 * 60 * 60 * 1000
sql = 'select * from tasks t where (t.type=0 or t.type=1) and t.state=20 and t.start_time<' + str(
        time_endinterval) + ' and ' + sql_filter + ' order by t.type, t.start_time'
db.sql_request(sql)
rows = mydb.fetchall()
json_result = []
if (rows is None) or len(rows) < 1:
    headers.infoResponse('@str.no_tasks_week')
for row in rows:
    task_time_obj = {}
    timestamp = 0
    event = {}
    event['title'] = row['title']
    if (row['type'] == 1):
        event['color'] = '#193'
        task_time_obj = date_utils.getTimestamp(timezone_offset=row['timezone'], year=row['year'],
                                                month=row['month'], day=row['day'], hour=0,
                                                minute=0, seconds=0, ms=1)
        event['start'] = str(task_time_obj['year']) + '-' +\
                         str(task_time_obj['month']).rjust(2, '0') + '-' +\
                         str(task_time_obj['day']).rjust(2, '0')
        if (row['duration_time'] > 0):
            task_time_obj = date_utils.getHumanTime(timezone_offset=row['timezone'],
                                                    timestamp=task_time_obj['timestamp'] +\
                                                              (row['duration_time'] * 60 * 1000))
            event['end'] = str(task_time_obj['year']) + '-' +\
                           str(task_time_obj['month']).rjust(2, '0') + '-' +\
                           str(task_time_obj['day']).rjust(2, '0')

    elif (row['type'] == 0):
        event['color'] = '#47b'
        if (row['utc_flag'] != 0):
            task_time_obj = date_utils.getHumanTime(timezone_offset=row['timezone'],
                                                    timestamp=row['start_time'])
        else:
            task_time_obj = date_utils.getTimestamp(timezone_offset=row['timezone'], year=row['year'],
                                                    month=row['month'], day=row['day'], hour=row['hour'],
                                                    minute=row['minute'])
        event['start'] = str(task_time_obj['year']) + '-' +\
                         str(task_time_obj['month']).rjust(2, '0') + '-' +\
                         str(task_time_obj['day']).rjust(2, '0') + 'T' +\
                         str(task_time_obj['hour']).rjust(2, '0') + ':' +\
                         str(task_time_obj['minute']).rjust(2, '0') +\
                         ':00'
        if (row['duration_time'] > 0):
            task_time_obj = date_utils.getHumanTime(timezone_offset=row['timezone'],
                                                    timestamp=task_time_obj['timestamp'] +\
                                                              (row['duration_time'] * 60 * 1000))
            event['end'] = str(task_time_obj['year']) + '-' +\
                           str(task_time_obj['month']).rjust(2, '0') + '-' +\
                           str(task_time_obj['day']).rjust(2, '0') + 'T' +\
                           str(task_time_obj['hour']).rjust(2, '0') + ':' +\
                           str(task_time_obj['minute']).rjust(2, '0') +\
                           ':00'
    json_result.append(event)
headers.goodResponse(json_result)
