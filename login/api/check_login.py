#!/usr/local/bin/python3

import hashlib
import inspect
import os
import sys
import time

currentdir = os.path.dirname(os.path.abspath(
        inspect.getfile(inspect.currentframe())))
sys.path.insert(0, os.path.dirname(os.path.dirname(currentdir)))
from _common.api import utils
from _common.api import headers
from _common.api import auth
from _common.api._settings import mydb


def badExit(index: int = 0):
    auth.credentials = auth.buildCredentials(0, '', '', 0, 0)
    headers.jsonAPI(False)
    time.sleep(1)
    headers.errorResponse(
            ' @str.bad_request', '@str.error',400)


def wrongCred():
    auth.credentials = auth.buildCredentials(0, '', '', 0, 0)
    headers.jsonAPI(False)
    time.sleep(1)
    headers.errorResponse('@str.user_not_found','@str.error',  404)


if (auth.isMobile):  # login from mobile not accepted here
    badExit(0)

jsonpost = auth._POST

if jsonpost is None:
    badExit(1)

if 'login' not in jsonpost:
    badExit(2)

if 'password' not in jsonpost:
    badExit(3)

if auth.isMobile:
    badExit(3)
else:
    if 'remember' not in jsonpost:
        badExit(5)
    else:
        try:
            jsonpost['remember'] = int(jsonpost['remember'])
        except Exception:
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
        'select id,login,fail_login_counter,fail_login_timestamp,password,state from users where login="' + jsonpost[
            'login'] +
        '" and state>0')
usr = mydb.fetchone()
if usr is None:
    wrongCred()

if usr['fail_login_timestamp'] is None:
    usr['fail_login_timestamp'] = 0

if usr['fail_login_counter'] is None:
    usr['fail_login_counter'] = 0

timestamp_int = int(time.time() * 1000)
if (abs(timestamp_int - int(usr['fail_login_timestamp'])) < 60 * 1000) and (int(usr['fail_login_counter']) > 5):
    auth.credentials = auth.buildCredentials(0, '', '', 0, 0)
    headers.jsonAPI(False)
    time.sleep(1)
    headers.errorResponse('@str.wait_1_min', '@str.attention', 403)

timestamp_string = str(timestamp_int)
if usr['password'] != jsonpost['password'] or int(usr['state']) < 1:
    mydb.execute(
            'update users set fail_login_counter=(fail_login_counter+1),fail_login_timestamp=' + timestamp_string + ' where id=' + str(
                    usr['id']))
    wrongCred()  # auth fail

auth.user_id = int(usr['id'])  # before! buildCredentials call
if auth.isMobile:
    badExit()  # using this form from mobile app APIs is not permitted
else:
    mydb.execute('update users set fail_login_counter=0,fail_login_timestamp=0,lastlogin=' +
                 timestamp_string + ' where id=' + str(auth.user_id))

auth.credentials = auth.buildCredentials(
        auth.user_id, usr['login'], usr['password'], jsonpost['remember'], auth.user_some_state)
headers.jsonAPI(False)  # New cookie always there
utils.log(usr['login'] + ' Logged in', 'auth')
headers.goodResponse({'accepted': True})

