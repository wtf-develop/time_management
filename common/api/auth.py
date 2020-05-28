import cgi
import os
import http.cookies
import json
import sys


req_cookie = http.cookies.SimpleCookie(os.environ.get("HTTP_COOKIE"))
req_ip = (os.environ.get("REMOTE_ADDR") or "").strip()[:20]
req_method=(os.environ.get("REQUEST_METHOD") or "").strip()[:10]
req_agent=(os.environ.get("HTTP_USER_AGENT") or "").strip()[:50]
req_language=(os.environ.get("HTTP_ACCEPT_LANGUAGE") or "").strip()[:20]
req_scheme=(os.environ.get("REQUEST_SCHEME") or "").strip()[:5] #http or https
req_query=(os.environ.get("QUERY_STRING") or "").strip()[:350] #parameters

credentials = req_cookie.get("credentials")
user_role="guest"
access_levels=0
if credentials is None:
    credentials="0"
else:
    credentials=str(credentials).strip()[:75]
#TODO check access levels before any other actions

req_rawpost=""
req_jsonpost=None
if req_method == "POST":
    req_rawpost = sys.stdin.read()
    try:
        req_jsonpost=json.loads(req_rawpost)
    except Exception as ex:
        req_jsonpost=None

req_params = cgi.FieldStorage()
contentid=0
typeid=0
detailid=0


if "contentid" in req_params and not (req_params["contentid"] is None):
    try:
        contentid=int(req_params["contentid"])
    except Exception as ex:
        contentid = 0

if "typeid" in req_params and not (req_params["typeid"] is None):
    try:
        typeid=int(req_params["typeid"])
    except Exception as ex:
        typeid = 0

if "detailid" in req_params and not (req_params["detailid"] is None):
    try:
        detailid=int(req_params["detailid"])
    except Exception as ex:
        detailid = 0



def credentialsHeader():
    return "Set-Cookie: credentials="+credentials+"; HttpOnly; SameSite=Strict"