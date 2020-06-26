#!/usr/local/bin/python3
import inspect
import os
import sys

currentdir = os.path.dirname(os.path.abspath(
        inspect.getfile(inspect.currentframe())))
sys.path.insert(0, os.path.dirname(os.path.dirname(currentdir)))
from _common.api._settings import mydb
from _common.api import auth
from _common.api import headers
from _common.api import utils
from _common.api import translation

headers.jsonAPI()

sql = 'delete from tasks where devid in (select id from devices where uid=' + str(auth.user_id) + ')'
try:
    mydb.execute(sql)
except Exception as ex:
    utils.log(utils.clearUserLogin(str(ex)), 'error', 'sql')
    headers.errorResponse('Can not remove tasks')

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
headers.goodResponse({'status': True}, translation.getValue('remove_account_message'))
