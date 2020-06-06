#!/usr/local/Cellar/python/3.7.7/Frameworks/Python.framework/Versions/3.7/bin/python3
# !/usr/bin/env python3
import os
import sys
import inspect
import json
import time
currentdir = os.path.dirname(os.path.abspath(
    inspect.getfile(inspect.currentframe())))
sys.path.insert(0, os.path.dirname(os.path.dirname(currentdir)))
from _common.api._database import mydb, mydb_connection
from _common.api import auth
from _common.api import headers
from _common.api import utils

headers.jsonAPI(True)
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
