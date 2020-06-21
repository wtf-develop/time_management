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
from mobile_service.apiv1.mobile import sql_request

headers.jsonAPI()

jsonpost = auth._POST
if (jsonpost is None) or ('invite' not in jsonpost):
    headers.errorResponse('Bad request')
invite = utils.clearStringHard(str(jsonpost['invite']))[:7]
if len(invite) < 3:
    headers.errorResponse('Too short invite')
sql_request('select id from sync_devices where ((dst=' + str(auth.user_some_state) + ') or (`default`=1)) and invite="' + invite+'"')
row = mydb.fetchone()
id = 0
if row is None:
    headers.errorResponse('Not found')
id = int(row['id'])
if id < 1:
    headers.errorResponse('Not found')

sql_request('update sync_devices set invite="", state=1 where id=' + str(id))
headers.goodResponse({'state': True})
