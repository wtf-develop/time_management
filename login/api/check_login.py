#!/usr/local/Cellar/python/3.7.7/Frameworks/Python.framework/Versions/3.7/bin/python3
# !/usr/bin/env python3
import os
import sys
import inspect
import json
import hashlib
import time
currentdir = os.path.dirname(os.path.abspath(
    inspect.getfile(inspect.currentframe())))
sys.path.insert(0, os.path.dirname(os.path.dirname(currentdir)))
from _common.api import utils
from _common.api import headers
from _common.api import auth
from _common.api._database import mydb, mydb_connection


def badExit(index: int):
    auth.credentials = auth.buildCredentials(0, '', '', 0, 0)
    headers.jsonAPI(False)
    time.sleep(1)
    headers.errorResponse(
        '@str.error', ' @str.bad_request - ' + str(index), 400)


def wrongCred(index: int):
    auth.credentials = auth.buildCredentials(0, '', '', 0, 0)
    headers.jsonAPI(False)
    time.sleep(1)
    headers.errorResponse('@str.error', '@str.not_found - ' + str(index), 404)


jsonpost = auth._POST

if jsonpost is None:
    badExit(1)

if 'login' not in jsonpost:
    badExit(2)

if 'password' not in jsonpost:
    badExit(3)

if auth.isMobile:
    jsonpost['remember'] = 1
    if 'device' not in jsonpost:
        badExit(4)
else:
    if 'remember' not in jsonpost:
        badExit(5)
    else:
        try:
            jsonpost['remember'] = int(jsonpost['remember'])
        except Exception as ex:
            jsonpost['remember'] = 0

if 'device' not in jsonpost:
    jsonpost['device'] = ''

if (jsonpost['remember'] > 1) or (jsonpost['remember'] < 0):
    badExit(6)

jsonpost['device'] = utils.clearUserLogin(jsonpost['device'])[:50]
jsonpost['login'] = utils.clearUserLogin(jsonpost['login'])
jsonpost['password'] = hashlib.md5(
    (jsonpost['password']).encode('utf-8')).hexdigest().lower()
auth.user_some_state = 0
auth.user_id = 0
mydb.execute(
    'select id,login,password from users where login="' + jsonpost['login'] +
    '" and password="' + jsonpost['password'] +
    '" and state>0')
usr = mydb.fetchone()
if usr is None:
    wrongCred(1)

auth.user_id = int(usr['id'])
timestamp_string = str(int(time.time() * 1000))
if auth.isMobile:
    mydb.execute(
        'select id from devices where uid=' + str(auth.user_id) +
        ' and name="' + jsonpost['device'] +
        '" and state>0')
    dev = mydb.fetchone()
    if dev is None:
        wrongCred(2)

    auth.user_some_state = int(dev['id'])
    if auth.user_some_state < 1:
        wrongCred(3)
    mydb.execute('update devices set lastconnect=' +
                 timestamp_string + ' where uid=' + str(auth.user_id) + ' and id=' + str(auth.user_some_state))
else:
    mydb.execute('update users set lastlogin=' +
                 timestamp_string + ' where id=' + str(auth.user_id))


auth.credentials = auth.buildCredentials(
    auth.user_id, usr['login'], usr['password'], jsonpost['remember'], auth.user_some_state)
headers.jsonAPI(False)  # New cookie always there
if auth.isMobile:
    print('{"accepted": true, "token":"' + auth.credentials + '"}')
else:
    print('{"accepted": true}')
