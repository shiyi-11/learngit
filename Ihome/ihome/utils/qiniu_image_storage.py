# -*- coding: utf-8 -*-
# flake8: noqa
from qiniu import Auth, put_data, etag
import qiniu.config
# 需要填写你的 Access Key 和 Secret Key
access_key = 'rEAzB3tgW-bdxhugEaMBkNtEqt3QAYX_IklQQFQn'
secret_key = '7IUr4iHAf-8o3U98wfoHf7MOvfyQioVwCZwzTshL'

def upload_image(file_data):
	# 构建鉴权对象
	q = Auth(access_key, secret_key)

	# 要上传的空间
	bucket_name = 'shiyiflaskihome'

	# 上传后保存的文件名
	# key = 'my-python-logo.png'

	# 生成上传 Token，可以指定过期时间等
	token = q.upload_token(bucket_name, None, 3600)
	# token = q.upload_token(bucket_name, key, 3600)

	# 要上传文件的本地路径
	# localfile = './sync/bbb.jpg'
	ret, info = put_data(token, None, file_data)
	print(info)
	print(ret)
	if info.status_code == 200:
		return ret.get('key')
	else:
		raise Exception('上传七牛失败')

