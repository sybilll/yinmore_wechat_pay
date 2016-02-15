require './style.less'
error = require 'lib/functions/error.coffee'
toast = require 'lib/functions/toast.coffee'
top_toast = toast.getTopRightToast()

module.exports =
  data:->
    total_fee:null
    total_fee_error:false
    card_number:null
  template: require('./template.html')
  components:
    'bind_info': require('../bind_info')
    'recharge_info': require('../recharge_info')
  ready:->
    error.setOnErrorVm(@)
  methods:
    setAndPay:(fee)->
      @total_fee = fee
      @pay()
    pay:->
      @loading=true
      if not @total_fee
        @total_fee_error=true
        top_toast.warning "必须填入充值金额"
        return
      if @total_fee <= 0
        @total_fee_error=true
        top_toast.warning "充负数是不可以的"
        return
      if @card_number == null
        throw new Error('没有取到充值卡号，请刷新页面')
      parm = JSON.stringify
        total_fee:@total_fee*100 #后台单位是分
        card_number:@card_number
      $.ajax
        url: '/get_wechat_prepay_id'
        type: 'POST'
        data : parm
        success: (data, status, response) =>
          @loading=false
          if data.error != '0'
            throw new Error(data.error)
          else
            prepay = data.data
            weixin_parm = {
              'appId': prepay.appId
              'timeStamp': prepay.timeStamp
              'nonceStr': prepay.nonceStr
              'package': prepay.package
              'signType': prepay.signType
              'paySign': prepay.paySign
            }
            #alert JSON.stringify(weixin_parm)
            WeixinJSBridge.invoke 'getBrandWCPayRequest', weixin_parm, (res) ->
              alert res.err_msg
              if res.err_msg == 'get_brand_wcpay_request:ok'
                alert '充值成功'
                _.delay(window.recharge_info.getPayInfos, 5000)
              else
                #alert(res.err_code + res.err_desc + res.err_msg)
                console.log(res.err_code + res.err_desc)
              # 使用以上方式判断前端返回,微信团队郑重提示：res.err_msg将在用户支付成功后返回    ok，但并不保证它绝对可靠。 
              return
            #wx.chooseWXPay
            #  appId: prepay.appid
            #  timeStamp: prepay.timestamp
            #  nonceStr: prepay.nonce_str
            #  package: "prepay_id=#{prepay.prepay_id}"
            #  signType: 'MD5'
            #  paySign: prepay.sign
            #  success: (res) ->
            #    if res.errMsg == 'chooseWXPay:ok'
            #      #支付成功
            #    else
            #      alert res.errMsg
            #    return
            #  cancel: (res) ->
            #    #支付取消
            #    return
    cleanError:->
      @total_fee_error=false
      @loading = false
