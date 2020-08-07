import re
import time, datetime
from threading import Thread
import queue
import ctypes
import inspect
import yaml

filter_b = r"^__.*__$"

insert_sql_b = r"^insert\s"
update_sql_b = r"^update\s"
delete_sql_b = r"^delete\s"


def judgeSqlCommitType(sql):
    _sql = sql.lower()
    if re.match(insert_sql_b, _sql) or re.match(update_sql_b, _sql) or re.match(delete_sql_b, _sql):
        return True
    else:
        return False


def filterPrivatePrototype(ary):
    li = []
    for d in ary:
        if re.match(filter_b, d) == None:
            li.append(d)
    return li


def filterPrivateMethodPrototype(table, ary):
    li = []
    """
    getattr(Object, param)
    返回Object对象的param属性的值
    """
    for d in ary:
        # if re.match(filter_b, d) == None:
        if d[0].isupper():
            func = getattr(table, d)
            if hasattr(func, '__call__'):
                li.append(d)
    return li


def filterPrivateMethodParamsPrototype(fun):
    li = []
    """
    inspect.getargspec(fun):
    查看fun函数的参数
    """
    params = inspect.getargspec(fun)
    # params = fun.__code__.co_varnames
    for p in params[0]:
        if p != "self":
            li.append(p)
    return li

def format_script_info_data(_fun):
    params = filterPrivateMethodParamsPrototype(_fun)
    doc = filterPrivateMethodDoc(_fun)
    if doc != None:
        try:
            docDict = yaml.safe_load(doc)
            if type(docDict) == dict and 'info' in docDict and 'params' in docDict:
                keys = []
                for item in docDict['params']:
                    keys.append(item['key'])
                for arg in params:
                    if arg not in keys:
                        return {
                            'isUri': True,
                            'error': {
                                'msg': '参数与定义不符',
                                'data': '参数:{},在注释中不存在'.format(arg)
                            }
                        }
                for _k in ['title', 'detail', 'auth', 'status']:
                    if _k not in docDict['info']:
                        docDict['info'][_k] = '未定义'
                if 'release_time' not in docDict:
                    docDict['release_time'] = datetime.datetime.now().strftime('%Y/%m/%d %H:%M:%S')
                if 'tags' not in docDict:
                    docDict['tags'] = []
                if 'options' not in docDict:
                    docDict['options'] = {
                        'undependence_env': False
                    }
                for _param in docDict['params']:
                    default_item = {
                        'key': '',
                        'label': '',
                    }
                    default_schema = {
                        'enum_option': [],
                        'value_type': '',
                        'commponent_type': '',
                        'value_default': '',
                        'enum_url': '',
                        'enum_url_error': '',
                        'tooltip': '',
                        'placeholder': ''
                    }
                    if 'schema' not in _param:
                        _param['schema'] = {}
                    default_schema.update(_param['schema'])
                    _param['schema'] = default_schema
                    default_item.update(_param)
                    _param = default_item
                return {
                    'isUri': True,
                    'funParse': docDict
                }
            elif 'info' not in docDict:
                return {
                    'isUri': True,
                    'error': {
                        'msg': '解析失败，缺少必要信息：info，原文注释如下',
                        'data': doc
                    }
                }
            elif "params" not in docDict:
                return {
                    'isUri': True,
                    'error': {
                        'msg': '解析失败，缺少必要信息：params，原文注释如下',
                        'data': doc
                    }
                }
            else:
                return {
                    'isUri': True,
                    'error': {
                        'msg': '解析失败，注释不符合规范，原文注释如下',
                        'data': doc
                    }
                }
        except Exception as error:
            return {
                'isUri': True,
                'error': {
                    'msg': '解析失败, 错误信息如下',
                    'data': str(error)
                }
            }
    else:
        return {
            'isUri': True,
            'error': {
                'msg': '解析失败, 注释为空',
                'data': 'doc is None'
            }
        }
    # 这里需要制定规则。


def getTreeObj(path, item):
    keys = item.keys()
    re = []
    for key in keys:
        newPath = "{}/{}".format(path, key)
        if 'isUri' in item[key]:
            re.append({
                'label': key,
                "path": newPath
            })
        else:
            child = getTreeObj(newPath, item[key])
            re.append({
                'label': key,
                "path": newPath,
                'children': child
            })
    return re


def getRootPathList(_obj, rootPath):
    paths = rootPath.split('/')
    del paths[0]
    item = _obj
    for path in paths:
        if path == '':
            return getTreeObj(item)
        if path in item:
            item = item[path]
        else:
            return []
        if 'isUri' in item:
            return []
    return getTreeObj(item)

def uriMap2Uri(_obj, rootPath, uriList, matchUri):
    # print(type(_obj))
    if type(_obj) == dict:
        keys = _obj.keys()
        for _key in keys:
            path = "{}/{}".format(rootPath, _key)
            if 'isUri' not in _obj[_key]:
                uriMap2Uri(_obj[_key], path, uriList, matchUri)
            else:
                if re.match(matchUri, path):
                    uriList.append({
                        'uri': path,
                        'data': _obj[_key]
                    })
    else:
        print(_obj, '----------')


def filterPrivateMethodDoc(fun):
    """
    fun.__doc__:返回fun方法的注释
    """
    return fun.__doc__


def getListString(_list):
    _str = []
    for item in _list:
        if isinstance(item, str):
            _str.append("\"{}\"".format(item))
        else:
            _str.append(str(item))
    return _str


def getSqlString(data):
    tablename = data["table"]
    count = data["count"]
    select = data["select"]
    if count:
        _select_str = 'count(*)'
    else:
        if len(select) != 0:
            _select_str = ','.join(select)
    _where_str = getfilterSqlString(data)
    return 'SELECT {} \nFROM {}\n{};\n'.format(_select_str, tablename, _where_str)


def getfilterSqlString(data):
    # tablename = data["table"]
    # count = data["count"]
    # select = data["select"]
    where = data["where"]
    limit = data["limit"]
    order = data["orderBy"]
    group = data["groupBy"]
    _select_str = '*'
    _where_str = ''
    _limit_str = ''
    _order_str = ''
    _group_str = ''
    # if count:
    #     _select_str = 'count(*)'
    # else:
    #     if len(select) != 0:
    #         _select_str = ','.join(select)
    if order:
        if "key" in order:
            _order_str = "\nORDER BY {} {}".format(
                order["key"], order["type"].upper())
    if group:
        if "key" in group:
            _group_str = "\nGROUP BY {}".format(order["key"])
    if limit:
        if isinstance(limit, dict):
            _limit_str = "\nLIMIT {},{} ".format(limit['skip'], limit['limit'])
        else:
            _limit_str = '\nLIMIT {} '.format(limit)
    if where:
        _where_arry = []
        for item in where:
            if isinstance(where[item], dict):
                for child in where[item]:
                    if child.upper() == "ISNULL":
                        _where_arry.append("{} IS NULL".format(item))
                    elif child.upper() == "ISNOTNULL":
                        _where_arry.append("{} IS NOT NULL".format(item))
                    elif child.upper() == "IN":
                        if isinstance(where[item][child], list):
                            vals = getListString(where[item][child])
                            _where_arry.append("{} IN({})".format(
                                item, ','.join(vals)))
                    elif child.upper() == "NOTIN":
                        if isinstance(where[item][child], list):
                            vals = getListString(where[item][child])
                            _where_arry.append("{} NOT IN({})".format(
                                item, ','.join(vals)))
                    elif child.upper() == "LIKE":
                        _where_arry.append("{} LIKE \"{}\" ".format(
                            item, where[item][child]))
                    elif child.upper() == "NOTLIKE":
                        _where_arry.append("{} NOT LIKE \"{}\" ".format(
                            item, where[item][child]))
                    else:
                        _where_arry.append("{} {} {}".format(
                            item, child, where[item][child]))
            else:
                _where_arry.append("{}={}".format(item, where[item]))
        _where_str = 'WHERE ' + '\n AND '.join(_where_arry)
    return '{}{}{}{};'.format(_where_str, _order_str, _group_str, _limit_str)


def _terminateThread(thread):
    # if not thread.isAlive():
    #     return
    exc = ctypes.py_object(SystemExit)
    # 获取线程的ID号
    print('设定线程退出信号...')
    res = ctypes.pythonapi.PyThreadState_SetAsyncExc(
        ctypes.c_long(thread.ident), exc)
    print('获取退出线程ID:{}.'.format(res))
    if res == 0:
        print("nonexistent thread id")
        # raise ValueError("nonexistent thread id")
    elif res >= 1:
        print('线程ID:{},将要强制退出'.format(res))
        ctypes.pythonapi.PyThreadState_SetAsyncExc(thread.ident, None)
        print("PyThreadState_SetAsyncExc KILL THREAD")
        # raise SystemError()


class threadChannel():
    def __init__(self):
        self.data = {}

    def Set(self, name, val):
        self.data[name] = val

    def Get(self, name):
        return self.data[name]


def clock(name, timeout, q):
    # print('定时器【{}】创建成功...'.format(name))
    while timeout > 0:
        if q.Get('status'):
            print('【{}】连接成功，计时器正常退出!'.format(name))
            timeout = -1
        time.sleep(0.5)
        timeout = timeout - 1
        # print('【{}】计时器---{}'.format(name,timeout))
    # print('定时器【{}】记时结束...'.format(name))
    if not q.Get('status'):
        print('计时器【{}】超时，将要暂停连接线程'.format(name))
        q.Set('status', False)


def newTimeOutThread(name, fun, _args, timeout=1):
    q = threadChannel()
    q.Set('status', False)
    # fun(_args + (q,))
    t1 = Thread(target=fun, args=_args + (q,))
    t1.start()
    # t1.join()
    # print('【{}】计时器定时器启动...'.format(name))
    clock(name, timeout * 4, q)
    # print('【{}】计时器定时器运行结束...'.format(name))
    if not q.Get('status'):
        print('【{}】计时器超时或连接失败，将要停止连接线程...'.format(name))
        _terminateThread(t1)
    return q.Get('status')
