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
from _common.api import translation

headers.jsonAPI()

sql = 'delete from tasks where devid in (select id from devices where uid=' + str(auth.user_id) + ')'
try:
    mydb.execute(sql)
except Exception as ex:
    utils.log(utils.clearUserLogin(str(ex)), 'error', 'sql')
    headers.errorResponse('Can not remove tasks')

sql = 'delete from tasks_tags where tagid in (select id from tags where uid=' + str(auth.user_id) + ')'
try:
    mydb.execute(sql)
except Exception as ex:
    utils.log(utils.clearUserLogin(str(ex)), 'error', 'sql')
    headers.errorResponse('Can not remove tags link')

sql = 'delete from tags where uid=' + str(auth.user_id) + ''
try:
    mydb.execute(sql)
except Exception as ex:
    utils.log(utils.clearUserLogin(str(ex)), 'error', 'sql')
    headers.errorResponse('Can not remove tags')

sql = 'delete from sync_devices where src in (select id from devices where uid=' + str(auth.user_id) + ')'
try:
    mydb.execute(sql)
except Exception as ex:
    utils.log(utils.clearUserLogin(str(ex)), 'error', 'sql')
    headers.errorResponse('Can not remove source sync devices')

sql = 'delete from sync_devices where dst in (select id from devices where uid=' + str(auth.user_id) + ')'
try:
    mydb.execute(sql)
except Exception as ex:
    utils.log(utils.clearUserLogin(str(ex)), 'error', 'sql')
    headers.errorResponse('Can not remove dest sync devices')

sql = 'delete from sync_tasks where dst in (select id from devices where uid=' + str(auth.user_id) + ')'
try:
    mydb.execute(sql)
except Exception as ex:
    utils.log(utils.clearUserLogin(str(ex)), 'error', 'sql')
    headers.errorResponse('Can not remove tasks sync links')

sql = 'delete from devices where uid=' + str(auth.user_id) + ''
try:
    mydb.execute(sql)
except Exception as ex:
    utils.log(utils.clearUserLogin(str(ex)), 'error', 'sql')
    headers.errorResponse('Can not remove devices')

sql = 'delete from users where id=' + str(auth.user_id) + ''
try:
    mydb.execute(sql)
except Exception as ex:
    utils.log(utils.clearUserLogin(str(ex)), 'error', 'sql')
    headers.errorResponse('Can not remove user account')
headers.goodResponse({'status': True, 'message': translation.getValue('remove_account_message')})
