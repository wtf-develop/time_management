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
from mobile_service.apiv1 import functions as func

headers.jsonAPI()
if not(auth.isMobile):  # check that this request from mobile application
    headers.errorResponse('Wrong type')

devid = auth.user_some_state
if(auth._POST is None):  # only POST accepted
    headers.errorResponse('Wrong information')
json = auth._POST
if 'data' not in json:
    headers.errorResponse('Nothing was sent')
data = json['data']
mobile_crc = json['crc32']
if len(data) > 0:
    for task in data:
        db.saveTask(task)

# After updating we check CRC32 values,
# if they are different - need to check
server_crc = utils.crc32(func.getTotalIdsString(
    auth.user_id, auth.user_some_state, auth.user_ch0, auth.user_ch1, auth.user_ch2, auth.user_ch3))
