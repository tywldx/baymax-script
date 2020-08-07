import b_logger
import pymysql
import contextlib
from pymysql import err
from flask import g
from libs import error_handel
from scriptes import env_router
"""
这里是一个基于pymysql组件的数据库连接配置。
主要功能：
建立一个数据库连接池，PYMYSQL_CONNECT_POOL.用于管理多环境的连接。
异常处理：
     1、当连接出现错误时，会进行重试。
     2、数据库的连接超时，通过
"""
# 连接池
PYMYSQL_CONNECT_POOL = {}

def get_env_mysql_connect(env_name:str, db_name: str):
    flg, options = env_router.EnvRouter().get_mysql_option(env_name, db_name)
    if flg:
        connect_long_name = "{}-{}-{}".format(env_name, options["host"], options["port"])
        if not connect_long_name in PYMYSQL_CONNECT_POOL:
            # try:
                _conn = pymysql.connect(
                    host=options["host"],
                    port=int(options["port"]),
                    user=options["user"],
                    passwd=options["passwd"],
                    db=db_name,
                    charset='utf8',
                    autocommit=True,
                    cursorclass=pymysql.cursors.DictCursor,
                    connect_timeout=10
                )
                PYMYSQL_CONNECT_POOL[connect_long_name] = _conn
                return _conn
            # except Exception as e:
            #     raise Exception('数据库连接失败:{}, {}'.format(env_name, db_name))
            #     raise Exception({
            #         'error': '数据库连接失败:{}, {}'.format(env_name, db_name),
            #         'resean': e
            #     })
        try:
            cursor = PYMYSQL_CONNECT_POOL[connect_long_name].cursor()
            cursor.execute("select 1")
            cursor.close()
            return PYMYSQL_CONNECT_POOL[connect_long_name]
        except Exception as e:
            del PYMYSQL_CONNECT_POOL[connect_long_name]
            get_env_mysql_connect(env_name, db_name)
    else:
        raise Exception(options)

def get_mysql_connect(db_name:str):
    return get_env_mysql_connect(g.env_name, db_name)

class GetConnect():
    def __enter__(self):
        print("In __enter__()")
        return "Foo"
 
    def __exit__(self, type, value, trace):
        print("Out __enter__()")

@contextlib.contextmanager
def get_cursor(db_name: str):
    connect = get_mysql_connect(db_name)
    cursor = connect.cursor()
    try:
        yield cursor
    finally:
        connect.commit()
        cursor.close()

def execute(sql: str, db_name: str = ''):
    """
    返回数据类型: SqlObj[]
    """
    if db_name == '':
        raise Exception("SQL:{} 未对db_name 输入参数!".format(sql))
    with get_cursor(db_name) as cursor:
        try:
            cursor.execute(sql)
        except err.ProgrammingError as e:
            raise Exception("SQL:\"{}\". 执行失败，请检查!".format(sql))
        row_all = cursor.fetchall()
        return row_all

def execute_count(sql: str, db_name: str = ''):
    """
    返回数据 (count, data)
    """
    if db_name != '':
        _use_db(db_name)
    try:
        with get_cursor(db_name) as cursor:
            row_count = cursor.execute(sql)
            row_all = cursor.fetchall()
            return row_count, row_all
    except Exception as er:
        raise Exception({
            'error': 'SQL执行失败:{}'.format(sql),
            'resean': e
        })

def execute_get_one(sql: str, db_name: str = ''):
    """
    返回数据 SqlObj
    """
    if db_name != '':
        _use_db(db_name)
    try:
        with get_cursor(db_name) as cursor:
            row_count = cursor.execute(sql)
            row_one = cursor.fetchone()
            return row_one
    except Exception as er:
        raise Exception({
            'error': 'SQL执行失败:{}'.format(sql),
            'resean': e
        })
