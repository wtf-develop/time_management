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

headers.jsonAPI()
data = {}
data['daily'] = []
for i in range(55):
    obj = {'title': 'daily' +
           str(i), 'desc': 'example description for element',
           'hour': 8 + (i * 2),
           'minute': 26 + i}
    data['daily'].append(obj)

data['timers'] = []
for i in range(55):
    obj = {'title': 'timers' +
           str(i), 'desc': 'example description for element',
           'hour': 8 + (i * 2),
           'minute': 26 + i}
    data['timers'].append(obj)
headers.goodResponse(data)
