#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pg
import user_bz
import db_bz
#import time_bz
user_oper = user_bz.UserOper(pg)


def getPayInfo(openid=None, statuses=None, user_id=None):
    sql = '''
    select id, card_number, stat_date, card_number, total_fee, status from pay
        where 1=1
    '''
    if openid:
        sql += " and openid='%s' " % openid
    if statuses:
        in_statuses = db_bz.formatToInSql(statuses)
        sql += " and status in (%s) " % in_statuses
    if user_id:
        sql += " and user_id=%s " % user_id
    sql += " order by created_date desc "
    return list(pg.query(sql))


def getLast(user_id):
    if user_id is None:
        return
    result = list(pg.select('last', where="user_id=%s" % user_id))
    if result:
        return result[0]


def delNoName(type, name):
    sql = '''
    update user_info set %s=null where lower(%s)=lower('%s')
    ''' % (type, type, name)
    pg.query(sql)
    print 'del', type, name


def getOpenidsByName(type, name):
    sql = '''
        select w.openid from user_info u, follow_who f, user_info u2, wechat_user w
        where lower(u.%s)=lower('%s')
        and u.id = f.god_id
        and u2.id = f.user_id
        and w.user_name=u2.user_name
    ''' % (type, name)
    return pg.query(sql)


def followedWho(user_id):
    sql = '''
        select god_id from follow_who where user_id=%s
    ''' % user_id
    return pg.query(sql)


def getWechatUserByOpenid(openid):
    '''
    create by bigzhu at 15/04/04 12:48:58 根据 openid 来查询微信用户
    '''
    return list(pg.select('wechat_user', where="openid='%s'" % openid))


def getBindInfoByOpenid(openid):
    sql = '''
        select b.openid,
            b.card_number,
            b.car_number,
            b.car_type,   -- 车型
            b.phone_number, -- 手机号
            b.name,  -- 姓名
            b.id_number   -- 身份证号
         from bind_card_info b
         where b.openid='%s'
    ''' % openid
    return pg.query(sql)


def getWechatUserBindInfoByOpenid(openid):
    '''
    查出用户信息
    '''
    sql = '''
        select w.openid,
            w.id as wechat_user_id,
            b.card_number,
            b.car_number,
            b.car_type,   -- 车型
            b.phone_number, -- 手机号
            b.name,  -- 姓名
            b.id_number   -- 身份证号
         from wechat_user w left join bind_card_info b
        on w.id = b.wechat_user_id
        where w.openid='%s'
    ''' % openid
    return pg.query(sql)
if __name__ == '__main__':
    pass
