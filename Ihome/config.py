# coding:utf8
import redis

class Config(object):


	SECRET_KEY = '\x1b(=\xdc\x13[-\xc0\xf22O'

	SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:shiyi@127.0.0.1:3306/ihome"
	SQLALCHEMY_TRACK_MODIFICATIONS = True

	REDIS_HOST = '127.0.0.1'
	REDIS_PORT = 6379


	SESSION_TYPE = 'redis'
	SESSION_REDIS = redis.StrictRedis(host=REDIS_HOST,port=REDIS_PORT)
	# 隐藏cookie中的session的id
	SESSION_USE_SINGER = True
	# SESSION_PERMANENT = False
	PERMANENT_SESSION_LIFETIME = 86400

class DevelopmentConfig(Config):
	'''开发模式配置信息'''
	DEBUG = True


class ProductionConfig(Config):
	'''生产环境配置信息'''
	pass

config_map = {
	'develop':DevelopmentConfig,
	'product':ProductionConfig
}