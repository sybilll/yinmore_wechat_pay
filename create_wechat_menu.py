#!/usr/bin/env python
# -*- coding: utf-8 -*-
import wechat_oper
if __name__ == '__main__':
    wechat = wechat_oper.getWechat()
    menu_data = {
        'button': [
            {
                'type': 'view',
                'name': '油卡冲值',
                'url': 'http://yinmore.follow.center/app'
            },
            {
                'type': 'view',
                'name': '油卡管理',
                'url': 'http://yinmore.follow.center/app#!/card_manager/'
            },
        ]
    }
    print wechat.create_menu(menu_data)
