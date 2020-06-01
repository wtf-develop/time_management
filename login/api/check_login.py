#!/usr/local/Cellar/python/3.7.7/Frameworks/Python.framework/Versions/3.7/bin/python3
# !/usr/bin/env python3
import os, sys, inspect, json, hashlib, time
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
sys.path.insert(0, os.path.dirname(os.path.dirname(currentdir)))  # one level up "os.path.dirname()"
from _common.api._database import mydb, mydb_connection
from _common.api import auth
from _common.api import headers

rawpost = ''
jsonpost = None
if auth.req_method == "POST":
    req_rawpost = sys.stdin.read()
    try:
        jsonpost = json.loads(req_rawpost)
    except Exception as ex:
        jsonpost = None
if jsonpost is None:
    time.sleep(1)
    headers.jsonAPI(False)
    headers.errorResponse('@str.error', '@str.bad_request', 400)

if 'login' not in jsonpost:
    time.sleep(1)
    headers.jsonAPI(False)
    headers.errorResponse('@str.error', '@str.bad_request', 400)

if 'password' not in jsonpost:
    time.sleep(1)
    headers.jsonAPI(False)
    headers.errorResponse('@str.error', '@str.bad_request', 400)

if 'remember' not in jsonpost:
    time.sleep(1)
    headers.jsonAPI(False)
    headers.errorResponse('@str.error', '@str.bad_request', 400)
try:
    jsonpost['remember'] = int(jsonpost['remember'])
except Exception as ex:
    jsonpost['remember'] = 0

jsonpost['password'] = hashlib.md5((jsonpost['password']).encode('utf-8')).hexdigest()
mydb.execute(
    'select * from users where login="' + jsonpost['login'] + '" and password="' + jsonpost['password'] + '" and status=0')
row = mydb.fetchone()
if row is None:
    headers.jsonAPI(False)
    time.sleep(2)
    headers.errorResponse('@str.error', '@str.not_found', 404)

mydb.execute('update users set lastlogin='+str(int(time.time()*1000))+' where id='+str(row['id']))


auth.credentials = auth.buildCredentials(int(row['id']), row['login'], row['password'], jsonpost['remember'], 0)
headers.jsonAPI(False)
print('{"accepted": true}')
