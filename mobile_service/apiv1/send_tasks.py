#!/usr/local/bin/python3
import os
import sys
import inspect
import json
import time

currentdir = os.path.dirname(os.path.abspath(
        inspect.getfile(inspect.currentframe())))
sys.path.insert(0, os.path.dirname(os.path.dirname(currentdir)))
from _common.api._settings import mydb, mydb_connection
from _common.api import auth
from _common.api import headers
from _common.api import utils
from _common.api import db
from mobile_service.apiv1 import mobile

headers.jsonAPI()
mobile.clearPermissionSQLCache()
devid = auth.user_some_state
if (auth._POST is None):  # only POST accepted
    mobile.elog('No posted info uid:' + auth.user_id)
    headers.errorResponse('Wrong information')
json = auth._POST
if 'tasks' not in json:
    mobile.elog('Incorrect info format uid:' + auth.user_id)
    headers.errorResponse('Nothing was sent')
tasks = json['tasks']

mobile_crc32 = json['sync_info']['crc32']
mobile_time = json['sync_info']['time']
mobile_serial = json['sync_info']['serial']
mobile_count = json['sync_info']['count']
saved_ids = []
broken_ids = []
remove_ids = []
# headers.errorResponse('error n-' + str(len(data)))
counter = 0
if len(tasks) > 0:
    obj = mobile.getTotalIdsString(user_id=auth.user_id, devid=auth.user_some_state, extendType=0)
    set_ids = set(obj['info']['ids'].split(','))
    remove_objects = []
    # create list of all existing (not new) global ids
    # and remove tasks that out of user access
    for task in tasks:
        if ('globalid' in task) and (not (task['globalid'] is None)) and len(task['globalid']) > 5:
            if not (task['globalid'] in set_ids):  # check that its not exists in access area
                task['id'] = db.getIdFromGlobal(task['globalid'])
                if task['id'] > 0:  # check that this id exists in DB
                    remove_ids.append(task['globalid'])  # if so - remove this from mobile
                    remove_objects.append(task)  # and remove from tasks

    for toremove in remove_objects:
        tasks.remove(toremove)

    for task in tasks:
        task['devid'] = auth.user_some_state
        # headers.errorResponse(str(task))
        save_result = db.saveTask(task)
        counter = counter + 1
        if (save_result > 0):
            saved_ids.append(task['globalid'])
        else:
            broken_ids.append(task['globalid'])

# After updating we check db values and CRC32,
# if they are different - need to check
obj = mobile.getTotalIdsString(user_id=auth.user_id, devid=auth.user_some_state, extendType=2)
if obj is None:
    headers.errorResponse('SQL error')
if (mobile_time != obj['time'] or (mobile_serial != obj['serial']) or
        (mobile_count != obj['count']) or (mobile_crc32 != utils.crc32(obj['info']['ids']))):
    headers.goodResponse({
        'saved': {'state': True,
                  'ids': ','.join(saved_ids),
                  'broken': ','.join(broken_ids),
                  'remove': ','.join(remove_ids),
                  },
        'diff': {'state': True,
                 'info': obj['info']
                 }
    })
else:
    headers.goodResponse({'saved': {'state': True,
                                    'ids': ','.join(saved_ids),
                                    'broken': ','.join(broken_ids),
                                    'remove': ','.join(remove_ids),
                                    },
                          'diff': {'state': False}
                          })
