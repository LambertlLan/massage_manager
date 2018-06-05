# 接口类型：互亿无线触发短信接口，支持发送验证码短信、订单通知短信等。
# 账户注册：请通过该地址开通账户http://user.ihuyi.com/register.html
# 注意事项：
# （1）调试期间，请使用用系统默认的短信内容：您的验证码是：【变量】。请不要把验证码泄露给其他人。
# （2）请使用 APIID 及 APIKEY来调用接口，可在会员中心获取；
# （3）该代码仅供接入互亿无线短信接口参考使用，客户可根据实际需要自行编写；

# !/usr/local/bin/python
# -*- coding:utf-8 -*-
import http.client
from urllib import parse

host = "106.ihuyi.com"
sms_send_uri = "/webservice/sms.php?method=Submit"

# 查看用户名 登录用户中心->验证码通知短信>产品总览->API接口信息->APIID
account = "cf_10novo"
# 查看密码 登录用户中心->验证码通知短信>产品总览->API接口信息->APIKEY
password = "4eb7c5687a356a473794822a3b607972"
# 短信模板
msg_template = "您的动态校验码是：【变量】。工作人员不会向您索要，请勿向任何人泄露。"


def send_sms(mobile, code):
    params = parse.urlencode(
        {'account': account, 'password': password, 'content': get_text(code), 'mobile': mobile, 'format': 'json'})
    headers = {"Content-type": "application/x-www-form-urlencoded", "Accept": "text/plain"}
    conn = http.client.HTTPConnection(host, port=80, timeout=30)
    conn.request("POST", sms_send_uri, params, headers)
    response = conn.getresponse()
    response_str = response.read()
    conn.close()
    return response_str


def get_text(code):
    return f"您的动态校验码是：【{code}】。工作人员不会向您索要，请勿向任何人泄露。"


if __name__ == '__main__':
    mobile = "18280443179"
    text = "您的动态校验码是：【变量】。工作人员不会向您索要，请勿向任何人泄露。"
