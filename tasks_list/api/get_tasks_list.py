#!/usr/local/bin/python3
import inspect
import os
import sys

currentdir = os.path.dirname(os.path.abspath(
        inspect.getfile(inspect.currentframe())))
sys.path.insert(0, os.path.dirname(os.path.dirname(currentdir)))
from _common.api.auth import _GET
from _common.api import headers
from _common.api import db
from _common.api import auth
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

panels = [
    {
        'state': 20,
        "id": "inprogress",
        'pname': '@str.inprogress',
        'items': []
    },
    {
        'state': 30,
        "id": "completed",
        'pname': '@str.completed',
        'items': []
    },
    {
        'state': 40,
        "id": "canceled",
        'pname': '@str.canceled',
        'items': []
    }

]
items_20 = panels[0]['items']
items_30 = panels[1]['items']
items_40 = panels[2]['items']

sql_filter = db.buildSqlPermissionfilter(auth.user_id, devid, True)
sql = 'select * from tasks t where t.type=2 and ' + sql_filter + ' order by t.state, t.priority desc,t.update_time desc limit 600'
db.sql_request(sql)
rows = mydb.fetchall()
json_result = []
toastMessage=None
if (rows is None) or len(rows) < 1:
    toastMessage='@str.no_notes'
for row in rows:
    obj = {'id': row['id'], 'title': row['title'], 'desc': row['desc'], 'priority': row['priority']}
    if row['state'] == 20:
        items_20.append(obj)
    elif row['state'] == 30:
        items_30.append(obj)
    elif row['state'] == 40:
        items_40.append(obj)

headers.goodResponse({'panels': panels},toastMessage)
