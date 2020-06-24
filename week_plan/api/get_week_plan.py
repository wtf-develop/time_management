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
from _common.api import utils
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

current_day = utils.getStartDayTime(timezone_offset)

data = {}
data['daily'] = []
data['timers'] = []
sql_filter = db.buildSqlPermissionfilter(auth.user_id, devid, True)
timestamp_int = int(time.time() * 1000)
time_endweek = timestamp_int + 8 * 24 * 60 * 60 * 1000
sql = 'select * from tasks t where (t.type=0 or t.type=1) and t.state=20 and t.start_time<' + str(
        time_endweek) + ' and ' + sql_filter + ' order by t.type, t.start_time'
db.sql_request(sql)
rows = mydb.fetchmany()
if (rows is None) or len(rows) < 1:
    headers.infoResponse('No plans for this week')
for row in rows:
    if (row['type'] == 1):
        obj = {'title': row['title'],
               'desc': row['desc'],
               'hour': row['hour'],
               'minute': row['minute']}
        data['daily'].append(obj)
    elif (row['type'] == 0):
        obj = {'title': row['title'],
               'desc': row['desc'],
               'hour': row['hour'],
               'minute': row['minute']}
        data['timers'].append(obj)
# headers.infoResponse('No plans for this week')
headers.goodResponse(data)
