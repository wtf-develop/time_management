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
from mobile_service.apiv1 import mobile
from _common.api import translation


def badExit(index: int):
    auth.credentials = auth.buildCredentials(0, '', '', 0, 0)
    headers.jsonAPI(False)
    time.sleep(1)
    mobile.elog('Request error - ' + str(index), 'reg')
    headers.errorResponse(
            'Bad request - ' + str(index), ' Request to server is incorrect', 400)


def wrongCred(index: int):
    auth.credentials = auth.buildCredentials(0, '', '', 0, 0)
    headers.jsonAPI(False)
    time.sleep(1)
    mobile.elog('Credentials error - ' + str(index), 'auth')
    headers.errorResponse('Incorrect login or password', 'user not found - ' + str(index), 404)


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

if ('crc32_control' not in jsonpost) or ('crc32_str' not in jsonpost):
    badExit(5)
crc32_control = int(jsonpost['crc32_control'])
if crc32_control != utils.crc32(str(jsonpost['crc32_str'])):
    auth.credentials = auth.buildCredentials(0, '', '', 0, 0)
    headers.jsonAPI(False)
    time.sleep(1)
    mobile.elog('CRC32 algorithm control mistake', 'critical')
    headers.errorResponse("CRC32 algorithm error")

if len(jsonpost['login']) < 4 or len(jsonpost['password']) < 4 or len(jsonpost['device']) < 4:
    auth.credentials = auth.buildCredentials(0, '', '', 0, 0)
    headers.jsonAPI(False)
    time.sleep(1)
    mobile.elog('Too short symbols', 'auth')
    headers.errorResponse(translation.getValue('mobile_too_short'))

jsonpost['remember'] = -1
if auth.isMobile:  # Yes only from Mobile!!!
    jsonpost['remember'] = 1
else:
    badExit(6)

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
    mobile.log('New user registered id:' + str(auth.user_id))
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
    mobile.log('New device added id:' + str(auth.user_some_state))
else:
    auth.user_some_state = int(dev['id'])

if auth.user_some_state < 1:
    wrongCred(4)

auth.credentials = auth.buildCredentials(
        int(auth.user_id), jsonpost['login'], jsonpost['password'], 1, auth.user_some_state)
headers.jsonAPI(False)
mobile.log('Token was sent to device id:' + str(auth.user_some_state))
headers.goodResponse({'accepted': True, 'token': auth.credentials})
