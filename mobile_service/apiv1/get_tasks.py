#!/usr/local/bin/python3
import inspect
import os
import sys

currentdir = os.path.dirname(os.path.abspath(
        inspect.getfile(inspect.currentframe())))
sys.path.insert(0, os.path.dirname(os.path.dirname(currentdir)))
from _common.api import auth
from _common.api import headers
from mobile_service.apiv1 import _mobile

headers.jsonAPI()
_mobile.clearPermissionSQLCache()
devid = auth.user_some_state
if (auth._POST is None):  # only POST accepted
    _mobile.elog('No posted info uid:' + auth.user_id)
    headers.errorResponse('Wrong information')
json = auth._POST
if 'need_tasks' not in json:
    _mobile.elog('Incorrect tasks uid:' + auth.user_id)
    headers.errorResponse('Nothing was sent')
tasks = json['need_tasks']
if len(tasks) < 1:
    headers.errorResponse('No requested information was sent')
obj = _mobile.getTotalIdsString(user_id=auth.user_id, devid=auth.user_some_state, cross=tasks, extendType=1)
if obj is None:
    headers.errorResponse('SQL error')
headers.goodResponse(obj)
