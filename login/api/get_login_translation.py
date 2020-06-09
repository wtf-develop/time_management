#!/usr/local/bin/python3

import os
import sys
import inspect
currentdir = os.path.dirname(os.path.abspath(
    inspect.getfile(inspect.currentframe())))
sys.path.insert(0, os.path.dirname(os.path.dirname(currentdir)))
from _common.api import translation
from _common.api import headers
from _common.api import auth

headers.jsonAPI(False)


print(translation.get_array_with_code(auth.user_lang))
