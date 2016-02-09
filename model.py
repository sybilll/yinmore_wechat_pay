#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
初始化数据库
'''
import model_oper_bz
from peewee import TextField, IntegerField, DateTimeField
from playhouse.postgres_ext import JSONField
#import user_bz
import public_bz

project_name = public_bz.getProjectName()
db_name = project_name

import ConfigParser
config = ConfigParser.ConfigParser()
with open('conf/db.ini', 'r') as cfg_file:
    config.readfp(cfg_file)
    host = config.get('db', 'host')
    port = config.get('db', 'port')
    the_db = config.get('db', 'db')
    user = config.get('db', 'user')
    pw = config.get('db', 'pw')


class wechat_dead_line(model_oper_bz.base):

    '''
    记录wechat的超时时间,以决定要不要新建
    modify by bigzhu at 15/09/13 17:49:27 加入对wechat_ext的支持
    '''
    jsapi_ticket = TextField(null=True)
    jsapi_ticket_expires_at = DateTimeField(null=True)
    access_token = TextField(null=True)
    access_token_expires_at = DateTimeField(null=True)
    token = TextField(null=True)
    cookies = TextField(null=True)


class wechat_user(model_oper_bz.base):

    '''
    create by bigzhu at 15/04/04 13:30:57 记录微信用户的信息
    '''

    subscribe = IntegerField()  # 用户是否订阅该公众号标识，值为0时，代表此用户没有关注该公众号，拉取不到其余信息。
    openid = TextField()  # 用户的标识，对当前公众号唯一
    nickname = TextField()  # 用户的昵称
    sex = IntegerField()  # 用户的性别，值为1时是男性，值为2时是女性，值为0时是未知
    city = TextField()  # 用户所在城市
    country = TextField()  # 用户所在国家
    province = TextField()  # 用户所在省份
    language = TextField()  # 用户的语言，简体中文为zh_CN
    headimgurl = TextField(null=True)  # 用户头像，最后一个数值代表正方形头像大小（有0、46、64、96、132数值可选，0代表640*640正方形头像），用户没有头像时该项为空。若用户更换头像，原有头像URL将失效。
    subscribe_time = IntegerField()  # 用户关注时间，为时间戳。如果用户曾多次关注，则取最后关注时间
    unionid = TextField(null=True)  # 只有在用户将公众号绑定到微信开放平台帐号后，才会出现该字段。详见：获取用户个人信息（UnionID机制）
    remark = TextField()  # 不知道是什么
    groupid = IntegerField()  # 突然出现的


class bind_card_info(model_oper_bz.base):

    '''
    绑定的油卡信息 create by bigzhu at 16/02/09 00:42:55
    '''
    card_number = TextField()  # 加油卡卡号
    car_number = TextField(null=True)  # 车牌号
    car_type = TextField(null=True)  # 车型
    phone_number = TextField(null=True)  # 手机号
    name = TextField(null=True)  # 姓名
    id_number = TextField(null=True)  # 身份证号
    openid = TextField()  # wechat openid


class upload_info(model_oper_bz.base):
    openid = TextField()  # 用户的标识，对当前公众号唯一
    description = TextField(null=True)  # 客户的描述
    group_name = TextField()
    user_id = IntegerField(null=True)  # 审核通过的管理员 id
    stat = IntegerField(null=True)  # 1 审核通过 2 审核不通过
    files = JSONField()  # 上传的图片，只存储名字，不存储路径


class vote(model_oper_bz.base):
    openid = TextField()  # 用户的标识，对当前公众号唯一
    upload_info_id = IntegerField()  # 作品的 id


class hits(model_oper_bz.base):
    openid = TextField()  # 用户标识
    path = TextField()  # 访问的url路径


if __name__ == '__main__':
    #import user_bz
    # user_bz.createTable(db_name)
    # 需要用户登录模块
    # user_bz.createTable(db_name)
    #model_oper_bz.dropTable(hits, db_name)
    #model_oper_bz.createTable(hits, db_name)
    #model_oper_bz.dropTable(upload_info, db_name)
    #model_oper_bz.dropTable(vote, db_name)
    #model_oper_bz.dropTable(hits, db_name)
    #model_oper_bz.createAllTable(globals(), db_name, user=user, password=pw, host=host)
    model_oper_bz.reCreateTable(bind_card_info, db_name, user=user, password=pw, host=host)

