#!/usr/bin/env python
# -*- coding: utf-8 -*-
import db_bz
import pg
import public_db
import base64
import time_bz


def getGodSocialInfo(god):
    '''
    create by bigzhu at 15/11/27 10:37:14 取社交信息
    '''
    god.twitter_user = public_db.getTwitterUser(god.twitter)
    god.github_user = public_db.getGithubUser(god.github)
    god.instagram_user = public_db.getInstagramUser(god.instagram)
    god.tumblr_user = public_db.getTumblrUser(god.tumblr)
    return god

def isHaveGoodSocial(god):
    count = 0
    if god.twitter_user:
        count += god.twitter_user.followers_count
    if god.github_user:
        count += god.github_user.followers
    if god.instagram_user:
        count += god.instagram_user.counts.get('followed_by', 0)
    if god.tumblr_user:
        count += god.tumblr_user.likes
    if count >1000:
        return True
    else:
        return False

def getGods(user_id, recommand=False):
    '''
    create by bigzhu at 15/07/12 23:43:54 显示所有的大神, 关联twitter
    modify by bigzhu at 15/07/17 15:20:26 关联其他的,包括 github
    modify by bigzhu at 15/08/28 17:05:54 可以查出没关注的,和随机的
    modify by bigzhu at 16/01/27 17:15:15 过滤出满足条件的
    '''
    gods = list(public_db.getGodInfoFollow(user_id, recommand=recommand))
    #will_del = []
    have_social_gods = []
    for god in gods:
        god = getGodSocialInfo(god)
        if isHaveGoodSocial(god):
            have_social_gods.append(god)
    return have_social_gods


def getGodInfo(god_name, user_id=None):
    '''
    create by bigzhu at 15/11/27 10:31:48 查某个god
    '''

    gods = list(public_db.getGodInfoFollow(user_id, god_name=god_name))
    if gods:
        god = gods[0]
    else:
        raise Exception('没有查到god:' + god_name)
    god = getGodSocialInfo(god)
    return god


def saveLast(last_message_id, user_id):
    '''
    create by bigzhu at 15/08/16 16:22:39 保存最后一条的message
    '''
    #last_time = int(last_time)
    #datetime_last_time = time_bz.timestampToDateTime(last_time, millisecond=True)
    id = db_bz.insertIfNotExist(pg, 'last', {'user_id': user_id, 'last_message_id': last_message_id}, "user_id=%s" % user_id)
    if id is None:
        count = pg.update('last', where='last_message_id< %s and user_id=%s' % (last_message_id, user_id), last_message_id=last_message_id)
        return count
    return 1


def follow(user_id, god_id, make_sure=True):
    '''
    create by bigzhu at 15/07/15 14:22:51
    modify by bigzhu at 15/07/15 15:00:28 如果不用告警,就不要make_sure
    '''
    id = db_bz.insertIfNotExist(pg, 'follow_who', {'user_id': user_id, 'god_id': god_id}, "user_id=%s and god_id=%s" % (user_id, god_id))
    if id is None and make_sure:
        raise Exception('没有正确的Follow, 似乎已经Follow过了呢')


def getMessages(limit=None, current_user=None, god_name=None, offset=None, last_time=None):
    '''
    create by bigzhu at 15/08/03 13:24:39 分页方式取messages
    '''
    anchor = ''
    if limit is None:
        limit = 20
        more = 40
    messages = list(public_db.getMessages(current_user, limit=limit, god_name=god_name, offset=offset, last_time=last_time))
    if messages:
        anchor_message = messages[-1]
        anchor = '%s_%s' % (anchor_message.m_type, anchor_message.id)
        more = int(limit) + 20
    return messages, more, anchor


def makeSurePicture(user_info):
    '''
    create by bigzhu at 15/08/03 16:31:00 从各种用户里找头像
    modify by bigzhu at 15/08/03 16:58:52 同时把描述也找了
    '''
    if user_info.picture:
        return

    github_user = public_db.getGithubUser(user_info.user_name)
    if github_user:
        user_info.picture = github_user.avatar_url
        return
    twitter_user = public_db.getTwitterUser(user_info.user_name)
    if twitter_user:
        user_info.picture = twitter_user.profile_image_url_https
        if not user_info.slogan:
            user_info.slogan = twitter_user.description
        return
    instagram_user = public_db.getInstagramUser(user_info.user_name)
    if instagram_user:
        user_info.picture = instagram_user.profile_picture
        return


def encodeUrl(url):
    '''
    create by bigzhu at 15/08/07 10:37:21 加密url
    modify by bigzhu at 15/08/08 19:47:32 加密时会带上换行,要去了, 否则微信会打不开
    '''
    return base64.encodestring(base64.encodestring(url).replace('\n', '')).replace('\n', '')


def decodeUrl(url):
    return base64.decodestring(base64.decodestring(url))

if __name__ == '__main__':
    print decodeUrl("YUhSMGNEb3ZMM0JvYjNSdmN5MW9MbUZyTG1sdWMzUmhaM0poYlM1amIyMHZhSEJvYjNSdmN5MWhheTE0WVdZeEwzUTFNUzR5T0RnMUxURTVMM014TlRCNE1UVXdMekV4TXpjMU9ESTBYekUwTlRBMU5UZ3lNalV5TlRJM09ETmZNVGcwTnpVeU5UYzJNbDloTG1wd1p3PT0=")
    pass
