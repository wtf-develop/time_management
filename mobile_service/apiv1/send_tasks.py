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
if not (auth.isMobile):  # check that this request from mobile application
    mobile.elog('Only from mobile uid:' + auth.user_id)
    headers.errorResponse('Wrong type')

devid = auth.user_some_state
if (auth._POST is None):  # only POST accepted
    mobile.elog('No posted info uid:' + auth.user_id)
    headers.errorResponse('Wrong information')
json = auth._POST
if 'data' not in json:
    mobile.elog('Incorrect info format uid:' + auth.user_id)
    headers.errorResponse('Nothing was sent')
data = json['data']

mobile_crc32 = json['sync_info']['crc32']
mobile_time = json['sync_info']['time']
mobile_serial = json['sync_info']['serial']
saved_ids = []
broken_ids = []
# headers.errorResponse('error n-' + str(len(data)))
counter = 0
if len(data) > 0:
    # headers.errorResponse('error n-' + str(len(data)))
    for task in data:
        task['devid'] = auth.user_some_state
        # headers.errorResponse(str(task))
        save_result = db.saveTask(task)
        counter = counter + 1
        if (save_result > 0):
            saved_ids.append(task['globalid'])
        else:
            broken_ids.append(task['globalid'])

# After updating we check CRC32 values,
# if they are different - need to check
obj = mobile.getTotalIdsString(auth.user_id, auth.user_some_state)
obj['crc32'] = utils.crc32(obj['val'])
obj2 = {'crc32': obj['crc32'], 'time': obj['time'], 'serial': obj['serial']}
if (mobile_crc32 != obj['crc32']) or (mobile_time != obj['time'] or (mobile_serial != obj['serial'])):
    headers.goodResponse({
        'mobile': json['sync_info'],
        'srv': obj2,
        'saved': {'state': True,
                  'ids': ','.join(saved_ids),
                  'broken': ','.join(broken_ids),
                  },
        'diff': {'state': True,
                 'ids': obj['val']
                 }
    })
else:
    headers.goodResponse({'saved': {'state': True,
                                    'ids': ','.join(saved_ids)
                                    },
                          'diff': {'state': False}
                          })
