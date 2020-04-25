#coding=gbk

#coding=utf-8

#-*- coding: UTF-8 -*-  

from ihome.libs.yuntongxun.CCPRestSDK import REST
# import ConfigParser

# ���ź�
accountSid= '8aaf07087051bcec01707b228070177b'

# ���˺�token
accountToken= '6b9407c4d36f48a49768483455380f48'

# Ӧ��Id
appId='8aaf07087051bcec01707b2280d91781'

# �����ַ����ʽ���£�����Ҫдhttp://
serverIP='app.cloopen.com'

# ����˿�
serverPort='8883'

# REST�汾��
softVersion='2013-12-26'

class CCP(object):
    """�Լ���װ�ķ��Ͷ��ŵĸ�����"""
    # ������������������
    __instance=None
    def __new__(cls, *args, **kwargs):
        if cls.__instance is None:
            # �ж�cpp����û���Ѿ������Ķ������û�д���һ�����󣬲��ұ���
            # ����з��ر���Ķ���
            cls.__instance=super(CCP, cls).__new__(cls,*args, **kwargs)

            # ��ʼ��EST SDK
            cls.__instance.rest = REST(serverIP, serverPort, softVersion)
            cls.__instance.rest.setAccount(accountSid, accountToken)
            cls.__instance.rest.setAppId(appId)
        return cls.__instance

    def send_sms(self,to, datas, tempId):

        result = self.rest.sendTemplateSMS(to, datas, tempId)
        if result.get('statusCode') == '000000':
            # ���ͳɹ�
            return 0
        else:
            # ����ʧ��
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
#     # �����ֻ���     [��֤�룬ʱ��]      ��֤id
#     res = cpp.send_sms('18877565220', ['1234','5'], 1)
#     print(res)
