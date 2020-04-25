# --*-- coding:utf-8 --*--
import re
from flask import request, jsonify, current_app, session
from ihome import redis_store, db, constants
# from . import api
from ihome.api_v1_0 import api
from ihome.models import User
from ihome.utils.commons import login_required
from ihome.utils.response_code import RET
from sqlalchemy.exc import IntegrityError

redis_conn = redis_store

# /api/v1.0/users?mobile=xxx&phonecode=xxx&password=xxx&password2=xxx
@api.route('/users',methods=['POST'])
def register():
    """用户注册接口：
    1.获取参数phone_num 手机号，phonecode 	短信验证码，password 	密码
    2.校验数据
    3.从Redis获取短信验证码，和传来的数据校验，如果正确
    4.新增user对象，
    5.跳转首页，保持登录状态
    :return 返回注册信息{ 're_code':'0','msg':'注册成功'}
    """
    # 1.获取参数phone_num 手机号，phonecode 	短信验证码，password 	密码
    print('注册')
    json_dict=request.get_json()
    phone_num=json_dict.get('phone_num')
    sms_code=json_dict.get('phonecode')
    password=json_dict.get('password')
    password2 = json_dict.get('password2')

    #2.校验数据
    print(phone_num)
    print(sms_code)
    print(password2)
    print(password)
    if not all([phone_num,sms_code,password]):
        return jsonify(re_code=RET.PARAMERR,msg='参数不完整')
    print(1)
    # 校验手机号是否正确
    if not re.match(r'^0\d{2,3}\d{7,8}$|^1[358]\d{9}$|^147\d{8}$', phone_num):
        return jsonify(re_code=RET.PARAMERR, msg='手机号不正确')
    print(2)
    # 确认密码
    if password != password2:
        return jsonify(re_code=RET.PWDERR, msg='确认密码不一致')
    print(3)

    # 3.从Redis获取短信验证码，和传来的数据校验，如果正确
    try:
        real_sms_code=redis_conn.get('PhoneCode:'+phone_num)
    except Exception as e:
        current_app.logger.debug(e)
        return jsonify(re_code=RET.DBERR,msg='查询短信验证码失败')
    print(4)
    # 短信验证
    # str.encode('utf-8')
    # bytes.decode('utf-8')
    print(real_sms_code)
    real_sms_code=real_sms_code.decode('utf-8')
    print(real_sms_code)
    print(sms_code)
    if real_sms_code != sms_code:
        return jsonify(re_code=RET.PARAMERR,msg='短信验证码错误')
    print(5)
    #4.新增user对象，
    user=User()
    user.name=phone_num
    user.phone_num=phone_num
    # 加密密码
    user.password_hash=password
    # 提交
    try:
        db.session.add(user)
        db.session.commit()

    except IntegrityError as e:
        current_app.logger.errer(e)
        # 回滚
        db.session.rollback()
        return jsonify(re_code=RET.DBERR, msg='手机号已被注册')


    except Exception as e:
        current_app.logger.errer(e)
        db.session.rollback()
        return jsonify(re_code=RET.DBERR,msg='注册失败')
    print(6)
    #5.跳转首页，保持登录状态
    session["user_id"] = user.id
    session["name"] = user.name
    session["phone_num"] = user.phone_num
    #6.响应结果
    print('注册成功')
    return jsonify(re_code=RET.OK,msg='注册成功')

@api.route('/sessions',methods=['POST'])
def login():
    """登录
    1.获取参数：手机号，密码，并校验数据
    2.查询数据库，校验密码。
    :return: 返回响应，保持登录状态
    """
    # 获取参数
    json_dict=request.get_json()
    phone_num=json_dict.get('mobile')
    password=json_dict.get('password')
    if not all([phone_num,password]):
        return jsonify(re_code=RET.PARAMERR,msg='参数错误')

    # 限制登陆错误次数
    user_ip = phone_num
    try:
        access_num = redis_conn.get('access_num_%s'%user_ip)
    except Exception as e:
        current_app.logger.errer(e)
    else:
        if access_num is not None and int(access_num) >= constants.ACCESS_NUM:
            return jsonify(re_code=RET.REQERR,msg='登陆次数受限，请10分钟后重试')
    # 查询用户
    try:
        user=User.query.filter(User.phone_num==phone_num).first()
    except Exception as e:
        current_app.logger.debug(e)
        return jsonify(re_code=RET.DBERR,msg='查询用户失败')

    if not user or not user.check_password(password):
        try:
            # 设置累计登陆次数和有效期
            redis_conn.incr('access_num_%s'%user_ip)
            redis_conn.expire('access_num_%s'%user_ip,constants.ACCESS_NUM_TIME)
        except Exception as e:
            current_app.logger.errer(e)

        return jsonify(re_code=RET.LOGINERR,msg='用户或密码错误')


    # 5.跳转首页，保持登录状态
    session["user_id"]=user.id
    session["name"]=user.name
    session["phone_num"]=user.phone_num
    print('登陆成功')

    return jsonify(re_code=RET.OK,msg='登录成功')

@api.route('/sessions',methods=['GET'])
def check_login():
    # 检查登陆状态
    name = session['name']
    user_id = session["user_id"]
    phone_num = session["phone_num"]
    if name is not None:
        return jsonify(re_code=RET.OK, msg="ture",user={"name":name,"user_id":user_id,"phone_num":phone_num})
    else:
        return jsonify(re_code=RET.SESSIONERR, msg="false")


@api.route('/sessions',methods=['DELETE'])
@login_required     #登录校验
def logout():
    """退出登录功能：
    删除session
    :return: 返回响应，跳转首页
    """

    # session.pop('user_id')
    # session.pop('name')
    # session.pop('phone_num')
    session.clear()
    return jsonify(re_code=RET.OK,msg='退出成功')