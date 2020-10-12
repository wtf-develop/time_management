#!/usr/local/bin/python3
import inspect
import os
import sys
import time

currentdir = os.path.dirname(os.path.abspath(
        inspect.getfile(inspect.currentframe())))
sys.path.insert(0, os.path.dirname(os.path.dirname(currentdir)))
from _common.api.auth import safeGETint
from _common.api import headers
from _common.api import db
from _common.api import auth
from _common.api import date_utils
from _common.api._settings import mydb

headers.jsonAPI()

devid = safeGETint('devid')
timezone_offset = safeGETint('timezone')

if devid < 1:
    devid = 0

sql_filter = db.buildSqlPermissionfilter(auth.user_id, devid, True)
timestamp_int = int(time.time() * 1000)
time_endinterval = timestamp_int + 300 * 24 * 60 * 60 * 1000
sql = 'select * from tasks t where (t.type=0 or t.type=1) and t.state>=20 and t.start_time<' + str(
        time_endinterval) + ' and ' + sql_filter + ' order by t.type, t.start_time'
db.sql_request(sql)
rows = mydb.fetchall()
json_result = []
toastMessage = None
if (rows is None) or len(rows) < 1:
    toastMessage = '@str.no_calendar_events'
for row in rows:
    task_time_obj = {}
    timestamp = 0
    event = {}
    event['title'] = row['title']
    event['description'] = row['desc']
    if (row['state'] == 20):
        if (row['type'] == 1):
            event['color'] = '#193'
            event['allDay'] = True
            if (row['day'] == 0):
                bug_obj = date_utils.getHumanTime(row['timezone'], row['start_time'])
                row['day'] = bug_obj['day']
                row['month'] = bug_obj['month']
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
            event['allDay'] = False
            if (row['utc_flag'] != 0):
                task_time_obj = date_utils.getHumanTime(timezone_offset=row['timezone'],
                                                        timestamp=row['start_time'])
            else:
                if (row['day'] == 0):
                    bug_obj = date_utils.getHumanTime(row['timezone'], row['start_time'])
                    row['day'] = bug_obj['day']
                    row['month'] = bug_obj['month']
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
    else:
        task_time_obj = date_utils.getHumanTime(timezone_offset=row['timezone'],
                                                timestamp=row['done_time'])
        event['start'] = str(task_time_obj['year']) + '-' +\
                         str(task_time_obj['month']).rjust(2, '0') + '-' +\
                         str(task_time_obj['day']).rjust(2, '0') + 'T' +\
                         str(task_time_obj['hour']).rjust(2, '0') + ':' +\
                         str(task_time_obj['minute']).rjust(2, '0') +\
                         ':00'
        event['color'] = '#d7d7d7'
    json_result.append(event)
headers.goodResponse({'events': json_result}, toastMessage)
