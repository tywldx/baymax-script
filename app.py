import sys
from server import app
from flask_apscheduler import APScheduler

print('执行初始化')
main_app = app.init_app(sys.argv)
print('服务启动...!', main_app.config['SERVER_PORT'])
main_app.run(host=main_app.config['SERVER_HOST'], port=main_app.config['SERVER_PORT'])
print('服务关闭...!')