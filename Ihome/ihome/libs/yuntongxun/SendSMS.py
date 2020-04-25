#coding=gbk

#coding=utf-8

#-*- coding: UTF-8 -*-  

from ihome.libs.yuntongxun.CCPRestSDK import REST
# import ConfigParser

# 主张号
accountSid= '8aaf07087051bcec01707b228070177b'

# 主账号token
accountToken= '6b9407c4d36f48a49768483455380f48'

# 应用Id
appId='8aaf07087051bcec01707b2280d91781'

# 请求地址，格式如下，不需要写http://
serverIP='app.cloopen.com'

# 请求端口
serverPort='8883'

# REST版本号
softVersion='2013-12-26'

class CCP(object):
    """自己封装的发送短信的辅助类"""
    # 用来保存对象的类属性
    __instance=None
    def __new__(cls, *args, **kwargs):
        if cls.__instance is None:
            # 判断cpp类有没有已经创建的对象，如果没有创建一个对象，并且保存
            # 如果有返回保存的对象
            cls.__instance=super(CCP, cls).__new__(cls,*args, **kwargs)

            # 初始化EST SDK
            cls.__instance.rest = REST(serverIP, serverPort, softVersion)
            cls.__instance.rest.setAccount(accountSid, accountToken)
            cls.__instance.rest.setAppId(appId)
        return cls.__instance

    def send_sms(self,to, datas, tempId):

        result = self.rest.sendTemplateSMS(to, datas, tempId)
        if result.get('statusCode') == '000000':
            # 发送成功
            return 0
        else:
            # 发送失败
            return 1


    def sendTemplateSMS(self,to,datas,tempId):
        result = self.rest.sendTemplateSMS(to,datas,tempId)
        for k,v in result.iteritems():

            if k=='templateSMS' :
                    for k,s in v.iteritems():
                        print('%s:%s' % (k, s))
            else:
                print('%s:%s' % (k, v))

# if __name__ == '__main__':
#     cpp = CCP()
#     # 接收手机号     [验证码，时间]      验证id
#     res = cpp.send_sms('18877565220', ['1234','5'], 1)
#     print(res)
