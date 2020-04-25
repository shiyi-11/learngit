# coding:utf-8
from ihome.utils.captcha.captcha import captcha
from . import api
from ihome import redis_store, constants, db
from flask import current_app, jsonify, make_response, request, json
from ihome.utils.response_code import RET
import re
# from ihome.tasks.tasks_sms import send_sms
from ihome.tasks.sms.tasks import sends_sms
import random
from ihome.models import User
from ihome.libs.yuntongxun.SendSMS import CCP
redis_conn = redis_store


# 127.0.0.1：5000/api/v1.0/image_codes/<image_code_id>
@api.route('/image_codes/<image_code_id>')
def get_image_code(image_code_id):
    '''
    获取图片验证码
    :return:验证码图片
    '''
    print('生成图片验证码')
    # 生成图片验证码的name, text, image_data（二进制数据）
    name, text, image_data = captcha.generate_captcha()
    print(type(text))

    # 设置redis和有效期
    # redis_store.set('image_code_%s' % image_code_id, text)
    # redis_store.expire('image_code_%s' % image_code_id, constants.AREA_INFO_REDIS_EXPIRES)
    # 把上面两步用一步完成        记录名字                        记录有效期                      记录值
    try:
        redis_conn.setex('image_code_%s' % image_code_id, constants.IMAGE_CODE_REDIS_EXPIRES, text)
    except Exception as e:
        # 记录日志
        current_app.logger.error(e)
        # return jsonify(re_code=RET.DBERR, errmsg='save image code id failed')
        return jsonify(re_code=RET.DBERR, errmsg='保存图片id失败')
    # 业务处理
    # 生成验证码图片
    # 将验证码真实值和编号保存在redis中
    # 返回值
    response = make_response(image_data)
    response.headers['Content-Type'] = 'image/jpg'
    return response


# get api/v1.0/sms_codes/<mobile>?image_code=xxxx&image_code_id=xxxx
# @api.route("/sms_codes/<re(r'1[34578]\d{9}'):mobile>")
# def send_sms_code(mobile):
#     """发送手机短信息验证码：
#     1.接收参数，手机号，图片验证码，uuid
#     2.校验数据
#     3.判断图片验证码是否正确，如果正确
#     4.发送短信验证码
#     """
#     # 1.接收参数
#     print('短信验证1')
#     # 'image_code_id': imageCodeId,
#     # 'image_code': imageCode
#     image_code=request.args.get("image_code")
#     image_code_id=request.args.get('image_code_id')
#     print(image_code_id)
#     print(image_code)
#
#     phone_num = mobile
#     print(phone_num)
#     print('短信验证2')
#
#     # 2.校验数据
#     if not all([image_code,image_code_id]):
#
#         return jsonify(re_code=RET.PARAMERR,msg='缺少参数')
#
#     # 校验手机号是否正确
#     if not re.match(r'^0\d{2,3}\d{7,8}$|^1[358]\d{9}$|^147\d{8}$',phone_num):
#         return jsonify(re_code=RET.PARAMERR,msg='手机号不正确')
#     print('短信验证3')
#     #判断用户是否已注册
#     try:
#         user=User.query.filter(User.phone_num == phone_num).first()
#     except Exception as e:
#         current_app.logger.debug(e)
#         return jsonify(re_code=RET.DBERR,msg='查询数据库错误')
#     print('短信验证4')
#     #用户存在，提示该账户已被注册
#     if user:
#         return jsonify(re_code=RET.DATAEXIST,msg='该用户已被注册')
#     print('短信验证5')
#     # 3.判断图片验证码是否正确，如果正确
#     try:
#         # 从Redis取出值图片验证码
#         real_image_code=redis_conn.get('image_code_%s' %image_code_id)
#         print(real_image_code)
#     except Exception as e:
#         current_app.logger.debug(e)
#         return jsonify(re_code=RET.DBERR,msg='获取redis服务器图片验证码失败')
#     print('短信验证6')
#
#     #判断为验证码空或者过期
#     if not real_image_code:
#         return jsonify(re_code=RET.NODATA,msg='图片验证码已过期')
#     print('短信验证7')
#
#     # 获取短信验证码时删除对应的的图片验证码
#     try:
#         redis_conn.delete('image_code_%s' %image_code_id)
#         print('删除突破验证码')
#     except Exception as e:
#         current_app.logger.error(e)
#
#     #校验和前端传的验证码是否相等
#     if real_image_code.lower() == image_code.lower():
#
#         return jsonify(re_code=RET.DATAERR,msg='验证码输入有误')
#     print('短信验证8')
#
#     # 4.生成验证码
#     sms_code='%06d' % random.randint(0,999999)
#     current_app.logger.debug('短信验证码为：'+sms_code)
#     print(type(sms_code))
#     # 6.发送成功，短信验证码存储到Redis
#     try:
#         # constants.SMS_CODE_REDIS_EXPIRES是过期时间5分钟
#         redis_conn.setex('PhoneCode:'+phone_num,constants.SMS_CODE_REDIS_EXPIRES,sms_code)
#         # redis_conn.setex('PhoneCode:' + phone_num, constants.SMS_CODE_REDIS_EXPIRES, sms_code)
#     except Exception as e:
#         current_app.logger.debug(e)
#         return jsonify(re_code=RET.DBERR,msg='存储短信验证码失败')
#     print('短信验证9')
#     #响应结果
#     # 5.发送短信验证码            验证码         过期时间：容联的时间单位为:分   短信模板1
#     # result = CCP().send_sms('15770633066',[sms_code,constants.SMS_CODE_REDIS_EXPIRES/60],'1')
#     # if result != 1:
#     #     # 短信发送失败
#     #     return jsonify(re_code=RET.THIRDERR,msg='发送短信验证码失败')
#     try:
#         ccp = CCP()
#         print(22222)
#         # 云通讯发送短信验证码
#         res = ccp.send_sms(phone_num,[sms_code,str(constants.SMS_CODE_REDIS_EXPIRES/60)],1)
#     except Exception as e:
#         current_app.logger.error(e)
#         return jsonify(re_code=RET.THIRDERR, msg='发送失败')
#     print('短信验证10')
#     if res == 0:
#         return jsonify(re_code=RET.OK,msg='验证码发送成功')
#     else:
#         return jsonify(re_code=RET.THIRDERR,msg='发送失败')



@api.route("/sms_codes/<re(r'1[34578]\d{9}'):mobile>")
def send_sms_code(mobile):
    """发送手机短信息验证码：
    1.接收参数，手机号，图片验证码，uuid
    2.校验数据
    3.判断图片验证码是否正确，如果正确
    4.发送短信验证码
    """
    # 1.接收参数
    print('短信验证1')
    # 'image_code_id': imageCodeId,
    # 'image_code': imageCode
    image_code=request.args.get("image_code")
    image_code_id=request.args.get('image_code_id')
    print(image_code_id)
    print(image_code)

    phone_num = mobile
    print(phone_num)
    print('短信验证2')

    # 2.校验数据
    if not all([image_code,image_code_id]):

        return jsonify(re_code=RET.PARAMERR,msg='缺少参数')

    # 校验手机号是否正确
    if not re.match(r'^0\d{2,3}\d{7,8}$|^1[358]\d{9}$|^147\d{8}$',phone_num):
        return jsonify(re_code=RET.PARAMERR,msg='手机号不正确')
    print('短信验证3')
    #判断用户是否已注册
    try:
        user=User.query.filter(User.phone_num == phone_num).first()
    except Exception as e:
        current_app.logger.debug(e)
        return jsonify(re_code=RET.DBERR,msg='查询数据库错误')
    print('短信验证4')
    #用户存在，提示该账户已被注册
    if user:
        return jsonify(re_code=RET.DATAEXIST,msg='该用户已被注册')
    print('短信验证5')
    # 3.判断图片验证码是否正确，如果正确
    try:
        # 从Redis取出值图片验证码
        real_image_code=redis_conn.get('image_code_%s' %image_code_id)
        print(real_image_code)
    except Exception as e:
        current_app.logger.debug(e)
        return jsonify(re_code=RET.DBERR,msg='获取redis服务器图片验证码失败')
    print('短信验证6')

    #判断为验证码空或者过期
    if not real_image_code:
        return jsonify(re_code=RET.NODATA,msg='图片验证码已过期')
    print('短信验证7')

    # 获取短信验证码时删除对应的的图片验证码
    try:
        redis_conn.delete('image_code_%s' %image_code_id)
        print('删除突破验证码')
    except Exception as e:
        current_app.logger.error(e)

    #校验和前端传的验证码是否相等
    if real_image_code.lower() == image_code.lower():

        return jsonify(re_code=RET.DATAERR,msg='验证码输入有误')
    print('短信验证8')



    # 4.生成验证码
    sms_code='%06d' % random.randint(0,999999)
    current_app.logger.debug('短信验证码为：'+sms_code)
    print(type(sms_code))
    # 6.发送成功，短信验证码存储到Redis
    try:
        # constants.SMS_CODE_REDIS_EXPIRES是过期时间5分钟
        redis_conn.setex('PhoneCode:'+phone_num,constants.SMS_CODE_REDIS_EXPIRES,sms_code)
        # redis_conn.setex('PhoneCode:' + phone_num, constants.SMS_CODE_REDIS_EXPIRES, sms_code)
    except Exception as e:
        current_app.logger.debug(e)
        return jsonify(re_code=RET.DBERR,msg='存储短信验证码失败')
    print('短信验证9')
    #响应结果
    # 5.发送短信验证码            验证码         过期时间：容联的时间单位为:分   短信模板1
    # result = CCP().send_sms('15770633066',[sms_code,constants.SMS_CODE_REDIS_EXPIRES/60],'1')
    # if result != 1:
    #     # 短信发送失败
    #     return jsonify(re_code=RET.THIRDERR,msg='发送短信验证码失败')

    # 调用celery发送请求
    print()
    sends_sms(phone_num,[sms_code,str(constants.SMS_CODE_REDIS_EXPIRES/60)],1)

    return jsonify(re_code=RET.OK,msg='验证码发送成功')



