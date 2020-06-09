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


headers.jsonAPI()

print(json.dumps({'time': time.time(), 'login': auth.user_login,
                  'some_state': auth.user_some_state}))
