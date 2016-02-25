require './style.less'
error = require 'lib/functions/error.coffee'
toast = require 'lib/functions/toast.coffee'
top_toast = toast.getTopRightToast()

module.exports =
  data:->
    pay_infos:null
    pay_info_rechargings:null
    current_recharged:
      card_number:0
      total_fee:0
    status_desc:
      prepay: '生成订单'
      payed:'已支付'
      recharging:'冲入油卡中...'
      recharged:'已冲入油卡'

  template: require('./template.html')
  ready:->
    error.setOnErrorVm(@)
    @resource = @$resource('/pay{/parm}')
    @getPayInfos()
    @getPayInfosRecharging()
    #抛出到全局去污染
    window.recharge_info = @
    window.setInterval(@getPayInfos, 10000)
  methods:
    getPayInfos:->
      parm = JSON.stringify
        statuses:'payed'
      parm = {parm: parm}
      @resource.get(parm).then((response) =>
        if response.data.error != '0'
          throw new Error(response.data.error)
        @pay_infos = response.data.pay_infos
      )
    getPayInfosRecharging:->
      parm = JSON.stringify
        statuses:'recharging'
        user_id:'need'
      parm = {parm: parm}
      @resource.get(parm).then((response) =>
        if response.data.error != '0'
          throw new Error(response.data.error)
        @pay_info_rechargings = response.data.pay_infos
      )
    changeStatus:(pay_info)->
      if pay_info.status == 'payed'
        @updatePay(pay_info, 'recharging')
      if pay_info.status == 'recharging'
        @current_recharged = pay_info
        $('.small.modal').modal('show')
    updatePay:(pay_info, status)->
      parm = JSON.stringify
        id:pay_info.id
        status:status
      @resource.update(parm).then((response) =>
        if response.data.error != '0'
          top_toast.warning(response.data.error)
        else
          @getPayInfosRecharging()
          @getPayInfos()
          top_toast.info('操作成功')
      )
