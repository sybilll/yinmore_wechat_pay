#! /bin/bash
npm run build
scp ./dist/build.js 112.74.97.194:/home/bigzhu/yinmore_wechat_pay/spa/dist/
