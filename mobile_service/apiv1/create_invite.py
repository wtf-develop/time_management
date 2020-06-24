#!/usr/local/bin/python3
import inspect
import os
import sys
import time

currentdir = os.path.dirname(os.path.abspath(
        inspect.getfile(inspect.currentframe())))
sys.path.insert(0, os.path.dirname(os.path.dirname(currentdir)))
from _common.api._settings import mydb
from _common.api import auth
from _common.api import headers
from _common.api import utils
from mobile_service.apiv1._mobile import sql_request

headers.jsonAPI()

jsonpost = auth._POST

if (jsonpost is None) or ('login' not in jsonpost) or ('device' not in jsonpost):
    headers.errorResponse('Bad request')

login = utils.clearUserLogin(jsonpost['login'])
device = utils.clearUserLogin(jsonpost['device'])

sql_request('select id from users where login="' + login + '" and state>0')
uid = 0
rows = mydb.fetchall()
for row in rows:
    uid = int(row['id'])

sql_request('select id from devices where uid=' + str(uid) + ' and name="' + device + '"')
another_device = 0
rows = mydb.fetchall()
for row in rows:
    another_device = int(row['id'])

if (another_device < 1) or (uid < 1):
    headers.errorResponse('Not found')

my_device = auth.user_some_state

if (auth.user_id == uid) or (another_device == my_device):
    headers.errorResponse('You already have full access to your own devices')

sql_request(
    'select id, state, invite from sync_devices where src=' + str(my_device) + ' and dst=' + str(another_device))
link_id = 0
link_state = 0
link_invite = ''
rows = mydb.fetchall()
for row in rows:
    link_id = int(row['id'])
    link_state = int(row['state'])
    link_invite = row['invite']
if link_state > 0:
    headers.errorResponse('You already can send information to this device')

if link_id > 0:
    if len(link_invite) > 3:
        headers.goodResponse({'invite': link_invite.upper()})
    link_invite = utils.rand_string(5)
    sql_request('update sync_devices set state=0,invite="' + link_invite + '" where id=' + str(link_id))

else:
    link_invite = utils.rand_string(5)
    sql_request(
            'insert into sync_devices (src,dst,state,invite,created) values (' + str(my_device) + ',' + str(
                another_device) + ',0,"' + link_invite + '",' + str(int(time.time() * 1000)) + ')')
headers.goodResponse({'invite': link_invite.upper()})
