#!/usr/local/Cellar/python/3.7.7/Frameworks/Python.framework/Versions/3.7/bin/python3
#!/usr/bin/env python3
import os,sys,inspect,cgitb
cgitb.enable()
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
sys.path.insert(0,os.path.dirname(currentdir)) #one level up "os.path.dirname()"

from _common.api import auth
from _common.api import headers



headers.htmlPage(False)

print("Login Under construction")
