# coding:utf-8


from werkzeug.routing import BaseConverter
from flask import jsonify, session, g
from ihome.utils.response_code import RET
import functools
# 定义正则转换器
class ReConverter(BaseConverter):
	''''''
	def __init__(self, url_map, regex):
		super(ReConverter, self).__init__(url_map)
		self.regex = regex


def login_required(view_func):
	@functools.wraps(view_func)
	def wrapper(*args,**kwargs):
		user_id = session.get('user_id')
		if user_id is not None:
			g.user_id = user_id
			return view_func(*args,**kwargs)
		else:
			return jsonify(re_code=RET.SESSIONERR,msg='用户未登陆')
	return wrapper

