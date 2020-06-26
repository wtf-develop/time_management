#!/usr/local/bin/python3
# this script it's a small Hell
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

filter0 = False
filter1 = False
filter2 = False
filter3 = False
filterl = False
selected = 0
if (_GET is not None) and ('devid' in _GET) and (_GET['devid'] is not None) and (_GET['devid'][0] is not None):
    devid = int(_GET['devid'][0])

if (_GET is not None) and ('filter0' in _GET) and (_GET['filter0'] is not None) and (_GET['filter0'][0] is not None):
    filter0 = int(_GET['filter0'][0]) == 1
if (_GET is not None) and ('filter1' in _GET) and (_GET['filter1'] is not None) and (_GET['filter1'][0] is not None):
    filter1 = int(_GET['filter1'][0]) == 1
if (_GET is not None) and ('filter2' in _GET) and (_GET['filter2'] is not None) and (_GET['filter2'][0] is not None):
    filter2 = int(_GET['filter2'][0]) == 1
if (_GET is not None) and ('filter3' in _GET) and (_GET['filter3'] is not None) and (_GET['filter3'][0] is not None):
    filter3 = int(_GET['filter3'][0]) == 1
if (_GET is not None) and ('filterl' in _GET) and (_GET['filterl'] is not None) and (_GET['filterl'][0] is not None):
    filterl = int(_GET['filterl'][0]) == 1
if (_GET is not None) and ('selected' in _GET) and (_GET['selected'] is not None) and (_GET['selected'][0] is not None):
    selected = int(_GET['selected'][0])

# if filter0 and filter1 and filter2 and filter3 and filterl:
#    filterl = False
nodes = {}
edges = {}
own = db.getUserOwnDevices(auth.user_id, 0, True)
linked = db.getUserLinkedDevices(auth.user_id, 0, True)

if filter0:
    own['0'] = []
    linked['in']['0'] = []
    linked['out']['0'] = []
if filter1:
    own['1'] = []
    linked['in']['1'] = []
    linked['out']['1'] = []
if filter2:
    own['2'] = []
    linked['in']['2'] = []
    linked['out']['2'] = []
if filter3:
    own['3'] = []
    linked['in']['3'] = []
    linked['out']['3'] = []
if filterl:
    own['link'] = []
    linked['in']['link'] = []
    linked['out']['link'] = []

default_id = '0'
replace_default = False
our_device_selected=False
for value in own['all']:
    if selected == value['id']:
        our_device_selected=True
        break

for value in own['all']:
    isDef = ('default' in value) and (int(value['default']) == 1)
    if (isDef):
        default_id = str(value['id'])
    node_selected = (selected == value['id'])
    if our_device_selected:
        if isDef:
            if not node_selected:
                replace_default = True
                continue
    nodes[str(value['id'])] = {'id': value['id'],
                               'name': str(value['name']).title(),
                               'default': isDef,
                               'selected': node_selected,
                               'own': True}

for key in linked['all']:
    value = linked['all'][key]
    name_obj = linked['names'][value]
    node_selected = (selected == value)
    nodes[str(value)] = {'id': value,
                         'name': str(name_obj['device']).title(),
                         'user': str(name_obj['user']).title(),
                         'selected': node_selected,
                         'own': False}

removeId = '0'
if replace_default:
    removeId = str(default_id)
    default_id = str(selected)
for k in range(5):
    obj_key = str(k)
    if k == 4:
        obj_key = 'link'
    for obj in own[obj_key]:
        if default_id == str(obj):
            continue
        if (removeId == str(obj)):
            continue
        if default_id not in edges:
            edges[default_id] = {}
        if str(obj) not in edges[default_id]:
            edges[default_id][str(obj)] = {}
        if str(obj) not in edges:
            edges[str(obj)] = {}
        if default_id not in edges[str(obj)]:
            edges[str(obj)][default_id] = {}

for k in range(5):
    obj_key = str(k)
    if k == 4:
        obj_key = 'link'
    for obj in linked['in'][obj_key]:
        src = str(obj['src'])
        dst = str(obj['dst'])
        if src == dst:
            continue
        if src not in edges:
            edges[src] = {}
        if dst not in edges[src]:
            edges[src][dst] = {}

for k in range(5):
    obj_key = str(k)
    if k == 4:
        obj_key = 'link'
    for obj in linked['out'][obj_key]:
        src = str(obj['src'])
        dst = str(obj['dst'])
        if src == dst:
            continue
        if src not in edges:
            edges[src] = {}
        if dst not in edges[src]:
            edges[src][dst] = {}

headers.goodResponse({'nodes': nodes, 'edges': edges})
