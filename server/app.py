from flask import Flask
from flask_cors import CORS
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from flask_restful import Api
# from flask_restplus import Api
from flask_cors import CORS
# 引入路由
from server import router

def init_app(argv):
    # 初始化服务
    application = Flask(__name__)
    # 跨域配置
    CORS(application, resources={r"*": {"origins": "*"}})
    # 加载配置文件
    if "dev" in argv:
        application.config.from_pyfile('../config/config.dev.py')
    else:
        application.config.from_pyfile('../config/config.py')
    # 加载中间件
    api = Api(application)
    Bcrypt(application)
    JWTManager(application)
    # 加载路由
    router.initialize_routes(api)
    return application
