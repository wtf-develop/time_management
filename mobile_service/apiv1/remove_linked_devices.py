#!/usr/local/bin/python3
import inspect
import os
import sys

currentdir = os.path.dirname(os.path.abspath(
        inspect.getfile(inspect.currentframe())))
sys.path.insert(0, os.path.dirname(os.path.dirname(currentdir)))
from _common.api import auth
from _common.api import headers
from _common.api import db
from _common.api import utils
from _common.api import translation
from mobile_service.apiv1._mobile import sql_request

headers.jsonAPI()
if (auth._POST is None):
    headers.errorResponse("Bad request")
out = ''
incom = ''
your = ''
if ('out' in auth._POST) and not (auth._POST['out'] is None):
    out = utils.clearStringHard(auth._POST['out'])
if ('in' in auth._POST) and not (auth._POST['in'] is None):
    incom = utils.clearStringHard(auth._POST['in'])
if ('your' in auth._POST) and not (auth._POST['your'] is None):
    your = utils.clearStringHard(auth._POST['your'])
out_arr = {}
in_arr = {}
your_arr = {}
if len(out) > 0:
    out_arr = set(str(int(x)) for x in out.split(','))
if len(incom) > 0:
    in_arr = set(str(int(x)) for x in incom.split(','))
if len(your) > 0:
    your_arr = set(str(int(x)) for x in your.split(','))

def_id = db.getDefaultDevice(auth.user_id)

if len(your_arr) < 1 and len(out_arr) < 1 and len(in_arr) < 1:
    headers.errorResponse(
            "Nothing to do")

if str(auth.user_id) in your_arr:
    your_arr.remove(str(auth.user_id))

if str(def_id) in your_arr:
    your_arr.remove(str(def_id))
if len(your_arr) < 1 and len(out_arr) < 1 and len(in_arr) < 1:
    headers.errorResponse(
            "You can not remove current and default devices.\nBut you can erase your account from server")

if len(out_arr) > 0:
    req_filter = ",".join(list(out_arr))
    sql_request(
            "delete from sync_devices where src=" + str(auth.user_some_state) + " and dst in (" + req_filter + ")")
    sql_request("""delete sync_tasks from sync_tasks 
             inner join tasks as t on t.id=sync_tasks.tid and t.devid=""" + str(auth.user_some_state) + """
             where sync_tasks.dst in (""" + req_filter + ")")

if len(in_arr) > 0:
    req_filter = ",".join(list(in_arr))
    sql_request(
            "delete from sync_devices where dst=" + str(auth.user_some_state) + " and src in (" + req_filter + ")")
    sql_request("""delete sync_tasks from sync_tasks 
             inner join tasks as t on t.id=sync_tasks.tid and t.devid in (""" + req_filter + """) 
             where sync_tasks.dst in (""" + str(auth.user_some_state) + ")")

if len(your_arr) > 0:
    req_filter = ",".join(list(your_arr))
    sql_request(
            "update tasks set devid=" + str(auth.user_some_state) + " where devid in (" + req_filter + ") and devid in (select id from devices where uid=" + str(auth.user_id) + ")")
    sql_request(
            "delete from devices where id in (" + req_filter + ") and id in (select id from devices where uid=" + str(auth.user_id) + ")")

headers.goodResponse({'status': True},translation.getValue('device_link_removed'))
