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
removed = 0
if ('remove' in auth._GET) and not (auth._GET['remove'] is None):
    removed = int(auth._GET['remove'])
if removed < 1:
    headers.errorResponse('Bad request')

def_id = db.getDefaultDevice(auth.user_id)
if (removed == auth.user_id) or (removed == def_id):
    headers.errorResponse('You can not remove this device from list')
