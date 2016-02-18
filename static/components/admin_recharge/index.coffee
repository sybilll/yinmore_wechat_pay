require './style.less'
error = require 'lib/functions/error.coffee'
toast = require 'lib/functions/toast.coffee'
top_toast = toast.getTopRightToast()

module.exports =
  data:->
    pay_infos:null
    status_desc:
      prepay: '生成订单'
      payed:'已支付'
      recharging:'冲入油卡中...'
      recharged:'已冲入油卡'

  template: require('./template.html')
  ready:->
    error.setOnErrorVm(@)
    @getPayInfos()
    #抛出到全局去污染
    window.recharge_info = @
  methods:
    getPayInfos:->
      $.ajax
        url: '/getAdminPayInfos'
        type: 'POST'
        success: (data, status, response) =>
          if data.error != '0'
            throw new Error(data.error)
          else
            @pay_infos = data.data
