require './style.less'
module.exports =
  data:->
    user_info:
      user_name='bigzhu'
    loading: false
    disable_edit: true # 禁止编辑
    button_text:'修改资料'
  directives:
    disable: require 'lib/directives/disable'
  template: require('./template.html')
  ready:->
    if ! @user_info.card_number
      @enable()
  methods:
    enable:->
        @disable_edit = false
        $(@$el).find(".basic.button").html('<i class="icon save"></i>保存')
    disable:->
        @disable_edit=true
        $(@$el).find(".basic.button").html('<i class="icon file text"></i>编辑')
    save:->
      if @disable_edit
        @enable()
      else
        @loading=false
        @disable()
        parm = JSON.stringify
          user_name:@user_info.user_name
          blog:@user_info.blog
          twitter:@user_info.twitter
          github:@user_info.github
          instagram:@user_info.instagram
          slogan:@user_info.bio
          picture:@user_info.picture
        #$.ajax
        #  url: '/add'
        #  type: 'POST'
        #  data : parm
        #  success: (data, status, response) =>
        #    if data.error != '0'
        #      throw new Error(data.error)
        #    else
        #      top_toast["info"] "保存成功"
        #      if @is_my #如果改的是自已的，那么要吧localstorage的内容也要update
        #        localStorage.user_info = JSON.stringify(@user_info)
