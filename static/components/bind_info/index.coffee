###
#显示bind的信息
###
require './style.less'
error = require 'lib/functions/error.coffee'
toast = require 'lib/functions/toast.coffee'
top_toast = toast.getTopRightToast()

module.exports =
  data:->
    bind_info:
      name:''
      card_number:''
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
            @bind_info = data.data
            console.log data.data
            if ! @bind_info

              $('.small.modal').modal('show')
              console.log 'jump'
            if ! @bind_info.card_number
              console.log 'jump'
