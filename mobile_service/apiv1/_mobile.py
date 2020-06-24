from _common.api import auth
from _common.api import db
from _common.api import headers
from _common.api import utils
from _common.api._settings import mydb


# SQL query MUST be optimized - later
# extendType = 0 - only array of current ids in ['info']['ids']
# extendType = 1 - current records directly from database in ['db'] field Only DATABASE
# extendType = 2 - array of current ids, serials, updates - ['val']['ids','serials','updates']
def getTotalIdsString(user_id: int, devid: int, cross: str = '', extendType: int = 0) -> dict:
    sql_tasks_permission_string = db.buildSqlPermissionfilter(user_id=user_id, devid=devid, cache=False)
    cross = utils.clearStringHard(cross)
    add_fields = ''  # when extendType==0
    add_condition = ''
    if extendType == 1:
        add_fields = " GROUP_CONCAT(tgs.name SEPARATOR ',') as tags,t.*,"
        add_condition = '''
        left join tasks_tags as tt on tt.taskid=t.id 
        left join tags as tgs on tt.tagid=tgs.id
        '''

    if len(cross) > 0:
        cross = ' and t.globalid in (' + ("'" + "','".join(cross.split(',')) + "'") + ') '

    # building sql request
    sql = '''
    select ''' + add_fields + ''' t.globalid as fval, t.update_time as ftime, t.`serial` as fserial from tasks as t 
    ''' + add_condition + '''    
    where t.state=20 ''' + cross + ''' and
    (
    ''' + sql_tasks_permission_string + '''
    )
    group by t.id
    order by t.update_time,t.`serial`
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
            if row['tags'] is None or (len(row['tags']) < 1):
                row.pop('tags', None)
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


def sql_request_ignore_error(sql: str):
    try:
        mydb.execute(sql)
    except Exception:
        pass


if not (auth.isMobile):  # check that this request from mobile application
    headers.jsonAPI(False)
    elog('Only from mobile uid:' + auth.user_id)
    headers.errorResponse('Wrong type')
