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
from mobile_service.apiv1 import functions as func

headers.jsonAPI()
if not(auth.isMobile):  # check that this request from mobile application
    headers.errorResponse('Wrong type')
if(auth._POST is None):  # only POST accepted
    headers.errorResponse('Wrong information')
json = auth._POST
if 'data' not in json:
    headers.errorResponse('Nothing was sent')
data = json['data']
crc = json['crc32']
for task in data:
    nope
