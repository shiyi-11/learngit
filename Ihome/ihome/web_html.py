# coding:utf-8

from flask import Blueprint, current_app, make_response
from flask_wtf import csrf

# 提供静态文件的蓝图
html = Blueprint('web_html',__name__)

# 127.0.0.1:5000/()
# 127.0.0.1:5000/index.html
# 127.0.0.1:5000/register.html
# 127.0.0.1:5000/favicon.ico #浏览器默认的网站标识，浏览器会自己请求这个资源

@html.route('/<re(r".*"):html_file_name>')
def get_html(html_file_name):
	if not html_file_name:
		html_file_name = "index.html"

	if html_file_name != 'favicon.ico':

		html_file_name = "html/" + html_file_name
	# 创建csrf_token值
	csrf_token = csrf.generate_csrf()
	# flask提供返回静态文件的方法
	response = make_response(current_app.send_static_file(html_file_name))
	# 设置cookie
	response.set_cookie('csrf_token', csrf_token)

	# flask提供返回静态文件的方法
	return response