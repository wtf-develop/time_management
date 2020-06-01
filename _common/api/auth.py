import cgi, os, http.cookies, json, sys, hashlib, time


def buildCredentials(uid: int, login: str, passwd: str, remember_me: bool, some_state: int = 0):
    timestamp = 0
    remember = "0"
    if remember_me:
        timestamp = int(time.time()) + 90 * 24 * 60 * 60
        remember = "1"
    else:
        timestamp = int(time.time()) + 30 * 60
    hash = hashlib.md5((str(timestamp) + str(some_state) + login + remember + str(uid) + passwd + 'WASSUP!').encode(
        'utf-8')).hexdigest()
    return str(timestamp) + '_' + remember + '_' + str(uid) + '_' + str(some_state) + '_' + hash


def checkCredentials(arr: list):
    if len(arr) == 5:
        timestamp = 0
        remember = "0"
        uid = 0
        some_state = 0
        hash = ''
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
            remember = str(int(arr[1]))
        except Exception as ex:
            remember = "0"

        try:
            some_state = int(arr[3])
        except Exception as ex:
            some_state = 0

        hash = arr[4]
        # TODO SQL request to database for login and password with selected uid

        hash2 = hashlib.md5(
            (str(timestamp) + str(some_state) + login + remember + str(uid) + passwd + 'WASSUP!').encode(
                'utf-8')).hexdigest()
        if hash == hash2:
            user_id = uid
            user_login = login
            user_password = passwd
            user_remember = remember
            user_some_state = some_state
            return True
    else:
        return False
    return False


def credentialsHeader():
    return "Set-Cookie: credentials=" + credentials + "; path=/; HttpOnly; SameSite=Strict"


# -------- run part -------
# -------- run part -------
# -------- run part -------

req_cookie = http.cookies.SimpleCookie(os.environ.get("HTTP_COOKIE"))
req_ip = (os.environ.get("REMOTE_ADDR") or "").strip()[:20]
req_method = (os.environ.get("REQUEST_METHOD") or "").strip()[:10]
req_agent = (os.environ.get("HTTP_USER_AGENT") or "").strip()[:50]
req_language = (os.environ.get("HTTP_ACCEPT_LANGUAGE") or "").strip()[:20]
req_scheme = (os.environ.get("REQUEST_SCHEME") or "").strip()[:5]  # http or https
req_query = (os.environ.get("QUERY_STRING") or "").strip()[:350]  # parameters

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

user_role = "guest"
access_levels = 0
user_id = 0
user_login = ''
user_password = ''
user_remember = 0
user_some_state = 0
if credentials is None:
    access_levels = 0
    credentials = buildCredentials(0, '', '', False, 0)
else:
    credentials = str(credentials).strip()[:150]
    if checkCredentials(credentials.split('_', 7)):
        credentials = buildCredentials(user_id, user_login, user_password, user_remember == 1, user_some_state)
        user_password = ''  # reset MD5 hashed password from global variable
    else:
        access_levels = 0
        credentials = buildCredentials(0, '', '', False, 0)

user_password = ''  # reset MD5 hashed password from global variable
req_rawpost = ""
req_jsonpost = None
contentid = 0
typeid = 0
detailid = 0
req_params = None

# TODO check access levels before any other actions - DONE!
if access_levels != 0:
    if req_method == "POST":
        req_rawpost = sys.stdin.read()
    try:
        req_jsonpost = json.loads(req_rawpost)
    except Exception as ex:
        req_jsonpost = None

req_params = cgi.FieldStorage()
contentid = 0
typeid = 0
detailid = 0

if "contentid" in req_params and not (req_params["contentid"] is None):
    try:
        contentid = int(req_params["contentid"])
    except Exception as ex:
        contentid = 0

if "typeid" in req_params and not (req_params["typeid"] is None):
    try:
        typeid = int(req_params["typeid"])
    except Exception as ex:
        typeid = 0

if "detailid" in req_params and not (req_params["detailid"] is None):
    try:
        detailid = int(req_params["detailid"])
    except Exception as ex:
        detailid = 0
