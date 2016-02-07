#require './app.less'
Vue = require './vue_local.coffee'

error = require 'lib/functions/error.coffee'
user_info = require 'lib/functions/user_info.coffee'
v_header = new Vue
  created:->
    error.setOnErrorVm(@)
    if user_info.isLogin()
      @nav_links.push(
        {
          name:'退出'
          href:'/logout'
          target:''
        }
      )

  data:->
    navbar_header:
      name:'Follow Center'
      href:'/'
    nav_links:[
      {
        name:'Changelog'
        href:'/Changelog'
        target:''
      }
      {
        name:'云南程序员'
        href:'http://yncoder.github.io/'
        target:'_blank'
      }
    ]
  el:'#v_header'
  components:
    'vnav': require('lib/components/nav-bz')
