# __author: Lambert
# __date: 2018/6/6 17:12
import hashlib

WPC = {
    'APPID': 'wx21e25187cb87c9f0',
    'APPSECRET': 'fdd177a7xxxxxxxxxxxxx856eeeb187c',
    'MCHID': '14222000000',
    'KEY': 'd7810713e1exxxxxxxxxxadc9617d0a6',
    'GOODDESC': '商户号中的公司简称或全称-无要求的商品名字',
    'NOTIFY_URL': 'https://www.xxxx.com/service/applesson/wechatordernotice',
}


# 获取MD5
def MD5(str):
    md5 = hashlib.md5()
    md5.update(str.encode('utf-8'))
    return md5.hexdigest()
