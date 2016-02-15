###
#显示bind的信息
###
require './style.less'
error = require 'lib/functions/error.coffee'
toast = require 'lib/functions/toast.coffee'
top_toast = toast.getTopRightToast()

module.exports =
  props: ['card_number']
  data:->
    bind_info:
      name:''
      card_number:''
  template: require('./template.html')
  ready:->
    error.setOnErrorVm(@)
    @getBindInfo()
  methods:
    jump:->
      window.location.hash = '#!/card_manager'
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
              @card_number = @bind_info.card_number
            else
              $('.small.modal').modal('show')
            #if ! @bind_info.card_number
            #  console.log 'jump'
