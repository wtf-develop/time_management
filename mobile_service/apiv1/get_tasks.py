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

devid = auth.user_some_state
if (auth._POST is None):  # only POST accepted
    mobile.elog('No posted info uid:' + auth.user_id)
    headers.errorResponse('Wrong information')
json = auth._POST
if 'tasks' not in json:
    mobile.elog('Incorrect tasks uid:' + auth.user_id)
    headers.errorResponse('Nothing was sent')
tasks = json['tasks']

obj = mobile.getTotalIdsString(user_id=auth.user_id, devid=auth.user_some_state, cross=tasks, extend=True)
if obj is None:
    headers.errorResponse('SQL error')
headers.goodResponse(obj)
