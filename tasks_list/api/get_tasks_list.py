#!/usr/local/bin/python3

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

headers.jsonAPI()

arrdata = []
for i in range(10):
    obj = {'title': 'daily' +
           str(i), 'desc': 'example description for element',
           'hour': 8 + (i * 2),
           'minute': 26 + i}
    arrdata.append(obj)


panels = {'panels': [{
    'state': 0,
    "id": "inreview",
    'bg_class': 'bg-light',
    'pname': '@str.inreview',
    'items': arrdata
},
    {
        'state': 10,
        "id": "approved",
        'bg_class': 'bg-light',
        'pname': '@str.approved',
        'items': arrdata
},
    {
        'state': 20,
        "id": "inprogress",
        'bg_class': 'bg-light',
        'pname': '@str.inprogress',
        'items': arrdata
},
    {
        'state': 30,
        "id": "completed",
        'bg_class': 'bg-light',
        'pname': '@str.completed',
        'items': arrdata
},
    {
        'state': 40,
        "id": "canceled",
        'bg_class': 'bg-light',
        'pname': '@str.canceled',
        'items': arrdata
},
    {
        'state': 50,
        "id": "archived",
        'bg_class': 'bg-light',
        'pname': '@str.archived',
        'items': []
}
]}
headers.goodResponse(panels)
