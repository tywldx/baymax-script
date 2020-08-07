# -*- coding:utf-8 -*-
import json
import b_msg, b_globals
from flask_restful import Resource
from flask import g, request
from scriptes import env_router
from libs import script_router, error_handel

class ExecuteController(Resource):
    """
    request.body = {
        env_name: '',
        method: ''
    }
    """
    def post(self):
        param = request.json
        # 设定全局变量
        # b_globals.__set_request()
        try:
            g.env_name = param['env_name']
            router = script_router.Route()
            return router.apply(param)
            # 删除全局变量
        except Exception as e:
            # 删除全局变量
            error_log = error_handel.log_traceback(e)
            return b_msg.error(msg={
                    'type': type(e).__name__,
                    'message': error_log,
                    'requestBody': param,
                })

class GetEnvironmentList(Resource):
    def get(self):
        return b_msg.success(data=env_router.EnvRouter().get_env_list())

class Health(Resource):
    def post(self):
        self.finish(b_msg.success())

class GetFolderTree(Resource):
    def post(self):
        """
        params: param 参数是需要获取的URI的地址，案例
        {
            rootPath: '/'
        }
        """
        param = request.json
        try:
            router = script_router.Route()
            script_tree=router.get_scripts_tree(param) #getRouterTree(param)
            return b_msg.success(data=script_tree)
        except Exception as e:
            error_log = error_handel.log_traceback(e)
            return b_msg.error(msg={
                    'type': type(e).__name__,
                    'message': error_log,
                    'requestBody': param,
                })


class GetListByPath(Resource):
    def post(self):
        """
        params: param 参数是需要获取的URI的地址，案例
        {
            rootPath: '/'
        }
        """
        param = request.json
        try:
            router = script_router.Route()
            uri_list=router.get_scripts_list(param)
            return b_msg.success(data=uri_list)
        except Exception as e:
            error_log = error_handel.log_traceback(e)
            return b_msg.error(msg={
                    'type': type(e).__name__,
                    'message': error_log,
                    'requestBody': param,
                })
