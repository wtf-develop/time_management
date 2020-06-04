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
print("""{
"time":""" + str(time.time() * 1000) + """,
"daily":[
{"title":"task1", "desc":"Description text with many simbols", "device":"Xiaomi", "type":1, "alarm_type":0,"start_time":""" + str((time.time() + 1000) * 1000) + """, "timezone":10000,"hour":14,"minute":37},
{"title":"task1", "desc":"Description text with many simbols", "device":"Xiaomi", "type":1, "alarm_type":0,"start_time":""" + str((time.time() + 800) * 1000) + """, "timezone":10000,"hour":14,"minute":17},
{"title":"task1", "desc":"Description text with many simbols", "device":"Xiaomi", "type":1, "alarm_type":1,"start_time":""" + str((time.time() + 1400) * 1000) + """, "timezone":10000,"hour":14,"minute":57}
],
"timers":[
{"title":"task1", "desc":"Description text with many simbols", "device":"Xiaomi", "type":0, "alarm_type":1,"start_time":""" + str((time.time() + 1000) * 1000) + """, "timezone":10000,"hour":14,"minute":37},
{"title":"task1", "desc":"Description text with many simbols", "device":"Xiaomi", "type":0, "alarm_type":2,"start_time":""" + str((time.time() + 800) * 1000) + """, "timezone":10000,"hour":14,"minute":49},
{"title":"task1", "desc":"Description text with many simbols", "device":"Xiaomi", "type":0, "alarm_type":0,"start_time":""" + str((time.time() + 1400) * 1000) + """, "timezone":10000,"hour":14,"minute":17},
{"title":"task1", "desc":"Description text with many simbols", "device":"Xiaomi", "type":0, "alarm_type":1,"start_time":""" + str((time.time() + 1000) * 1000) + """, "timezone":10000,"hour":14,"minute":37},
{"title":"task1", "desc":"Description text with many simbols", "device":"Xiaomi", "type":0, "alarm_type":2,"start_time":""" + str((time.time() + 800) * 1000) + """, "timezone":10000,"hour":14,"minute":49},
{"title":"task1", "desc":"Description text with many simbols", "device":"Xiaomi", "type":0, "alarm_type":0,"start_time":""" + str((time.time() + 1400) * 1000) + """, "timezone":10000,"hour":14,"minute":17}

]
}""")
