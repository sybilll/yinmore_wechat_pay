#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
xml2json:https://github.com/hay/xml2json
log_debug, print 相当于print
"""

from hashlib import md5
import requests
import time
import os
import json
from xml.etree import ElementTree
from xml2json import xml2json
import optparse

import ConfigParser
config = ConfigParser.ConfigParser()
with open('conf/wechat.ini', 'r') as cfg_file:
    config.readfp(cfg_file)
    appid = config.get('app', 'appid')
    appsecret = config.get('app', 'appsecret')
    token = config.get('app', 'token')
    user_name = config.get('app', 'user_name')
    password = config.get('app', 'password')
    encoding_aes_key = config.get('app', 'encoding_aes_key')
    mch_id = config.get('app', 'mch_id')
    api_key = config.get('app', 'api_key')
    notify_url = config.get('app', 'notify_url')
    domain = config.get('app', 'domain')


class WeiXinPay():

    """微信支付，返回回客户端需要参数
    """

    def __init__(self, out_trade_no, body, total_fee, spbill_create_ip, openid):
        """
        :param out_trade_no: 订单ID
        :param body: 商品描述
        :param total_fee: 订单金额
        :param nonce_str: 32位内随机字符串
        :param spbill_create_ip: 客户端请求IP地址
        """

        # 生生随机字符
        nonce_str = ''.join(map(lambda xx: (hex(ord(xx))[2:]), os.urandom(16)))
        self.params = {
            'appid': appid,
            'mch_id': mch_id,
            'nonce_str': nonce_str,
            'body': body,
            'out_trade_no': str(out_trade_no),
            'total_fee': str(int(total_fee)),
            'spbill_create_ip': spbill_create_ip,
            'trade_type': 'JSAPI',
            'notify_url': notify_url,
            'openid': openid
        }
        #print self.params

        self.url = 'https://api.mch.weixin.qq.com/pay/unifiedorder'  # 微信请求url
        self.error = None

    def key_value_url(self, value):
        """将将键值对转为 key1=value1&key2=value2
        """
        key_az = sorted(value.keys())
        pair_array = []
        for k in key_az:
            v = value.get(k, '').strip()
            v = v.encode('utf8')
            k = k.encode('utf8')
            #print('%s => %s' % (k, v))
            pair_array.append('%s=%s' % (k, v))

        tmp = '&'.join(pair_array)
        #print("key_value_url ==> %s " % tmp)
        return tmp

    def get_sign(self, params):
        """生成sign
        """
        stringA = self.key_value_url(params)
        stringSignTemp = stringA + '&key=' + api_key  # api_key, API密钥，需要在商户后台设置
        #print("stringSignTemp ==> %s" % stringSignTemp)
        sign = (md5(stringSignTemp).hexdigest()).upper()
        params['sign'] = sign
        print("==> %s" % sign)

    def get_req_xml(self):
        """拼接XML
        """
        self.get_sign(self.params)
        xml = "<xml>"
        for k, v in self.params.items():
            v = v.encode('utf8')
            k = k.encode('utf8')
            xml += '<' + k + '>' + v + '</' + k + '>'
        xml += "</xml>"
        #print(xml)
        return xml

    def get_prepay_id(self):
        """
        请求获取prepay_id
        """
        xml = self.get_req_xml()
        headers = {'Content-Type': 'application/xml'}
        r = requests.post(self.url, data=xml, headers=headers, verify=False)
        r.encoding = 'utf-8'
        print(r.text)
        #print("++++++++++++++++++++++++++")
        re_xml = ElementTree.fromstring(r.text.encode('utf8'))
        xml_status = re_xml.getiterator('result_code')[0].text
        #print("result_code ==> %s" % xml_status)
        if xml_status != 'SUCCESS':
            self.error = u"连接微信出错啦！"
            return
        #prepay_id = re_xml.getiterator('prepay_id')[0].text

        options = optparse.Values({"pretty": False})
        xml_json = json.loads(xml2json(r.text.encode('utf8'), options))['xml']

        r_params = {}
        r_params['prepay_id'] = xml_json['prepay_id']
        r_params['appid'] = xml_json['appid']
        r_params['mch_id'] = xml_json['mch_id']
        r_params['nonce_str'] = xml_json['nonce_str']
        r_params['sign'] = xml_json['sign']
        r_params['prepay_id'] = xml_json['prepay_id']

        r_params['paySign'] = xml_json['sign']
        r_params['package'] = 'prepay_id=%s' % xml_json['prepay_id']

        #self.params['prepay_id'] = prepay_id
        ##self.params['package'] = 'Sign=WXPay'
        #self.params['package'] = 'prepay_id=%s' % prepay_id
        #self.params['timestamp'] = str(int(time.time()))
        #self.params['paySign'] = re_xml.getiterator('sign')[0].text

        print r_params
        return r_params

    def re_finall(self):
        """得到prepay_id后再次签名，返回给终端参数
        """
        self.get_prepay_id()
        if self.error:
            return

        sign_again_params = {
            'appid': self.params['appid'],
            'noncestr': self.params['nonce_str'],
            'package': self.params['package'],
            'partnerid': self.params['mch_id'],
            'timestamp': self.params['timestamp'],
            'prepayid': self.params['prepay_id']
        }
        self.get_sign(sign_again_params)
        self.params['sign'] = sign_again_params['sign']

        # 移除其他不需要返回参数
        for i in self.params.keys():
            if i not in [
                'appid', 'mch_id', 'nonce_str',
                         'timestamp', 'sign', 'package', 'prepay_id']:
                self.params.pop(i)

        return self.params


class WeiXinResponse(WeiXinPay):

    """
    微信签名验证
    """

    def __init__(self, xml):
        """
        :param xml: 支付成功回调的XML
        """
        self.xml = xml
        options = optparse.Values({"pretty": False})
        self.xml_json = json.loads(xml2json(self.xml, options))['xml']
        self.sign = self.xml_json.get('sign', '')

    def verify(self):
        """验证签名"""

        self.xml_json.pop('sign')
        self.get_sign(self.xml_json)
        if self.sign != self.xml_json['sign']:
            print("signValue:%s !=  sing:%s" % (self.xml_json['sign'], self.sign))
            return False

        return True

if __name__ == '__main__':
    weixin_pay = WeiXinPay(out_trade_no='b2', body='test', total_fee='100',
                           spbill_create_ip='8.8.8.8', openid='oGXiIwHwx_zB8ekXibYjdt3Xb_fE')

    weixin_pay.get_prepay_id()
