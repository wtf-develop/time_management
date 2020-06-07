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

headers.jsonAPI()
data = {
    "nodes": {
        "a": {
            "id": 123,
            "name": "Xiaomi",
            "own": True,
            "selected": True
        },
        "c": {
            "name": "Philips",
            "own": False,
            "user": "Ivanuschka"
        },
        "b": {
            "name": "Samsung",
            "own": True
        },
        "e": {},
        "d": {},
        "g": {},
        "f": {},
        "i": {},
        "h": {},
        "k": {},
        "j": {},
        "x": {}
    },
    "edges": {
        "a": {
            "c": {},
            "b": {},
            "e": {},
            "f": {},
            "i": {},
            "x": {}
        },
        "c": {
            "a": {},
            "d": {}
        },
        "b": {
            "i": {},
            "a": {},
            "k": {},
            "j": {}
        },
        "e": {
            "a": {},
            "h": {},
            "x": {},
            "d": {},
            "f": {}
        },
        "d": {
            "c": {},
            "e": {}
        },
        "g": {
            "i": {},
            "h": {}
        },
        "f": {
            "a": {},
            "e": {}
        },
        "i": {
            "a": {},
            "x": {},
            "k": {},
            "j": {},
            "g": {}
        },
        "h": {
            "e": {},
            "g": {}
        },
        "j": {
            "i": {},
            "x": {}
        }
    }
}

headers.goodResponse(data)
