#require './app.less'
Vue = require './vue_local.coffee'
error = require 'lib/functions/error.coffee'
v_login_messages = new Vue
  created:->
    error.setOnErrorVm(@)
  el:'#login'
  components:
    'main-login': require('lib/components/main-login')
