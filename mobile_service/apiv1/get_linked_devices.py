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
in_bool = True
if ('share' in auth._GET):
    in_bool = False
links = db.getUserLinkedDevices(user_id=auth.user_id, devid=auth.user_some_state, incomming=in_bool, outgoing=True,
                                cache=False)
own = db.getUserOwnDevices(user_id=auth.user_id, devid=auth.user_some_state, cache=False)  # except myself
result = {'own': [], 'in': [], 'out': []}
def_id = db.getDefaultDevice(auth.user_id)
for dev in own['all']:
    if (dev['id'] == def_id) or (dev['id'] == auth.user_id):
        continue
    result['own'].append({'id': dev['id'], 'device': dev['name']})

for key in links['in']['all']:
    dev = links['in']['all'][key]
    result['in'].append({'id': dev, 'device': links['names'][dev]['device'], 'user': links['names'][dev]['user']})

for key in links['out']['all']:
    dev = links['out']['all'][key]
    result['out'].append({'id': dev, 'device': links['names'][dev]['device'], 'user': links['names'][dev]['user']})

if len(result['out']) < 1 and len(result['in']) < 1 and len(result['own']) < 1:
    headers.errorResponse('No devices available.\nInvite new devices on settings page')
headers.goodResponse(result)
