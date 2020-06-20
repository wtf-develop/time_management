#!/usr/local/bin/python3

import inspect
import os
import sys

currentdir = os.path.dirname(os.path.abspath(
        inspect.getfile(inspect.currentframe())))
sys.path.insert(0, os.path.dirname(os.path.dirname(currentdir)))
from _common.api import headers

headers.jsonAPI()
data = {
    "nodes": {
        "a": {
            "id": 123,
            "name": "XiaoMi".title(),
            "own": True,
            "selected": False
        },
        "c": {
            "name": "Philips".title(),
            "own": False,
            "user": "Семафорович"
        },
        "b": {
            "name": "samSung".title(),
            "own": True
        },
        "e": {"name": "Mein Handy".title(),
              "default": True
              },
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
