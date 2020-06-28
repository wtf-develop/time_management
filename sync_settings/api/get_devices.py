#!/usr/local/bin/python3
# this script it's a small Hell. Live is hard...
import inspect
import os
import sys

currentdir = os.path.dirname(os.path.abspath(
        inspect.getfile(inspect.currentframe())))
sys.path.insert(0, os.path.dirname(os.path.dirname(currentdir)))
from _common.api.auth import safeGETint
from _common.api import headers
from _common.api import db
from _common.api import auth

headers.jsonAPI()

filter0 = safeGETint('filter0') == 1
filter1 = safeGETint('filter1') == 1
filter2 = safeGETint('filter2') == 1
filter3 = safeGETint('filter3') == 1
filterl = safeGETint('filterl') == 1
selected = safeGETint('selected')

# if filter0 and filter1 and filter2 and filter3 and filterl:
#    filterl = False
nodes = {}
edges = {}
own = db.getUserOwnDevices(user_id=auth.user_id)
our_device_selected = False
for value in own['all']:
    if selected == value['id']:
        our_device_selected = True
        break
if(our_device_selected):
    own = db.getUserOwnDevices(user_id=auth.user_id, devid=selected, myself=True, cache=True)
linked = db.getUserLinkedDevices(auth.user_id, 0, True)
linksIn = linked['in']['link'].copy()
linksOut = linked['out']['link'].copy()

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

if (selected > 0) and replace_default and our_device_selected:
    selLinks = []
    for row in own['all']:
        if row['id'] == selected:
            obj = {}
            obj['id'] = row['id']
            obj['device'] = row['name']
            obj['sync0'] = row['sync0']
            obj['sync1'] = row['sync1']
            obj['sync2'] = row['sync2']
            obj['sync3'] = row['sync3']
            selLinks.append(obj)
            break

    for row in linksIn:
        if (row['src'] == selected):
            obj = {}
            obj['id'] = row['src']
            obj['dst'] = row['dst']
            obj['device'] = linked['names'][row['dst']]['device']
            obj['user'] = linked['names'][row['dst']]['user']
            obj['sync0'] = row['sync0']
            obj['sync1'] = row['sync1']
            obj['sync2'] = row['sync2']
            obj['sync3'] = row['sync3']
            selLinks.append(obj)

    for row in linksOut:
        if (row['src'] == selected):
            obj = {}
            obj['id'] = row['src']
            obj['dst'] = row['dst']
            obj['device'] = linked['names'][row['dst']]['device']
            obj['user'] = linked['names'][row['dst']]['user']
            obj['sync0'] = row['sync0']
            obj['sync1'] = row['sync1']
            obj['sync2'] = row['sync2']
            obj['sync3'] = row['sync3']
            selLinks.append(obj)
    headers.goodResponse({'nodes': nodes, 'edges': edges, 'links': selLinks})

if (selected > 0) and not our_device_selected:
    selLinks = []
    for row in linksIn:
        if (row['dst'] == selected):
            if (row['src'] in own['names']):
                obj = {}
                obj['id'] = row['src']
                obj['dst'] = row['dst']
                obj['device'] = own['names'][row['src']]
                obj['sync0'] = row['sync0']
                obj['sync1'] = row['sync1']
                obj['sync2'] = row['sync2']
                obj['sync3'] = row['sync3']
                selLinks.append(obj)

    for row in linksOut:
        if (row['dst'] == selected):
            if (row['src'] in own['names']):
                obj = {}
                obj['id'] = row['src']
                obj['dst'] = row['dst']
                obj['device'] = own['names'][row['src']]
                obj['sync0'] = row['sync0']
                obj['sync1'] = row['sync1']
                obj['sync2'] = row['sync2']
                obj['sync3'] = row['sync3']
                selLinks.append(obj)
    headers.goodResponse({'nodes': nodes, 'edges': edges, 'links': selLinks})

headers.goodResponse({'nodes': nodes, 'edges': edges, 'links': []})
