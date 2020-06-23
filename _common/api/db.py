import random
import time

from _common.api import utils
from _common.api._settings import mydb
from _common.api._settings import mydb_connection

#
# Functions for storing data for different tables
# This functions are used in many places of project
# and changes may broke everything
#
tasks_keymap = {
    'order': 'ordr',
    'device_id': 'devid',
    'defered': 'defered_interval',
    'duration': 'duration_time',
    'start': 'start_time',
    'done': 'done_time',
    'utc': 'utc_flag',
    'isUTC': 'utc_flag'

}


# return id or 0 - error, anything < 0 is  also error
def saveTask(data: dict, uid: int) -> int:
    # do all necessary checks and convert types
    data = utils.replace_keys(data, tasks_keymap)
    required = {'devid', 'title', 'desc', 'type'}
    if not (required.issubset(data.keys())):
        return -1
    # Convert all values only to Integers and Strings.
    # Other primitive types except float - it's a big lying
    int_fields = {'id', 'devid', 'type', 'alarm_type', 'state', 'priority', 'ordr', 'start_time', 'done_time',
                  'duration_time', 'repeat_type', 'repeat_value', 'defered_interval', 'year', 'month', 'day', 'hour',
                  'minute', 'timezone', 'utc_flag', 'serial'}
    for key in data:
        value = data[key]
        if (key in int_fields):
            if not (isinstance(value, int)):
                try:
                    data[key] = int(value)
                except Exception:
                    return -2
        else:
            if not (isinstance(value, str)):
                try:
                    data[key] = str(value)
                except Exception:
                    return -3

    if (data['devid'] < 1):
        return -4

    if data['type'] == 0:  # timer
        required = {'alarm_type', 'start_time', 'repeat_type', 'repeat_value', 'defered_interval', 'year', 'month',
                    'day', 'hour', 'minute', 'timezone', 'utc_flag'}
        if not (required.issubset(data.keys())):
            return -5
    elif data['type'] == 1:  # for the whole day
        required = {'start_time', 'repeat_type', 'repeat_value', 'year', 'month', 'day', 'timezone'}
        if not (required.issubset(data.keys())):
            return -6
    elif data['type'] == 2:  # notes
        required = {'state', 'priority'}
        if not (required.issubset(data.keys())):
            return -7

    elif data['type'] == 3:  # geo based reminders
        required = {'start_time', 'repeat_type', 'repeat_value', 'locations'}
        if not (required.issubset(data.keys())):
            return -8
    else:
        return -9  # not supported task type

    timestamplong = int(time.time() * 1000)
    timestampstr = str(int(timestamplong))
    gid_generator = str(int(timestamplong) - 1592000000000)

    if ('id' not in data) or (data['id'] is None) or (data['id'] < 1):  # new record in tasks
        data['id'] = 0

    if ('globalid' not in data) or (data['globalid'] is None) or len(data['globalid']) < 5:
        data['globalid'] = ''

    if (data['id'] == 0) and len(data['globalid']) == 0:  # 1-1
        data['globalid'] = gid_generator + utils.rand_string(6) +\
                           str(data['type'] + str(data['devid']))
    elif (data['id'] != 0) and len(data['globalid']) == 0:  # 0-1
        data['globalid'] = getGlobalFromId(data['id'])
        if len(data['globalid']) == 0:
            data['globalid'] = gid_generator + utils.rand_string(6) +\
                               str(data['type'] + str(data['devid']))
    elif (data['id'] == 0) and len(data['globalid']) != 0:  # 1-0
        data['id'] = getIdFromGlobal(data['globalid'])
    elif (data['id'] != 0) and len(data['globalid']) != 0:  # 0-0
        pass  # may be check that globalid is correct with id
    else:
        return -100  # not possible

    if (data['id'] == 0) and (('created' not in data) or (data['created'] is None)):
        data['created'] = timestampstr  # dont change this later never!

    # always update time after any changes
    if ('update_time' not in data) or (data['update_time'] is None):
        data['update_time'] = timestampstr

    # always change serial after any updates ;-)
    if ('serial' not in data) or (data['serial'] is None):
        data['serial'] = random.randint(1, 50000)

    tags = str(data.pop('tags', None))
    temp_global_id = data['globalid']  # store value before unset
    temp_dev_id = data['devid']
    data['update_devid'] = data['devid']
    if (data['id'] > 0):  # dont change this values!
        data.pop('created', None)  # dont change this values!
        data.pop('globalid', None)  # dont change this values!
        data.pop('devid', None)  # dont change this values!

    if ('locations' in data) and not (data['locations'] is None):
        data['locations'] = str(data['locations'])[:2048]
    sql = ''
    if (data['id'] > 0):
        sql = 'update tasks set ' +\
              __build_update(data) + ' where id=' + str(data['id'])
        data['globalid'] = temp_global_id
        data['devid'] = temp_dev_id
        try:
            mydb.execute(sql)
        except Exception as ex:
            utils.log(utils.clearUserLogin(str(ex)), 'error', 'sql')
            return -11
    else:
        sql = 'insert into tasks ' + __build_insert(data)
        data['globalid'] = temp_global_id
        data['devid'] = temp_dev_id
        try:
            mydb.execute(sql)
        except Exception as ex:
            utils.log(utils.clearUserLogin(str(ex)), 'error', 'sql')
            return -12
        data['id'] = mydb_connection.insert_id()

    tags_db_ids = []
    tags_db_ids.append('0')
    if not (tags is None):
        tags_arr = tags.split(',')
        if len(tags_arr) > 0:
            for tag in tags_arr:
                tags_db_ids.append(str(setTaskTag(data['id'], tag, uid)))
                pass
    sql = 'delete from tasks_tags where taskid=' + str(data['id']) + ' and tagid not in (' + ','.join(tags_db_ids) + ')'
    try:
        mydb.execute(sql)
    except Exception:
        pass
    return data['id']


def setTaskTag(tid: int, tag: str, uid: int):
    tag = utils.removeDoubleSpaces(utils.removeQuotes(utils.removeNonUTF(utils.stripTags(tag.replace(',', '')))))
    tag_id = 0
    sql = 'select id from tags where name="' + tag + '"'
    try:
        mydb.execute(sql)
    except Exception:
        pass
    row = mydb.fetchone()
    str_time = str(int(time.time() * 1000))
    if row is None:
        sql = 'insert into tags (name,created_user,created) values ("' + tag + '",' + str(uid) + ',' + str_time + ')'
        try:
            mydb.execute(sql)
        except Exception:
            pass
        tag_id = mydb_connection.insert_id()
    else:
        tag_id = int(row['id'])
    if (tag_id is None) or (tag_id < 1):
        return
    sql = 'insert into tasks_tags set taskid=' + str(tid) + ', tagid=' + str(tag_id) + ', created=' + str_time
    try:
        mydb.execute(sql)
    except Exception:
        pass
    return tag_id


def __build_update(data: dict) -> str:
    result = ""
    for key in data:
        value = data[key]
        if (key == 'id') or (key == 'globalid') or (key == 'created'):  # ignore this fields
            continue
        if (isinstance(value, str)):
            result = result + '`' + key + '`="' +\
                     mydb_connection.escape_string(value) + '",'
        elif (isinstance(value, int)):
            result = result + '`' + key + '`=' + str(value) + ','
    return result.strip(", ")


def __build_insert(data: dict) -> str:
    prefix = ""
    postfix = ""
    for key in data:
        if key == 'id':  # ignore this fields
            continue
        value = data[key]
        if isinstance(value, str):
            prefix = prefix + '`' + key + '`,'
            postfix = postfix + '"' +\
                      mydb_connection.escape_string(value) + '",'

        elif isinstance(value, int):
            prefix = prefix + '`' + key + '`,'
            postfix = postfix + str(value) + ','
    # return last part of insert statement
    return '(' + prefix.strip(", ") + ') values (' + postfix.strip(", ") + ')'


def getIdFromGlobal(global_id: str) -> int:
    sql = 'select id from tasks where globalid="' + global_id + '"'
    mydb.execute(sql)
    row = mydb.fetchone()
    if not (row is None):
        return int(row['id'])
    return 0


def getGlobalFromId(id: int) -> str:
    sql = 'select globalid from tasks where id="' + str(id) + '"'
    mydb.execute(sql)
    row = mydb.fetchone()
    if not (row is None):
        return str(row['globalid'])
    return ""


__linkedDevices = None
__ownDevices = None
__linkedTasks = None


def getUserLinkedDevices(user_id: int, devid: int = 0, incomming: bool = True, outgoing: bool = True,
                         cache: bool = True) -> dict:
    global __linkedDevices
    if (devid == 0) and incomming and outgoing and cache and (not (__linkedDevices is None)):
        return __linkedDevices.copy()
    result = {
        'in': {
            '0': [], '1': [], '2': [], '3': [],
            'all': {}  # map of all external-ids - senders
        },
        'out': {
            '0': [], '1': [], '2': [], '3': [],
            'all': {}  # map of all external-ids - receivers
        },
        'all': {},  # map of all external-ids, without own ids
        'names': {},  # simply map of all names with login
    }

    addsql = ''
    if devid > 0:
        addsql = ' and d2.id=' + str(devid) + ' '

    result_all = result['all']
    result_names = result['names']
    if incomming:
        # get external devices that send info to user  id - src (ext-dev), dst - user device
        sql = '''select u.login,d2.name as dst_name,s.dst,d.name,d.id,s.sync0,s.sync1,s.sync2,s.sync3
                from devices as d
                inner join sync_devices as s on s.src=d.id and s.`state`>0
                inner join devices as d2 on s.dst=d2.id and d2.`uid`=''' + str(user_id) + addsql + ''' and d2.`state`>0
                inner join users as u on d.uid=u.id
                where d.state>0
                '''

        # utils.debug(sql)
        mydb.execute(sql)
        rows = mydb.fetchall()
        result_in = result['in']
        result_in_all = result_in['all']
        obj = {}
        for row in rows:
            result_names[row['id']] = {  # external
                'device': row['name'],
                'user': row['login']
            }
            result_names[row['dst']] = {
                'device': row['dst_name']
            }
            result_all[row['id']] = row['id']
            result_in_all[row['id']] = row['id']
            obj = {'src': row['id'], 'dst': row['dst']}
            if (row['sync0'] == 0):
                result_in['0'].append(obj)
            if (row['sync1'] == 1):
                result_in['1'].append(obj)
            if (row['sync2'] == 2):
                result_in['2'].append(obj)
            if (row['sync3'] == 3):
                result_in['3'].append(obj)

    if outgoing:
        # get external devices that receive info from user  id - desctination (ext-dev), src - user device
        sql = '''select u.login,d2.name as src_name,s.src,d.name,d.id,s.sync0,s.sync1,s.sync2,s.sync3 from devices as d
            inner join sync_devices as s on s.dst=d.id and s.`state`>0
            inner join devices as d2 on s.src=d2.id and d2.`uid`=''' + str(user_id) + addsql + ''' and d2.`state`>0
            inner join users as u on d.uid=u.id
            where d.state>0
            '''
        # utils.debug(sql)
        mydb.execute(sql)
        rows = mydb.fetchall()
        result_out = result['out']
        result_out_all = result_out['all']
        for row in rows:
            result_names[row['id']] = {  # external
                'device': row['name'],
                'user': row['login']
            }
            result_names[row['src']] = {
                'device': row['src_name']
            }
            result_all[row['id']] = row['id']
            result_out_all[row['id']] = row['id']
            obj = {'src': row['src'], 'dst': row['id']}
            if (row['sync0'] == 0):
                result_out['0'].append(obj)
            if (row['sync1'] == 1):
                result_out['1'].append(obj)
            if (row['sync2'] == 2):
                result_out['2'].append(obj)
            if (row['sync3'] == 3):
                result_out['3'].append(obj)

    if (devid == 0) and incomming and outgoing:
        __linkedDevices = result.copy()
    return result


def getDefaultDevice(user_id: int) -> int:
    sql = 'select id from devices where uid=' + str(user_id) + ' order by `default` desc,id limit 1'
    mydb.execute(sql)
    row = mydb.fetchone()
    if row is None:
        return 0
    return int(row['id'])


def getUserOwnDevices(user_id: int, devid: int = 0, cache: bool = True) -> dict:
    global __ownDevices
    if (devid == 0) and cache and (not (__ownDevices is None)):
        return __ownDevices.copy()

    result = {'0': [], '1': [], '2': [], '3': [], 'all': []}

    sql = '''select d.id,d.name,0 as sync0,1 as sync1,2 as sync2,3 as sync3
    from devices d
    where d.uid=''' + str(user_id) + ''' and d.state>0
    '''

    if devid > 0:
        sql = '''select d.id,d.name,
            CASE WHEN d.sync0<d2.sync0 then d.sync0 else d2.sync0 end as sync0,
            CASE WHEN d.sync1<d2.sync1 then d.sync1 else d2.sync1 end as sync1,
            CASE WHEN d.sync2<d2.sync2 then d.sync2 else d2.sync2 end as sync2,
            CASE WHEN d.sync3<d2.sync3 then d.sync3 else d2.sync3 end as sync3
            from devices d
            inner join devices d2 on d.uid=d2.uid and d2.id=''' + str(devid) + ''' and d2.state>0
            where d.uid=''' + str(user_id) + ''' and d.id!=''' + str(devid) + ''' and d.state>0
            '''

    mydb.execute(sql)
    rows = mydb.fetchall()

    # myown device will get all data that its owned
    for row in rows:
        result['all'].append(row)
        if (row['sync0'] == 0):
            result['0'].append(row['id'])
        if (row['sync1'] == 1):
            result['1'].append(row['id'])
        if (row['sync2'] == 2):
            result['2'].append(row['id'])
        if (row['sync3'] == 3):
            result['3'].append(row['id'])

    if (devid == 0):
        __ownDevices = result.copy()
    return result


def getUserLinkedTasks(user_id: int, devid: int = 0, cache: bool = True) -> list:
    global __linkedTasks
    if (devid == 0) and cache and (not (__linkedTasks is None)):
        return __linkedTasks.copy()
    result = []
    addsql = ''
    if devid > 0:
        addsql = ' and d.id=' + str(devid) + ' '
    sql = '''select t.id
        from tasks as t
        inner join sync_tasks as s on t.id=s.tid
        inner join devices as d on d.id=s.dst and d.uid=''' + str(user_id) + addsql + ''' and d.state>0
    '''
    mydb.execute(sql)
    rows = mydb.fetchall()

    # myown device will get all data that its owned
    for row in rows:
        result.append(row['id'])
    if (devid == 0):
        __linkedTasks = result.copy()
    return result


def buildSqlPermissionfilter(user_id: int, devid: int) -> str:
    links = getUserLinkedDevices(user_id, devid)
    own = getUserOwnDevices(user_id, devid)
    tasks = getUserLinkedTasks(user_id, devid)
    return '''(
            (devid=''' + str(devid) + ''')
            or
            (id in (''' + ','.join(str(x) for x in tasks) + '''))
            or
            (type=0 and devid in (''' + (','.join(str(x) for x in list(set().union(links['0'], own['0'])))) + '''))
    or
    (type=1 and devid in (''' + (','.join(str(x) for x in list(set().union(links['1'], own['1'])))) + '''))
    or
    (type=2 and devid in (''' + (','.join(str(x) for x in list(set().union(links['2'], own['2'])))) + '''))
    or
    (type=3 and devid in (''' + (','.join(str(x) for x in list(set().union(links['3'], own['3'])))) + '''))
    )'''
