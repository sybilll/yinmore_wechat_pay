require './style.less'
error = require 'lib/functions/error.coffee'
toast = require 'lib/functions/toast.coffee'
top_toast = toast.getTopRightToast()

module.exports =
  data:->
    pay_infos:null
    pay_info_rechargings:null
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
      parm = {parm: parm}
      @resource.get(parm).then((response) =>
        if response.data.error != '0'
          throw new Error(response.data.error)
        @pay_info_rechargings = response.data.pay_infos
      )
    changeStatus:(pay_info)->
      if pay_info.status == 'payed'
        @updateToRecharging(pay_info)
    updateToRecharging:(pay_info)->
      parm = JSON.stringify
        id:pay_info.id
      @resource.update(parm).then((response) ->
        console.log response.data
        if response.data.error != '0'
          top_toast.warning(response.data.error)
      )
