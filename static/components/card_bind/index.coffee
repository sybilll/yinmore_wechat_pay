require './style.less'
error = require 'lib/functions/error.coffee'
toast = require 'lib/functions/toast.coffee'
top_toast = toast.getTopRightToast()

module.exports =
  data:->
    card_number_error:false
    name_error:false
    phone_number_error:false
    id_number_error:false

    bind_info:
      name:''
      car_type:"私家车"
    loading: false
    disable_edit: true # 禁止编辑
    button_text:'修改资料'
  directives:
    disable: require 'lib/directives/disable'
  template: require('./template.html')
  ready:->
    error.setOnErrorVm(@)
    @getBindInfo()
  methods:
    getBindInfo:->
      $.ajax
        url: '/get_wechat_bind_info'
        type: 'POST'
        success: (data, status, response) =>
          if data.error != '0'
            throw new Error(data.error)
          else
            if data.data
              @bind_info = data.data
              @disable()
            else
              @enable()
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
        if not @bind_info.card_number
          @card_number_error=true
          top_toast.warning "必须填入加油卡卡号"
          return
        if not @bind_info.name
          @name_error=true
          top_toast.warning "必须填入持卡人姓名"
          return
        if not @bind_info.id_number
          @id_number_error=true
          top_toast.warning "必须填入身份证号码"
          return
        if @bind_info.id_number.trim().length != 18
          @id_number_error=true
          top_toast.warning "请输入正确的18位身份证号码"
          return
        if not @bind_info.phone_number
          @phone_number_error=true
          top_toast.warning "必须填入手机号"
          return

        @loading=true
        parm = JSON.stringify
          card_number:@bind_info.card_number
          car_number:@bind_info.car_number
          car_type:@bind_info.car_type
          phone_number:@bind_info.phone_number
          name:@bind_info.name
          id_number:@bind_info.id_number
        console.log parm
        $.ajax
          url: '/save_wechat_bind_info'
          type: 'POST'
          data : parm
          success: (data, status, response) =>
            @loading=false
            if data.error != '0'
              throw new Error(data.error)
            else
              @disable()
              top_toast["info"] "保存成功"
    cleanError:->
      @card_number_error=false
      @name_error=false
      @phone_number_error=false
      @id_number_error=false
      @loading = false
