#!/usr/local/bin/python3
import inspect
import os
import sys

currentdir = os.path.dirname(os.path.abspath(
        inspect.getfile(inspect.currentframe())))
sys.path.insert(0, os.path.dirname(os.path.dirname(currentdir)))
from _common.api.auth import _GET
from _common.api import headers
from _common.api import db
from _common.api import auth

headers.jsonAPI()

devid = 0

if not (_GET is None) and ('devid' in _GET) and not (_GET['devid'] is None) and not (_GET['devid'][0] is None):
    devid = int(_GET['devid'][0])

nodes = {}
edges={}
own = db.getUserOwnDevices(auth.user_id, devid, True)
linked = db.getUserLinkedDevices(auth.user_id, devid, True)
for value in own['all']:
    nodes[str(value['id'])] = {'id': value['id'],
                               'name': value['name'],
                               'default': (value['default'] != 0),
                               'own': True}

for key in linked['all']:
    value = linked['all'][key]
    name_obj = linked['names'][key]
    nodes[str(value)] = {'id': value,
                         'name': name_obj[value]['device'],
                         'user': name_obj[value]['user'],
                         'own': False}

headers.goodResponse({'nodes': nodes,'edges':edges})

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
