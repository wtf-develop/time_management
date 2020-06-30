#!/usr/local/bin/python3
import hashlib
import inspect
import os
import sys
import time

currentdir = os.path.dirname(os.path.abspath(
        inspect.getfile(inspect.currentframe())))
sys.path.insert(0, os.path.dirname(os.path.dirname(currentdir)))
from _common.api import auth
from _common.api import utils
from _common.api import headers
from _common.api._settings import mydb, mydb_connection
from mobile_service.apiv1 import _mobile
from _common.api import translation


def badExit(index: int):
    auth.credentials = auth.buildCredentials(0, '', '', 0, 0)
    headers.jsonAPI(False)
    time.sleep(1)
    _mobile.elog('Request error - ' + str(index), 'reg')
    headers.errorResponse(translation.getValue('bad_request'))


def wrongCred(index: int):
    auth.credentials = auth.buildCredentials(0, '', '', 0, 0)
    headers.jsonAPI(False)
    time.sleep(1)
    _mobile.elog('Credentials error - ' + str(index), 'auth')
    headers.errorResponse(translation.getValue('user_not_found'))


timestamp_int = int(time.time() * 1000)
timestamp_string = str(timestamp_int)
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
    _mobile.elog('CRC32 control mistake', 'critical')
    headers.errorResponse("CRC32 algorithm error")

if len(jsonpost['login']) < 4 or len(jsonpost['password']) < 4 or len(jsonpost['device']) < 4:
    auth.credentials = auth.buildCredentials(0, '', '', 0, 0)
    headers.jsonAPI(False)
    time.sleep(1)
    _mobile.elog('Too short symbols', 'auth')
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
        'select id,login,fail_login_counter,fail_login_timestamp,password,state from users where login="' + jsonpost[
            'login'] + '"')
usr = mydb.fetchone()
if usr is None:  # Need to create new record
    mydb.execute(
            'insert into users set login="' +
            jsonpost['login'] + '", password="' + jsonpost['password'] +
            '", state=1, created=' + timestamp_string)
    auth.user_id = mydb_connection.insert_id()
    if auth.user_id > 0:
        mydb.execute(
                'insert into devices set `default`=1, uid=' + str(auth.user_id) +
                ', name="Server", state=1, created=' + timestamp_string +
                ',sync0=0,sync1=1,sync2=2,sync3=3' +
                ', lastconnect=' + timestamp_string)
        _mobile.log('New user registered id:' + str(auth.user_id))
else:  # user exists, need to check permissions
    if usr['fail_login_timestamp'] is None:
        usr['fail_login_timestamp'] = 0

    if usr['fail_login_counter'] is None:
        usr['fail_login_counter'] = 0

    if (abs(timestamp_int - int(usr['fail_login_timestamp'])) < 60 * 1000) and (int(usr['fail_login_counter']) > 5):
        auth.credentials = auth.buildCredentials(0, '', '', 0, 0)
        headers.jsonAPI(False)
        time.sleep(1)
        _mobile.elog(jsonpost['login'] + ': too often wrong passwords', 'auth')
        headers.errorResponse(translation.getValue('wait_1_min'))
    # if user exists, but wrong password or state
    if (usr['password'] != jsonpost['password']) or (int(usr['state']) < 1):
        mydb.execute(
                'update users set fail_login_counter=(fail_login_counter+1),fail_login_timestamp=' + timestamp_string + ' where id=' + str(
                        usr['id']))
        usr['id'] = 0
        wrongCred(1)
    auth.user_id = int(usr['id'])

if auth.user_id < 1:
    wrongCred(3)
mydb.execute('update users set fail_login_counter=0,fail_login_timestamp=0 where id=' + str(auth.user_id))
mydb.execute(
        'select id,`default` from devices where uid=' + str(auth.user_id) +
        ' and name="' + jsonpost['device'] +
        '" and state>0')
dev = mydb.fetchone()
if dev is None:  # Need to add new device to user
    mydb.execute(
            'insert into devices set `default`=0, uid=' + str(auth.user_id) +
            ', name="' + jsonpost['device'] +
            '", state=1, created=' + timestamp_string +
            ', lastconnect=' + timestamp_string)
    auth.user_some_state = mydb_connection.insert_id()
    _mobile.log('New device added id:' + str(auth.user_some_state))
else:
    if int(dev['default']) > 0:
        headers.errorResponse('You can not use this device name')
    auth.user_some_state = int(dev['id'])

if auth.user_some_state < 1:
    wrongCred(4)

auth.credentials = auth.buildCredentials(
        int(auth.user_id), jsonpost['login'], jsonpost['password'], 1, auth.user_some_state)
headers.jsonAPI(False)
_mobile.log('Token was sent to device id:' + str(auth.user_some_state))
headers.goodResponse({'accepted': True, 'token': auth.credentials}, translation.getValue('registration_success'))
