# from libs import error_handel
from flask import g
from interface.component.b_pymysql import mysql_pool
import requests
import b_logger
from scriptes import env_router
class BaseClass():
    """
    基础类，用来定义对外调用，例如redis,mq,api等，(mysql已经在底层进行封装)
    """
    def __init__(self):
        pass
    
    def __get_host(self, application_name):
        # 获取 g.env_name 下的对应的应用的域名配置
        router = env_router.EnvRouter()
        return router.get_application_host(g.env_name, application_name)

    def __request(self, opt):
        try:
            res = None
            new_opt = {
                    'url': opt['url']
            }
            is_json = False
            if 'json' in opt:
                is_json = opt['json']
            if 'headers' in opt:
                new_opt['headers'] = opt['headers']
            if 'body' in opt:
                new_opt['json'] = opt['body']
            if 'params' in opt:
                new_opt['params'] = opt['params']
            b_logger.info('-------请求参数：-------', new_opt)
            if 'method' in opt and opt['method'].upper() == 'POST':
                res = requests.post(**new_opt)
            else:
                res = requests.get(**new_opt)
            if res.status_code == 404:
                msg = 'request: {} statuscode:404'.format(json.dumps(opt))
                b_logger.error(msg)
                raise Exception(msg)
            else:
                b_logger.info('----获取返回结果----', res.text)
                reItem = res.text
                if "application/json" in res.headers['Content-Type']:
                    b_logger.info('返回结果JSON序列化')
                    reItem = json.loads(res.content)
                return reItem
        except Exception as e:
            raise Exception(e)
    
    def __execute(self, sql, db_name):
        return mysql_pool.execute(sql, db_name)
    
    def __execute_count(self, sql, db_name):
        return mysql_pool.execute_count(sql, db_name)
    
    def __execute_get_one(self, sql, db_name):
        return mysql_pool.execute_get_one(sql, db_name)