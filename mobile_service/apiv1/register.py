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
    time.sleep(1)
    headers.jsonAPI(False)
    headers.errorResponse(
        '@str.error', ' @str.bad_request - ' + str(index), 400)


jsonpost = auth._POST

if jsonpost is None:
    badExit(1)

if 'login' not in jsonpost:
    badExit(2)

if 'password' not in jsonpost:
    badExit(3)

if 'device' not in jsonpost:
    badExit(4)

if auth.req_agent.startswith('PlanMe APP'):
    jsonpost['remember'] = 1
else:
    if 'remember' not in jsonpost:
        badExit(4)
    else:
        try:
            jsonpost['remember'] = int(jsonpost['remember'])
        except Exception as ex:
            jsonpost['remember'] = 0


if (jsonpost['remember'] > 1) or (jsonpost['remember'] < 0):
    badExit(6)

jsonpost['login'] = utils.clearUserLogin(jsonpost['login'])
jsonpost['password'] = hashlib.md5(
    (jsonpost['password']).encode('utf-8')).hexdigest()
mydb.execute(
    'select * from users where login="' + jsonpost['login'] + '" and password="' + jsonpost['password'] + '" and state>0')
row = mydb.fetchone()
if row is None:
    headers.jsonAPI(False)
    time.sleep(2)
    headers.errorResponse('@str.error', '@str.not_found', 404)

mydb.execute('update users set lastlogin=' +
             str(int(time.time() * 1000)) + ' where id=' + str(row['id']))


auth.credentials = auth.buildCredentials(
    int(row['id']), row['login'], row['password'], jsonpost['remember'], 0)
headers.jsonAPI(False)
print('{"accepted": true, "token":"' + auth.credentials + '"}')
