#!/usr/local/bin/python3

import os
import sys
import inspect
import json
import time
currentdir = os.path.dirname(os.path.abspath(
    inspect.getfile(inspect.currentframe())))
sys.path.insert(0, os.path.dirname(os.path.dirname(currentdir)))
from _common.api import auth
from _common.api import headers
from _common.api._settings import mydb, mydb_connection
from _common.api import db


headers.jsonAPI()
devices = [{'id': 0, 'name': '@str.all_devices'}, {'id': 100, 'selected': 1, 'name': 'xiaOmi'.title()},
           {'id': 101, 'name': 'Samsung'.title()}, {'id': 102, 'name': 'Philips'.title()}]
headers.goodResponse({'login': auth.user_login,
                      'some_state': auth.user_some_state,
                      'all_devices': [{'id': 0, 'name': '@str.all_devices'}],
                      # incorrect need another function
                      'own_devices': db.getOwnDevices(
                          auth.user_id, auth.user_some_state,
                          auth.user_ch0, auth.user_ch1,
                          auth.user_ch2, auth.user_ch3)['all'],
                      # incorrect need another function
                      'linked_devices': db.getLinkedDevices(auth.user_some_state)['all']
                      })
