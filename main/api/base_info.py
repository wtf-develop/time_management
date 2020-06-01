#!/usr/local/Cellar/python/3.7.7/Frameworks/Python.framework/Versions/3.7/bin/python3
# !/usr/bin/env python3
import os, sys, inspect, json, time
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
sys.path.insert(0, os.path.dirname(os.path.dirname(currentdir)))  # one level up "os.path.dirname()"
from _common.api import auth
from _common.api import headers


headers.jsonAPI(True)

print(json.dumps({'time': time.time(), 'login': auth.user_login}))