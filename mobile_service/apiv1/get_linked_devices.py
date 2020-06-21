#!/usr/local/bin/python3
import inspect
import os
import sys

currentdir = os.path.dirname(os.path.abspath(
        inspect.getfile(inspect.currentframe())))
sys.path.insert(0, os.path.dirname(os.path.dirname(currentdir)))
from _common.api import auth
from _common.api import headers
from _common.api import db

headers.jsonAPI()
links = db.getUserLinkedDevices(user_id=auth.user_id, devid=auth.user_some_state, incomming=True, outgoing=True,
                                cache=True)
own = db.getUserOwnDevices(user_id=auth.user_id, devid=auth.user_some_state, cache=False)  # except myself
result = {'own': [], 'in': [], 'out': []}

for dev in own['all']:
    result['own'].append({'id': dev['id'], 'device': dev['name']})

for key in links['in']['all']:
    dev = links['in']['all'][key]
    result['in'].append({'id': dev, 'device': links['names'][dev]['device'], 'user': links['names'][dev]['user']})

for key in links['out']['all']:
    dev = links['in']['all'][key]
    result['out'].append({'id': dev, 'device': links['names'][dev]['device'], 'user': links['names'][dev]['user']})

headers.goodResponse(result)
