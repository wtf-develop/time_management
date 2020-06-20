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
ext_links = db.getUserLinkedDevices(auth.user_id)
ext_link_names = ext_links['names']
ext_link_ids = ext_links['all']
linked_devices = []
for key in ext_link_ids:
    obj = {'id': ext_link_ids[key],
           'name': ext_link_names[ext_link_ids[key]]['device'].title(),
           'user': (ext_link_names[ext_link_ids[key]]['user'] or '').title()
           }
    linked_devices.append(obj)
own_devices = db.getUserOwnDevices(auth.user_id)
headers.goodResponse({'login': auth.user_login,
                      'some_state': auth.user_some_state,
                      'all_devices': [{'id': 0, 'name': '@str.all_devices'}],
                      'own_devices': own_devices['all'],
                      'linked_devices': linked_devices
                      })
