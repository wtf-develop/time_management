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
from mobile_service.apiv1._mobile import sql_request_ignore_error, getTotalIdsString, sql_request
from _common.api._settings import mydb

headers.jsonAPI()
if (auth._POST is None):
    headers.errorResponse("Bad request")
out = ''
your = ''
tasks = ''
if ('out' in auth._POST) and not (auth._POST['out'] is None):
    out = utils.clearStringHard(auth._POST['out'])
if ('your' in auth._POST) and not (auth._POST['your'] is None):
    your = utils.clearStringHard(auth._POST['your'])
if ('tasks' in auth._POST) and not (auth._POST['tasks'] is None):
    tasks = utils.clearStringHard(auth._POST['tasks'])

out_arr = []
your_arr = []
tasks_arr = []
tasks = getTotalIdsString(user_id=auth.user_id, devid=auth.user_some_state, cross=tasks, extendType=0)['info']['ids']

sql = "select group_concat(id,',') as int_tasks from tasks where globalid in ('" + "','".join(tasks.split(',')) + "')"
sql_request(sql)
tasks_row = mydb.fetchone()
if tasks_row is None:
    headers.errorResponse('Permission denied')
tasks = str(tasks_row['int_tasks']).strip(',')
if len(out) > 0:
    out_arr = list(set((int(x)) for x in out.split(',')))
if len(your) > 0:
    your_arr = list(set((int(x)) for x in your.split(',')))
if len(tasks) > 0:
    tasks_arr = list(set(str(x) for x in tasks.split(',')))

all_devices = list(set().union(out_arr, your_arr))  # integers
def_id = db.getDefaultDevice(auth.user_id)

if (len(all_devices) < 1) or len(tasks) < 1:
    headers.errorResponse(
            "Error, nothing to do")

if str(auth.user_id) in all_devices:
    all_devices.remove(str(auth.user_id))

if str(def_id) in all_devices:
    all_devices.remove(str(def_id))

if len(all_devices) < 1:
    headers.errorResponse(
            "You can't share to your current or default devices")

own_dict = db.getUserOwnDevices(user_id=auth.user_id, devid=auth.user_some_state)
out_dict = db.getUserLinkedDevices(user_id=auth.user_id, devid=auth.user_some_state, incomming=False, outgoing=True)
check_list = (set().union(list(x['id'] for x in own_dict['all']), out_dict['out']['all']))  # integers
to_remove_from = []

# check permissions
for device in all_devices:
    if not (device in check_list):
        to_remove_from.append(device)

for remover in to_remove_from:
    all_devices.remove(remover)

# tids_str = "'" + "','".join(tasks_arr) + "'"
# sql_request("delete from sync_tasks where tid in ("+tids_str+") and dst in ("++")")

sql_request_ignore_error('START TRANSACTION')
for device in all_devices:
    for task in tasks_arr:
        sql = 'insert ignore into sync_tasks (dst,tid,sender) values (' + str(device) + ',' + str(task) + ',' + str(
                auth.user_id) + ')'
        sql_request_ignore_error(sql)

sql_request_ignore_error('COMMIT')

headers.goodResponse({'status': True},translation.getValue('sharing_complete'))
