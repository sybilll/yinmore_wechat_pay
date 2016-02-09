require './style.less'
error = require 'lib/functions/error.coffee'
toast = require 'lib/functions/toast.coffee'
top_toast = toast.getTopRightToast()

module.exports =
  data:->
    total_fee:null
    total_fee_error:false
  template: require('./template.html')
  components:
    'bind_info': require('../bind_info')
  methods:
    setTotalFee:(fee)->
      @total_fee = fee
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
      parm = JSON.stringify
        total_fee:@total_fee*100 #后台单位是分
        card_number:'数据要传递过来'

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
            WeixinJSBridge.invoke 'getBrandWCPayRequest', {
              'appId': prepay.appid
              'timeStamp': prepay.timestamp
              'nonceStr': prepay.nonce_str
              'package': prepay.package
              'signType': 'MD5'
              'paySign': prepay.sign
            }, (res) ->
              if res.err_msg == 'get_brand_wcpay_request：ok'
              else
              # 使用以上方式判断前端返回,微信团队郑重提示：res.err_msg将在用户支付成功后返回    ok，但并不保证它绝对可靠。 
              return
    cleanError:->
      @total_fee_error=false
      @loading = false

