# __author: Lambert
# __date: 2018/6/6 17:12
import hashlib
import requests
import time
import xmltodict

from user_manager.views import GetMsgCode



WPC = {
    'APPID': 'xxxxxxxxxxxx',
    'APPSECRET': 'xxxxxxxxxxxxxxxx',
    'MCHID': 'xxxxxxxxxxxxxxxxx',
    'KEY': 'xxxxxxxxxxxxxxxxxxxxxxxxxx',
    'GOODDESC': '商户号中的公司简称或全称-无要求的商品名字',
    # 'NOTIFY_URL': 'http://16313t6p27.iok.la:39865/recharge/pay_success/',
    'NOTIFY_URL': 'xxxxxxxxxxxxxxxxxxxxxxxxxx',
}

# 获取MD5
def MD5(str):
    md5 = hashlib.md5()
    md5.update(str.encode('utf-8'))
    return md5.hexdigest()


class WxPay(object):
    def wx_create_order(self, openid, order_number, user_ip, price, res_json):
        """微信下单接口"""
        unifie_order_request = dict()

        unifie_order_request.update({
            'appid': WPC["APPID"],  # 公众账号ID
            'body': '私派充值中心-会员充值',  # 商品描述
            'mch_id': WPC["MCHID"],  # 商户号:深圳市泽慧文化传播有限公司
            'nonce_str': '',  # 随机字符串
            'notify_url': WPC["NOTIFY_URL"],  # 微信支付结果异步通知地址
            'openid': '',  # trade_type为JSAPI时，openid为必填参数！此参数为微信用户在商户对应appid下的唯一标识, 统一支付接口中，缺少必填参数openid！
            'out_trade_no': '',  # 商户订单号
            'spbill_create_ip': '',  # 终端IP
            'total_fee': '',  # 标价金额
            'trade_type': 'JSAPI',  # 交易类型
        })
        unifie_order_request['nonce_str'] = self.getnoncestr()
        unifie_order_request['openid'] = openid
        unifie_order_request['out_trade_no'] = unifie_order_request['mch_id'] + '-' + str(order_number)  # 内部订单号码
        unifie_order_request['spbill_create_ip'] = user_ip
        unifie_order_request['total_fee'] = int(price * 100)
        # 签名并生成xml
        xml = self.get_xml(unifie_order_request)

        resp = requests.post("https://api.mch.weixin.qq.com/pay/unifiedorder", data=xml.encode('utf-8'),
                             headers={'Content-Type': 'text/xml'})
        msg = resp.text.encode('ISO-8859-1').decode('utf-8')
        xml_resp = xmltodict.parse(msg)

        if xml_resp['xml']['return_code'] == 'SUCCESS':
            prepay_id = xml_resp['xml']['prepay_id']
            timestamp = str(int(time.time()))
            data = dict()
            data.update({
                "appId": xml_resp['xml']['appid'],
                "nonceStr": xml_resp['xml']['nonce_str'],
                "package": "prepay_id=" + prepay_id,
                "signType": "MD5",
                "timeStamp": timestamp
            })
            data['paySign'] = self.get_sign(data)
            res_json["results"] = data
        else:
            msg = xml_resp['xml']['err_code_des']
            res_json["code"] = 1
            res_json["msg"] = msg

        return res_json

    @staticmethod
    def getnoncestr():
        """生成随机数字符串"""
        return GetMsgCode.create_msg_code()

    @staticmethod
    def get_sign(kwargs):
        # 计算签名
        keys, paras = sorted(kwargs), []
        paras = ['{}={}'.format(key, kwargs[key]) for key in keys if key != 'appkey']  # and kwargs[key] != '']
        string_a = '&'.join(paras)

        string_sign_temp = string_a + '&key=' + WPC['KEY']
        sign = MD5(string_sign_temp).upper()

        return sign

    def get_xml(self, kwargs):
        kwargs['sign'] = self.get_sign(kwargs)

        # 生成xml
        xml = ''
        for key, value in kwargs.items():
            xml += '<{0}>{1}</{0}>'.format(key, value)
        xml = '<xml>{0}</xml>'.format(xml)

        return xml
