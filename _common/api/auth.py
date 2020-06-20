import hashlib
import http.cookies
import json
import os
import sys
import time
from urllib import parse

from _common.api import db
from _common.api import utils
from _common.api._settings import debug
from _common.api._settings import logs_path
from _common.api._settings import mydb
from _common.api._settings import server_token_key


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
                    uid) + passwd + server_token_key + req_agent + req_scheme + req_language).encode(
                    'utf-8')).hexdigest().lower()
    return str(timestamp) + '_' + str(remember) + '_' + str(uid) + '_' + str(some_state) + '_' + hashstr


def __resetAuth():
    global isMobile, user_id, user_role, user_login, user_password, user_remember, user_some_state, req_agent, req_scheme, req_language
    user_id = 0
    user_role = "GUEST"
    user_login = ''
    user_password = ''
    user_remember = 0
    user_some_state = 0
    return False


def checkCredentials(arr: list):
    global user_sync0, user_sync1, user_sync2, user_sync3, isMobile, user_id, user_role, user_login, user_password, user_remember, user_some_state, req_agent, req_scheme, req_language
    if len(arr) != 5:
        return __resetAuth()

    timestamp = 0
    remember = 0
    uid = 0
    some_state = 0
    myhash = ''
    login = ''
    passwd = ''

    try:
        uid = int(arr[2])
    except Exception:
        uid = 0

    if uid < 1:
        return __resetAuth()

    try:
        timestamp = int(arr[0])
    except Exception:
        timestamp = 0

    if (timestamp < int(time.time())):
        return __resetAuth()

    try:
        remember = int(arr[1])
    except Exception:
        remember = 0

    if (isMobile) and (remember != 1):
        return __resetAuth()

    try:
        some_state = int(arr[3])
    except Exception:
        some_state = 0

    if (isMobile) and (some_state < 1):
        return __resetAuth()

    myhash = arr[4]
    # TODO SQL request to database for login and password with selected uid
    if uid > 0:
        mydb.execute('select id,login,password,role from users where id=' +
                     str(uid) + ' and state>0')
        row = mydb.fetchone()
        if row is None:
            return __resetAuth()
        else:
            uid = int(row['id'])
            user_id = uid
            user_role = row['role']
            login = utils.clearUserLogin(row['login'])
            passwd = row['password']

    if uid < 1:
        return __resetAuth()

    hash2 = hashlib.md5(
            (str(timestamp) + str(some_state) + login + str(remember) + str(
                    uid) + passwd + server_token_key + req_agent + req_scheme + req_language).encode(
                    'utf-8')).hexdigest().lower()
    if myhash != hash2:
        return __resetAuth()

    if not (isMobile):  # if not mobile - complete
        user_id = uid
        user_login = utils.clearUserLogin(login)
        user_password = passwd
        user_remember = remember
        user_some_state = some_state
        return True
    else:  # if mobile need to check device id in database
        mydb.execute('select id,sync0,sync1,sync2,sync3 from devices where id=' + str(some_state) + ' and uid=' +
                     str(uid) + ' and state>0')
        dev = mydb.fetchone()
        if row is None:
            return __resetAuth()
        else:
            # device id for mobile API. Values less then 1 are not permitted
            user_some_state = int(dev['id'])
            if user_some_state < 1:
                return __resetAuth()
            user_id = uid
            user_login = utils.clearUserLogin(login)
            user_password = passwd
            user_remember = 1
            user_sync0 = int(dev['sync0'])
            user_sync1 = int(dev['sync1'])
            user_sync2 = int(dev['sync2'])
            user_sync3 = int(dev['sync3'])
            if user_sync0 != 0:
                user_sync0 = -1
            if user_sync1 != 1:
                user_sync1 = -1
            if user_sync2 != 2:
                user_sync2 = -1
            if user_sync3 != 3:
                user_sync3 = -1
            return True
    return __resetAuth()


def credentialsHeader():
    return "Set-Cookie: credentials=" + credentials + "; path=/; HttpOnly; SameSite=Strict"


# -------- run part -------
# -------- run part -------
# -------- run part -------
req_cookie = http.cookies.SimpleCookie(os.environ.get("HTTP_COOKIE"))
req_ip = (os.environ.get("REMOTE_ADDR") or "").strip()[:39]
req_method = (os.environ.get("REQUEST_METHOD") or "").strip()[:10]
req_agent = (os.environ.get("HTTP_USER_AGENT") or "").strip()[:100]
req_language = (os.environ.get("HTTP_ACCEPT_LANGUAGE") or "").strip()[:2]
req_scheme = (os.environ.get("REQUEST_SCHEME")
              or "").strip()[:5]  # http or https
req_query = (os.environ.get("QUERY_STRING") or "").strip()[:350]  # parameters

isMobile = False
if req_agent.startswith('PlanMe mobile reminder APP'):
    isMobile = True
else:
    req_agent = req_agent[:23]
# --- debug part start ---
# --- debug part start ---
# --- debug part start ---
load_debug_config = False
if (debug):
    prefix = sys.modules['__main__'].__file__.replace('\\', '/').split('/')
    prefix = prefix[len(prefix) - 1].split('.')[0]
    # if run from console or start from debuger< there is no User-Agent
    load_debug_config = (len(req_agent) == 0)
    if load_debug_config:
        dfile = open(logs_path + prefix + '_debug_headers_dump.json', "r")
        req_headers = json.load(dfile)
        req_ip = req_headers['req_ip']
        req_method = req_headers['req_method']
        req_agent = req_headers['req_agent']
        req_language = req_headers['req_language']
        req_scheme = req_headers['req_scheme']
        req_query = req_headers['req_query']
        isMobile = req_headers['isMobile']
        dfile.close()
    else:
        dfile = open(logs_path + prefix + '_debug_headers_dump.json', "w")
        dfile.write(json.dumps(
                {'req_ip': req_ip, 'req_method': req_method, 'req_agent': req_agent, 'req_language': req_language,
                 'req_scheme': req_scheme, 'req_query': req_query, 'isMobile': isMobile}))
        dfile.close()
# --- debug part ends ---
# --- debug part ends ---
# --- debug part ends ---


_GET = None  # always not NONE. Check exact values. Device-id is always there
if len(req_query) > 0:
    _GET = parse.parse_qs(req_query)

req_rawpost = None
_POST = None
# --- debug part start ---
# --- debug part start ---
# --- debug part start ---
if (debug and load_debug_config):
    pass
# --- debug part ends ---
# --- debug part ends ---
# --- debug part ends ---
else:
    if req_method.lower().strip() == "post":
        req_rawpost = sys.stdin.read()
        try:
            _POST = json.loads(req_rawpost)
            req_rawpost = None
        except Exception:
            _POST = None

# --- debug part start ---
# --- debug part start ---
# --- debug part start ---
if (debug):
    prefix = sys.modules['__main__'].__file__.replace('\\', '/').split('/')
    prefix = prefix[len(prefix) - 1].split('.')[0]
    if load_debug_config:
        dfile = open(logs_path + prefix + '_debug_post_dump.json', "r")
        try:
            _POST = json.load(dfile)
        except Exception:
            _POST = None
        dfile.close()
    else:
        dfile = open(logs_path + prefix + '_debug_post_dump.json', "w")
        if (_POST is None):
            dfile.write('')
        else:
            dfile.write(json.dumps(_POST))
        dfile.close()
# --- debug part ends ---
# --- debug part ends ---
# --- debug part ends ---


credentials = None
if not (_GET is None) and ('credentials' in _GET) and not (_GET['credentials'] is None) and not (
        _GET['credentials'][0] is None):
    # try fetch token from GET parameter (ONLY AFTER COOKIE!!)
    credentials = _GET['credentials'][0]
else:
    credentials = req_cookie.get("credentials")
    if not (credentials is None):
        # try fetch token from cookie (FIRST!!)
        credentials = credentials.value
    else:
        credentials = ''

user_lang = req_cookie.get("lang")
if not (user_lang is None):
    user_lang = user_lang.value
else:
    user_lang = req_language
user_lang = user_lang.lower()

user_indx = 0
if not (isMobile):
    user_indx = req_cookie.get("indx")
    if not (user_indx is None):
        try:
            user_indx = int(user_indx.value)
        except Exception:
            user_indx = 0
    else:
        user_indx = 0

# --- debug part start ---
# --- debug part start ---
# --- debug part start ---
if (debug):
    prefix = sys.modules['__main__'].__file__.replace('\\', '/').split('/')
    prefix = prefix[len(prefix) - 1].split('.')[0]
    if load_debug_config:
        dfile = open(logs_path + prefix + '_debug_extra_dump.json', "r")
        extra = json.load(dfile)
        user_indx = extra['user_indx']
        user_lang = extra['user_lang']
        credentials = extra['credentials']
        dfile.close()
    else:
        dfile = open(logs_path + prefix + '_debug_extra_dump.json', "w")
        dfile.write(json.dumps({'user_indx': user_indx, 'user_lang': user_lang, 'credentials': credentials}))
        dfile.close()
# --- debug part ends ---
# --- debug part ends ---
# --- debug part ends ---


user_role = "GUEST"
access_levels = 0
user_id = 0
user_login = ''
user_password = ''
user_remember = 0

# for sync filter in mobile API, to not generate additional request to database
user_sync0 = -1
user_sync1 = -1
user_sync2 = -1
user_sync3 = -1

# page index for WEB and device_id for MOBILE (isMobile variable)
user_some_state = 0
if credentials is None:
    access_levels = 0
    credentials = buildCredentials(0, '', '', 0, 0)
else:
    credentials = str(credentials).strip()[:150]
    if checkCredentials(credentials.split('_', 7)):
        if not (isMobile):
            user_some_state = user_indx

        credentials = buildCredentials(
                user_id, user_login, user_password, user_remember, user_some_state)
        user_password = ''  # reset MD5 hashed password from global variable
        access_levels = 1
        timestamp_string = str(int(time.time() * 1000))
        if isMobile:
            mydb.execute('update devices set ' +
                         db.__build_update({'lastconnect': timestamp_string}) +
                         ' where uid=' + str(user_id) + ' and id=' + str(user_some_state))
        else:
            mydb.execute('update users set ' +
                         db.__build_update({'lastlogin': timestamp_string}) +
                         ' where id=' + str(user_id))
    else:
        access_levels = 0
        credentials = buildCredentials(0, '', '', 0, 0)

user_password = ''  # clear MD5 hashed password from global variable
