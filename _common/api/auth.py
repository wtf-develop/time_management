import os
import sys
import json
import http.cookies
import hashlib
import time
from urllib import parse
from _common.api._database import mydb, mydb_connection
from _common.api import utils


def buildCredentials(uid: int, login: str, passwd: str, remember: int, some_state: int = 0):
    global req_agent, req_scheme, req_language
    if uid == 0:
        return ''
    timestamp = 0
    login = utils.clearUserLogin(login)
    if remember == 1:
        timestamp = int(time.time()) + 90 * 24 * 60 * 60
    else:
        timestamp = int(time.time()) + 30 * 60
    hashstr = hashlib.md5(
        (str(timestamp) + str(some_state) + login + str(remember) + str(
            uid) + passwd + 'WASSUP!' + req_agent + req_scheme + req_language).encode(
            'utf-8')).hexdigest()
    return str(timestamp) + '_' + str(remember) + '_' + str(uid) + '_' + str(some_state) + '_' + hashstr


def checkCredentials(arr: list):
    global user_id, user_role, user_login, user_password, user_remember, user_some_state, req_agent, req_scheme, req_language
    if len(arr) == 5:
        timestamp = 0
        remember = 0
        uid = 0
        some_state = 0
        myhash = ''
        login = ''
        passwd = ''

        try:
            uid = int(arr[2])
        except Exception as ex:
            uid = 0
        if uid == 0:
            return False

        try:
            timestamp = int(arr[0])
        except Exception as ex:
            timestamp = 0

        try:
            remember = int(arr[1])
        except Exception as ex:
            remember = 0

        try:
            some_state = int(arr[3])
        except Exception as ex:
            some_state = 0

        myhash = arr[4]
        # TODO SQL request to database for login and password with selected uid
        if uid != 0:
            mydb.execute('select * from users where id=' +
                         str(uid) + ' and state>0')
            row = mydb.fetchone()
            if row is None:
                uid = 0
                user_id = 0
                user_role = "GUEST"
                user_login = ''
                user_password = ''
                user_remember = 0
                user_some_state = 0
                return False
            else:
                user_id = uid
                user_role = row['role']
                login = utils.clearUserLogin(row['login'])
                passwd = row['password']

        hash2 = hashlib.md5(
            (str(timestamp) + str(some_state) + login + str(remember) + str(
                uid) + passwd + 'WASSUP!' + req_agent + req_scheme + req_language).encode(
                'utf-8')).hexdigest()
        if myhash == hash2:
            user_id = uid
            user_login = utils.clearUserLogin(login)
            user_password = passwd
            user_remember = remember
            user_some_state = some_state
            return True
    uid = 0
    user_id = 0
    user_role = "GUEST"
    user_login = ''
    user_password = ''
    user_remember = 0
    user_some_state = 0
    return False


def credentialsHeader():
    return "Set-Cookie: credentials=" + credentials + "; path=/; HttpOnly; SameSite=Strict"


# -------- run part -------
# -------- run part -------
# -------- run part -------

req_cookie = http.cookies.SimpleCookie(os.environ.get("HTTP_COOKIE"))
req_ip = (os.environ.get("REMOTE_ADDR") or "").strip()[:40]
req_method = (os.environ.get("REQUEST_METHOD") or "").strip()[:10]
req_agent = (os.environ.get("HTTP_USER_AGENT") or "").strip()[:80]
req_language = (os.environ.get("HTTP_ACCEPT_LANGUAGE") or "").strip()[:20]
req_scheme = (os.environ.get("REQUEST_SCHEME")
              or "").strip()[:5]  # http or https
req_query = (os.environ.get("QUERY_STRING") or "").strip()[:350]  # parameters

_GET = None
if len(req_query) > 0:
    _GET = parse_qs(req_query)

req_rawpost = ''
_POST = None
if req_method.lower().strip() == "post":
    req_rawpost = sys.stdin.read()
    try:
        _POST = json.loads(req_rawpost)
    except Exception as ex:
        _POST = None

credentials = req_cookie.get("credentials")
if not (credentials is None):
    credentials = credentials.value
else:
    credentials = ''

user_lang = req_cookie.get("lang")
if not (user_lang is None):
    user_lang = user_lang.value
else:
    user_lang = 'en'

user_indx = req_cookie.get("indx")
if not (user_lang is None):
    try:
        user_indx = int(user_indx.value)
    except Exception as ex:
        user_indx = 0
else:
    user_indx = 0


user_role = "GUEST"
access_levels = 0
user_id = 0
user_login = ''
user_password = ''
user_remember = 0
user_some_state = 0  # page index for WEB and device id for MOBILE
if credentials is None:
    access_levels = 0
    credentials = buildCredentials(0, '', '', 0, 0)
else:
    credentials = str(credentials).strip()[:150]
    if checkCredentials(credentials.split('_', 7)):
        user_some_state = user_indx
        credentials = buildCredentials(
            user_id, user_login, user_password, user_remember, user_indx)
        user_password = ''  # reset MD5 hashed password from global variable
        access_levels = 1
    else:
        access_levels = 0
        credentials = buildCredentials(0, '', '', 0, 0)

user_password = ''  # clear MD5 hashed password from global variable
