#!/usr/bin/env python
# -*- coding: utf-8 -*-
# sys.setdefaultencoding() does not exist, here!
import json
import public_bz
import sys
import db_bz
import wechat_bz

#import db_bz
import tornado.ioloop
import tornado.web
import tornado_bz
import wechat_oper
from tornado_bz import BaseHandler
#from tornado_bz import UserInfoHandler

#import oper
import pg
import public_db
#import proxy
import web_bz
from wechat_pay import WeiXinPay
try:
    #    from wechat_sdk import WechatBasic
    from wechat_sdk.messages import (
        TextMessage, VoiceMessage, ImageMessage, VideoMessage, LinkMessage, LocationMessage, EventMessage
    )
except ImportError:
    print 'you need install wechat, please run:'
    print 'sudo pip install wechat-sdk'
    exit(1)


reload(sys)
sys.setdefaultencoding('utf-8')

import optparse
options = optparse.Values({"pretty": False})
from xml2json import xml2json
OK = '0'

OPENID = 'oGXiIwHwx_zB8ekXibYjdt3Xb_fE'
OPENID = None


class pay(BaseHandler):

    '''
     后台管理查支付信息
    '''
    @tornado_bz.mustLogin
    @tornado_bz.handleError
    def get(self, parm=None):
        self.set_header("Content-Type", "application/json")
        statuses = None
        user_id = None
        if parm:
            parm = json.loads(parm)
            statuses = parm.get('statuses')
            user_id = parm.get('user_id')
            if user_id:
                user_id = self.get_secure_cookie("user_id")

        pay_infos = public_db.getPayInfo(statuses=statuses, user_id=user_id)
        print pay_infos

        self.write(json.dumps({'error': '0', 'pay_infos': pay_infos}, cls=public_bz.ExtEncoder))

    @tornado_bz.mustLogin
    @tornado_bz.handleError
    def put(self):
        self.set_header("Content-Type", "application/json")
        parm = json.loads(self.request.body)
        id = parm.get('id')
        status = parm.get('status')

        user_id = self.get_secure_cookie("user_id")
        count = self.pg.update('pay', where="id=%s and status<>'%s' " % (id, status), status=status, user_id=user_id)
        if count != 1:
            raise Exception('占位失败')
        self.write(json.dumps({'error': '0'}, cls=public_bz.ExtEncoder))


class getPayInfos(BaseHandler):

    '''
    查出已支付信息
    '''
    @tornado_bz.handleError
    def post(self):
        self.set_header("Content-Type", "application/json")
        openid = self.get_secure_cookie("openid")
        pay_infos = public_db.getPayInfo(openid, ['payed', 'recharging', 'recharged'])

        self.write(json.dumps({'error': '0', 'data': pay_infos}, cls=public_bz.ExtEncoder))


class login(web_bz.login):

    '''
    要用自已的template，得重载
    '''

    def get(self):
        self.render(self.template)


class admin(BaseHandler):

    '''
    后台管理的 create by bigzhu at 16/02/15 16:21:02
    '''

    @tornado_bz.mustLogin
    def get(self):
        self.render(tornado_bz.getTName(self))


class payDone(BaseHandler):

    def post(self):

        self.set_header("Content-Type", "application/json")
        print self.request.body
        json_data = xml2json(self.request.body.encode('utf8'), options)
        data = json.loads(json_data)['xml']
        return_code = data['return_code']
        if return_code == 'SUCCESS':
            openid = data['openid']
            out_trade_no = data['out_trade_no']
            cash_fee = data['cash_fee']
            where = " openid='%s' and id=%s and (status<>'payed' or status is null) " % (openid, out_trade_no)
            from webpy_db import SQLLiteral
            count = pg.update('pay', status='payed', wexin_return=json_data, stat_date=SQLLiteral('NOW()'), where=where)
            if count != 1:
                error_info = 'update failure: count=%s where=%s' % (count, where)
                print error_info
                raise Exception(error_info)
            else:
                wechat = wechat_oper.getWechat()
                content = '''您支付的 %s 元已进入充值系统，正在向您的油卡充值，请耐心等候......''' % (int(cash_fee) / 100.00)
                wechat.send_text_message(openid, content)
        else:
            print data['return_msg']
#{u'openid': u'oGXiIwHwx_zB8ekXibYjdt3Xb_fE', u'trade_type': u'JSAPI', u'cash_fee': u'1', u'nonce_str': u'798243e4902342c83e833c71141385f', u'return_code': u'SUCCESS', u'is_subscribe': u'Y', u'bank_type': u'CFT', u'mch_id': u'1308443701', u'out_trade_no': u'86', u'result_code': u'SUCCESS', u'total_fee': u'1', u'appid': u'wx907d8a3f50de65db', u'fee_type': u'CNY', u'time_end': u'20160215113326', u'transaction_id': u'1002230516201602153283628055', u'sign': u'CAD12073F45232BB600B8F066B434A30'}

        success = '''
        <xml>
          <return_code><![CDATA[SUCCESS]]></return_code>
          <return_msg><![CDATA[OK]]></return_msg>
        </xml>
        '''
        self.write(success)


class get_wechat_prepay_id(BaseHandler):

    '''
    取得统一下单id
    '''
    @tornado_bz.handleError
    def post(self):
        self.set_header("Content-Type", "application/json")
        openid = self.get_secure_cookie("openid")
        #openid = 'oGXiIwHwx_zB8ekXibYjdt3Xb_fE'
        remote_ip = self.request.remote_ip

        data = json.loads(self.request.body)
        total_fee = data['total_fee']
        card_number = data['card_number']

        out_trade_no = pg.db.insert('pay', seqname='pay_id_seq', openid=openid, total_fee=total_fee, card_number=card_number, status='prepay')
        print 'out_trade_no=', out_trade_no

        weixin_pay = WeiXinPay(out_trade_no=out_trade_no, body='英茂油卡冲值:%s' % total_fee, total_fee=total_fee,
                               spbill_create_ip=remote_ip, openid=openid)

        prepay = weixin_pay.get_prepay_id()
        self.write(json.dumps({'error': '0', 'data': prepay}, cls=public_bz.ExtEncoder))


class get_wechat_bind_info(BaseHandler):

    @tornado_bz.handleError
    def post(self):
        self.set_header("Content-Type", "application/json")
        openid = self.get_secure_cookie("openid")
        if OPENID:
            openid = OPENID
        bind_info = public_db.getBindInfoByOpenid(openid)
        if bind_info:
            bind_info = bind_info[0]
        else:
            bind_info = None

        self.write(json.dumps({'error': '0', 'data': bind_info}, cls=public_bz.ExtEncoder))


class save_wechat_bind_info(BaseHandler):

    @tornado_bz.handleError
    def post(self):

        self.set_header("Content-Type", "application/json")
        data = json.loads(self.request.body)

        openid = self.get_secure_cookie("openid")
        #openid = 123
        data['openid'] = openid
        #where = "openid='%s' and card_number='%s' " % (openid, data['card_number'])
        where = "openid='%s' " % openid
        db_bz.insertOrUpdate(pg, 'bind_card_info', data, where)

        self.write(json.dumps({'error': '0'}))


class set_openid(web_bz.set_openid):
    pass


class app(BaseHandler):

    '''
    主程序
    '''

    @wechat_bz.mustSubscribe
    def get(self):
        #openid = self.get_secure_cookie("openid")
        # wechat_oper.addWechatUser(openid)
        # print openid
        self.render(tornado_bz.getTName(self))


class callback(BaseHandler):

    '''
    create by bigzhu at 15/04/02 16:34:53 微信的回调接口
    '''

    def get(self):
        self.write(self.get_argument('echostr'))

    def post(self):
        self.set_header("Content-Type", "application/json")

        wechat = wechat_oper.getWechat()

        wechat.parse_data(self.request.body)
        message = wechat.get_message()

        response = None
        if isinstance(message, TextMessage):
            # count = public_db.updateDescription(openid=message.source, desc=message.content)
            # if count == 1:
            #    response = wechat.response_text(content=u'描述已经添加,感谢您的举报.')
            # else:
            #    response = wechat.response_text(content=u'请先发送需要举报的照片')
            response = wechat.response_text(content=u'文字信息')

        elif isinstance(message, VoiceMessage):
            response = wechat.response_text(content=u'语音信息')
        elif isinstance(message, ImageMessage):

            # 需要下载图片
            def downloadImageFile():
                http_client = tornado.httpclient.AsyncHTTPClient()
                http_client.fetch(message.picurl, callback=done)

            def done(response):
                with open("static/upload/images/" + message.media_id + '.jpg', "w") as f:
                    f.write(response.body)
                print "DONE"
            downloadImageFile()
            # 检查用户是否存储了,没有的话存之
            wechat_user_info = public_db.getWechatUserByOpenid(message.source)
            if wechat_user_info:
                pass
            else:
                wechat_user_info = wechat.get_user_info(message.source)
                pg.db.insert('wechat_user', **wechat_user_info)
            pg.db.insert('upload_info', openid=message.source, media_id=message.media_id)

            response = wechat.response_text(content=u'图片已经保存,请继续向我们发送对图片的描述')
        elif isinstance(message, VideoMessage):
            response = wechat.response_text(content=u'视频信息')
        elif isinstance(message, LinkMessage):
            wechat_user_info = wechat.get_user_info(message.source)
            print wechat_user_info
            response = wechat.response_text(content=u'链接信息')
        elif isinstance(message, LocationMessage):
            response = wechat.response_text(content=u'地理位置信息')
        elif isinstance(message, EventMessage):  # 事件信息
            if message.type == 'subscribe':  # 关注事件(包括普通关注事件和扫描二维码造成的关注事件)
                print message.source
                if message.key and message.ticket:  # 如果 key 和 ticket 均不为空，则是扫描二维码造成的关注事件
                    response = wechat.response_text(content=u'用户尚未关注时的二维码扫描关注事件')
                else:
                    response = wechat.response_text(content=u'普通关注事件')
            elif message.type == 'unsubscribe':
                response = wechat.response_text(content=u'取消关注事件')
            elif message.type == 'scan':
                response = wechat.response_text(content=u'用户已关注时的二维码扫描事件')
            elif message.type == 'location':
                response = wechat.response_text(content=u'上报地理位置事件')
            elif message.type == 'click':
                response = wechat.response_text(content=u'自定义菜单点击事件')
            elif message.type == 'view':
                response = wechat.response_text(content=u'自定义菜单跳转链接事件')

        self.write(response)


if __name__ == "__main__":

    web_class = tornado_bz.getAllWebBzRequestHandlers()
    web_class.update(globals().copy())

    if len(sys.argv) == 2:
        port = int(sys.argv[1])
    else:
        port = 9000
    print port

    url_map = tornado_bz.getURLMap(web_class)
    # 机器人
    url_map.append((r'/robots.txt()', tornado.web.StaticFileHandler, {'path': "./static/robots.txt"}))
    # sitemap
    url_map.append((r'/sitemap.xml()', tornado.web.StaticFileHandler, {'path': "./static/sitemap.xml"}))
    #url_map.append((r'/static/(.*)', tornado.web.StaticFileHandler, {'path': "./static"}))

    url_map.append((r'/', admin))

    settings = tornado_bz.getSettings()
    settings["pg"] = pg
    settings["domain"] = 'yinmore.follow.center'
    settings["appid"] = wechat_oper.appid
    settings["appsecret"] = wechat_oper.appsecret
    settings["wechat"] = wechat_oper.getWechat()

    application = tornado.web.Application(url_map, **settings)

    application.listen(port)
    ioloop = tornado.ioloop.IOLoop().instance()

    tornado.autoreload.start(ioloop)
    ioloop.start()
