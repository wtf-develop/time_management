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

current_day = date_utils.getStartDayTime(timezone_offset)
days_time = []
timers = []
daily = []
for i in range(7):
    arr_time = current_day['timestamp'] + ((i + 1) * 24 * 60 * 60 * 1000)
    days_time.append(arr_time)
    time_info = date_utils.getHumanTime(
            timezone_offset=timezone_offset, timestamp=arr_time - 10 * 60 * 60 * 1000)
    timers.append(
            {'day': time_info['day'], 'month': time_info['month'],
             'week_day': time_info['week_day'], 'day_index': i, 'data': []})
    daily.append(
            {'day': time_info['day'], 'month': time_info['month'],
             'week_day': time_info['week_day'], 'day_index': i, 'data': []})

sql_filter = db.buildSqlPermissionfilter(auth.user_id, devid, True)
timestamp_int = int(time.time() * 1000)
time_endweek = timestamp_int + 8 * 24 * 60 * 60 * 1000
sql = 'select * from tasks t where (t.type=0 or t.type=1) and t.state=20 and t.start_time<' + str(
        time_endweek) + ' and ' + sql_filter + ' order by t.type, t.start_time'
db.sql_request(sql)
rows = mydb.fetchall()
if (rows is None) or len(rows) < 1:
    headers.infoResponse('@str.no_tasks_week')
for row in rows:
    task_time_obj = {}
    timestamp = 0
    if (row['type'] == 1):
        task_time_obj = date_utils.getTimestamp(timezone_offset=row['timezone'], year=row['year'],
                                                month=row['month'], day=row['day'], hour=row['hour'],
                                                minute=row['minute'])
        timestamp = task_time_obj['timestamp']
        for i in range(7):
            if (timestamp < days_time[i]):
                timers[i]['data'].insert(0, row)
                break
    elif (row['type'] == 0):
        if (row['utc_flag'] != 0):
            timestamp = row['start_time']
        else:
            task_time_obj = date_utils.getTimestamp(timezone_offset=row['timezone'], year=row['year'],
                                                    month=row['month'], day=row['day'], hour=row['hour'],
                                                    minute=row['minute'])
            timestamp = task_time_obj['timestamp']
        for i in range(7):
            if (timestamp < days_time[i]):
                timers[i]['data'].append(row)
                break
    #row['hour']=str(row['hour']).rjust(2, '0')
    row['minute'] = str(row['minute']).rjust(2, '0')
headers.goodResponse({'timers': timers})
