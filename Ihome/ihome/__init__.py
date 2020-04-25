# coding:utf-8

from flask import Flask
from config import config_map, Config
from flask_sqlalchemy import SQLAlchemy
import redis
from flask_session import Session
from flask_wtf import CSRFProtect
from ihome.utils.commons import ReConverter
import logging
from logging.handlers import RotatingFileHandler

# 创建数据库
db = SQLAlchemy()
# 创建redis连接对象
redis_store = None


logging.basicConfig(level=logging.INFO)  # 调试debug级
# 创建日志记录器，指明日志保存的路径、每个日志文件的最大大小、保存的日志文件个数上限
file_log_handler = RotatingFileHandler("logs/log", maxBytes=1024 * 1024 * 100, backupCount=10)
# 为全局的日志工具对象（flask app使用的）添加日志记录器
logging.getLogger().addHandler(file_log_handler)


# 工厂模式
def create_app(config_name):
	'''
	创建flask用用对象
	:param config_name:str 配置模式的名字 （‘develop’，‘product’）
	:return:
	'''
	app = Flask(__name__)

	# 根据配置模式的名字获取配置参数的类
	config_class = config_map.get(config_name)
	app.config.from_object(config_class)
	# 使用app初始化db
	db.init_app(app)

	# 初始化redis工具，区别开发模式和生产模式
	global redis_store
	redis_store = redis.StrictRedis(host=Config.REDIS_HOST, port=Config.REDIS_PORT)

	# 利用flask-session，将session数据保存在redis中
	Session(app)

	# 为flask补充csrf防护，用户使用的是银行服务器的html发起请求，黑客用的是自己服务器的html发起请求，
	# 因为同源策略，黑客html中的js读取不了银行服务器的html中的数据（包括header和body中的cookie是服务器返回页面🥌给上的）
	# CSRFProtect(app)
	# 同源策略是浏览器的一个安全功能，不同源的客户端脚本在没有明确授权的情况下，不能读写对方资源。
	# 所以xyz.com（服务器）下的js脚本采用ajax读取abc.com（服务器）里面的文件数据是会被拒绝的。
	# 同源策略限制了从同一个源加载的文档或脚本如何与来自另一个源的资源进行交互。这是一个用于隔离潜在恶意文件的重要安全机制。

	# 添加自定义的转换器
	app.url_map.converters['re'] = ReConverter
	# 注册蓝图
	from ihome import api_v1_0
	app.register_blueprint(api_v1_0.api, url_prefix="/api/v1.0")

	# 注册提供静态文件的蓝图
	from ihome import web_html
	app.register_blueprint(web_html.html)

	return app