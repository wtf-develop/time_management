#!/usr/local/bin/python3

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
from _common.api._settings import mydb, mydb_connection
from _common.api import db
from mobile_service.apiv1 import functions as func


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


# Registration only from mobile device (mobile application)
if not(auth.isMobile):
    badExit(0)

timestamp_string = str(int(time.time() * 1000))
jsonpost = auth._POST

if jsonpost is None:
    badExit(1)

if 'login' not in jsonpost:
    badExit(2)

if 'password' not in jsonpost:
    badExit(3)

if 'device' not in jsonpost:
    badExit(4)

jsonpost['remember'] = -1
if auth.isMobile:  # Yes only from Mobile!!!
    jsonpost['remember'] = 1

if (jsonpost['remember'] > 1) or (jsonpost['remember'] < 0):
    badExit(6)

jsonpost['device'] = utils.clearUserLogin(jsonpost['device'])[:50]
if len(jsonpost['device']) < 1:
    badExit(7)

jsonpost['login'] = utils.clearUserLogin(jsonpost['login'])
jsonpost['password'] = hashlib.md5(
    (jsonpost['password']).encode('utf-8')).hexdigest().lower()

auth.user_some_state = 0
auth.user_id = 0
mydb.execute(
    'select id,login,password,state from users where login="' + jsonpost['login'] + '"')
usr = mydb.fetchone()
if usr is None:  # Need to create new record
    mydb.execute(
        'insert into users set login="' +
        jsonpost['login'] + '", password="' + jsonpost['password'] +
        '", state=1, created=' + timestamp_string)
    auth.user_id = mydb_connection.insert_id()
else:
    if int(usr['state']) < 1:  # if user exists, but wrong password
        usr['id'] = 0
        wrongCred(1)
    if usr['password'] != jsonpost['password']:
        usr['id'] = 0
        wrongCred(2)
    auth.user_id = int(usr['id'])

if auth.user_id < 1:
    wrongCred(3)
mydb.execute(
    'select id from devices where uid=' + str(auth.user_id) +
    ' and name="' + jsonpost['device'] +
    '" and state>0')
dev = mydb.fetchone()
if dev is None:  # Need to add new device to user
    mydb.execute(
        'insert into devices set uid=' + str(auth.user_id) +
        ', name="' + jsonpost['device'] +
        '", state=1, created=' + timestamp_string +
        ', lastconnect=' + timestamp_string)
    auth.user_some_state = mydb_connection.insert_id()
else:
    auth.user_some_state = int(dev['id'])

if auth.user_some_state < 1:
    wrongCred(4)

auth.credentials = auth.buildCredentials(
    int(usr['id']), usr['login'], usr['password'], 1, auth.user_some_state)
headers.jsonAPI(False)
print('{"accepted": true, "token":"' + auth.credentials + '"}')
