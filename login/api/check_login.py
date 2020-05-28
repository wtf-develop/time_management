#!/usr/local/Cellar/python/3.7.7/Frameworks/Python.framework/Versions/3.7/bin/python3
# !/usr/bin/env python3
import os, sys, inspect, cgitb

cgitb.enable()
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
sys.path.insert(0, os.path.dirname(os.path.dirname(currentdir)))  # one level up "os.path.dirname()"

from _common.api import auth
from _common.api import headers

headers.jsonAPI(False)

print("""
{
    "error":{
        "state":true,
        "title": "----- Error object -----",
        "message":"This is example error object for library\nYou can use anythig else or extend existing,\nbut this object fields a must be processed",
        "code":777
    }
}
""")
