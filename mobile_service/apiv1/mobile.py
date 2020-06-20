from _common.api import auth
from _common.api import db
from _common.api import headers
from _common.api import utils
from _common.api._settings import mydb

__speedup_cache = None  # tasks not cached


def clearPermissionSQLCache():
    global __speedup_cache
    __speedup_cache = None


# SQL query MUST be optimized - later
# extendType = 0 - only array of current ids in ['val']['ids']
# extendType = 1 - current records directly from database in ['db'] field Only DATABASE
# extendType = 0 - array of current ids, serials, updates - ['val']['ids','serials','updates']
def getTotalIdsString(user_id: int, devid: int, cross: str = '', extendType: int = 0) -> dict:
    global __speedup_cache

    tasks = getLinkedTasks(user_id, devid)
    if __speedup_cache is None:
        links = getLinkedDevices(user_id, devid)
        own = getOwnDevices(user_id, devid)  # except myself
        __speedup_cache = ''' 
        (type=0 and devid in (''' + (','.join(str(x) for x in list(set().union(links['0'], own['0'])))) + '''))
        or
        (type=1 and devid in (''' + (','.join(str(x) for x in list(set().union(links['1'], own['1'])))) + '''))
        or
        (type=2 and devid in (''' + (','.join(str(x) for x in list(set().union(links['2'], own['2'])))) + '''))
        or
        (type=3 and devid in (''' + (','.join(str(x) for x in list(set().union(links['3'], own['3'])))) + ''')) '''

    cross = utils.clearStringHard(cross)
    add_fields = ''  # when extendType==0
    if extendType == 1:
        add_fields = ' *,'
    if len(cross) > 0:
        cross = ' and globalid in (' + ("'" + "','".join(cross.split(',')) + "'") + ') '
    sql = '''
    select ''' + add_fields + ''' globalid as fval, update_time as ftime, `serial` as fserial from tasks
    where state=20 ''' + cross + ''' and
    (
    (devid=''' + str(devid) + ''')
    or
    ''' + __speedup_cache + '''
    or
    (id in (''' + ','.join(str(x) for x in tasks) + '''))
    )
    order by serial,update_time
    '''
    result = {'info': {}, 'time': 0, 'serial': 0, 'count': 0, 'db': []}
    try:
        mydb.execute(sql)
    except Exception as ex:
        utils.log(utils.clearUserLogin(str(ex)), 'error', 'sql')
        return None

    rows = mydb.fetchall()

    ids_arr = []
    ser_arr = []
    upd_arr = []
    count = 0
    max_time = 0
    serial = 0
    for row in rows:

        tserial = int(row['fserial'])
        if row['ftime'] is None:
            row['ftime'] = 0
        tupdate = int(row['ftime'])
        if (extendType == 0) or (extendType == 2):
            ids_arr.append(row['fval'])
            if extendType == 2:
                ser_arr.append(str(tserial))
                upd_arr.append(str(tupdate))

        count = count + 1
        serial = serial + tserial
        if tupdate > max_time:
            max_time = tupdate

        if extendType == 1:
            row.pop('fval', None)
            row.pop('ftime', None)
            row.pop('fserial', None)
            result['db'].append(row)

    if (extendType == 0) or (extendType == 2):
        result['info']['ids'] = ','.join(ids_arr)
        if extendType == 2:
            result['info']['serials'] = ','.join(ser_arr)
            result['info']['updates'] = ','.join(upd_arr)
    result['time'] = max_time
    result['count'] = count
    result['serial'] = serial
    return result
    # myown device will get all data that its owned


def getLinkedDevices(user_id: int, devid: int) -> dict:
    result = {'0': [], '1': [], '2': [], '3': [], 'all': []}

    links = db.getUserLinkedDevices(
            user_id=user_id, devid=devid, incomming=True, outgoing=False, cache=False)

    for key, value in links['all']:
        result['all'].append({'id': value, 'name': links['names'][value]})

    for value in links['in']['0']:
        result['0'].append(value['src'])
    for value in links['in']['1']:
        result['1'].append(value['src'])
    for value in links['in']['2']:
        result['2'].append(value['src'])
    for value in links['in']['3']:
        result['3'].append(value['src'])

    if len(result['0']) < 1:
        result['0'].append(0)
    if len(result['1']) < 1:
        result['1'].append(0)
    if len(result['2']) < 1:
        result['2'].append(0)
    if len(result['3']) < 1:
        result['3'].append(0)
    if len(result['all']) < 1:
        result['all'].append({'id': 0, 'name': ''})
    return result


# except myself
def getOwnDevices(user_id: int, devid: int) -> dict:
    result = db.getUserOwnDevices(user_id=user_id, devid=devid, cache=False)  # except myself

    if len(result['0']) < 1:
        result['0'].append(0)
    if len(result['1']) < 1:
        result['1'].append(0)
    if len(result['2']) < 1:
        result['2'].append(0)
    if len(result['3']) < 1:
        result['3'].append(0)
    if len(result['all']) < 1:
        result['all'].append(0)
    return result


def getLinkedTasks(user_id: int, devid: int) -> list:
    result = db.getUserLinkedTasks(user_id=user_id, devid=devid, cache=False)
    if len(result) < 1:
        result.append(0)
    return result


def log(message: str, tag: str = '  info'):
    utils.log(message, tag, 'mobile')


def elog(message: str, tag: str = 'error'):
    utils.log(message, tag, 'mobile_error')


def sql_request(sql: str):
    try:
        mydb.execute(sql)
    except Exception as ex:
        utils.log(utils.clearUserLogin(str(ex)), 'error', 'sql')
        headers.errorResponse('SQL error')


if not (auth.isMobile):  # check that this request from mobile application
    headers.jsonAPI(False)
    elog('Only from mobile uid:' + auth.user_id)
    headers.errorResponse('Wrong type')
