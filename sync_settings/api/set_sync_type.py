#!/usr/local/bin/python3
# this script it's a small Hell. Live is hard...
import inspect
import os
import sys

currentdir = os.path.dirname(os.path.abspath(
        inspect.getfile(inspect.currentframe())))
sys.path.insert(0, os.path.dirname(os.path.dirname(currentdir)))
from _common.api.auth import safeGETint
from _common.api import headers
from _common.api import auth
from _common.api import db

headers.jsonAPI()

sync0 = safeGETint('sync0')
sync1 = safeGETint('sync1')
sync2 = safeGETint('sync2')
sync3 = safeGETint('sync3')
if sync0 == 1:
    sync0 = 0
else:
    sync0 = -1

if sync1 == 1:
    sync1 = 1
else:
    sync1 = -1

if sync2 == 1:
    sync2 = 2
else:
    sync2 = -1

if sync3 == 1:
    sync3 = 3
else:
    sync3 = -1

src = safeGETint('src')
if src < 0:
    headers.errorResponse('@str.permission_denied')
dst = safeGETint('dst')
db.sql_request('select id from devices where id=' + str(src) + ' and uid=' +
               str(auth.user_id) + ' and state>0 and `default`=0')
row = db.mydb.fetchone()
if (row is None) or ('id' not in row) or (row['id'] is None) or (int(row['id']) < 1) or (int(row['id']) != src):
    headers.errorResponse('@str.permission_denied')

if dst > 0:
    db.sql_request('select id from devices where id=' + str(dst) + ' and uid!=' + str(auth.user_id) + ' and state>0')
    row = db.mydb.fetchone()
    if (row is None) or ('id' not in row) or (row['id'] is None) or (int(row['id']) < 1) or (int(row['id']) != dst):
        headers.errorResponse('@str.permission_denied')
else:
    db.sql_request('update devices set sync0=' + str(sync0) + ',sync1=' + str(sync1) +
                   ',sync2=' + str(sync2) + ',sync3=' + str(sync3) + ' where id=' + str(src))
    headers.goodResponse({'saved': True})

db.sql_request('update sync_devices set sync0=' + str(sync0) + ',sync1=' + str(sync1) +
               ',sync2=' + str(sync2) + ',sync3=' + str(sync3) +
               ' where src=' + str(src) + ' and dst=' + str(dst) + ' and state>0')
headers.goodResponse({'saved': True})
