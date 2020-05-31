#!/usr/local/Cellar/python/3.7.7/Frameworks/Python.framework/Versions/3.7/bin/python3
# !/usr/bin/env python3
import os, sys, inspect

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
sys.path.insert(0, os.path.dirname(os.path.dirname(currentdir)))  # two levels up "os.path.dirname()"
from _common.api import auth
from _common.api import headers
from _common.api import translation

headers.jsonAPI(False)


print(translation.get_array_with_code(auth.user_lang))

