<style lang='less'>
  .container {
    border: 1px solid #00f
  }
  .red {
    color: #f00
  }
</style>

<template>
  <div>
    <bind-info :card_number.sync='card_number' ></bind-info>

    <div class='ui center aligned segment'>
      <h4 class='ui header'>请选择/填入充值金额</h4>
      <div @click='setAndPay(500)' class='ui yellow button'>500</div>
      <div @click='setAndPay(1000)' class='ui yellow button'>1000</div>
      <div @click='setAndPay(5000)' class='ui yellow button'>5000</div>
      <form class='ui form'>
        <div v-bind:class="{ 'error': total_fee_error }" class='field'>
          <label></label>
          <input @focus='cleanError' v-model='total_fee' type='number'  placeholder='充值金额'>
        </div>
      </form>
      <div class='ui center aligned basic segment'>
        <button @click='pay' v-bind:class="{ 'disabled': loading, 'loading': loading }" class='ui orange basic button'>
          <i class='yen icon'></i>
          充值
        </button>
      </div>
    </div>
    <recharge_info></recharge_info>
  </div>
</template>

<script>
  var error, toast, top_toast, WeixinJSBridge

  error = require('lib/functions/error.coffee')

  toast = require('lib/functions/toast.coffee')

  top_toast = toast.getTopRightToast()
  // import store from '../store'
  import $ from 'jquery'
  import _ from 'underscore'
  import BindInfo from './BindInfo.vue'
  export default {
    data: function () {
      return {
        total_fee: null,
        total_fee_error: false,
        card_number: null
      }
    },
    components: {
      BindInfo,
      'recharge_info': require('../../../static/components/recharge_info')
    },
    ready: function () {
      return error.setOnErrorVm(this)
    },
    methods: {
      setAndPay: function (fee) {
        this.total_fee = fee
        return this.pay()
      },
      pay: function () {
        var parm
        this.loading = true
        if (!this.total_fee) {
          this.total_fee_error = true
          top_toast.warning('必须填入充值金额')
          return
        }
        if (this.total_fee <= 0) {
          this.total_fee_error = true
          top_toast.warning('充负数是不可以的')
          return
        }
        if (this.card_number === null) {
          throw new Error('没有取到充值卡号，请刷新页面')
        }
        parm = JSON.stringify(
          {
            total_fee: this.total_fee * 100,
            card_number: this.card_number
          }
        )
        return $.ajax(
          {
            url: '/get_wechat_prepay_id',
            type: 'POST',
            data: parm,
            success: (
              function (_this) {
                return function (data, status, response) {
                  var prepay, weixin_parm
                  _this.loading = false
                  if (data.error !== '0') {
                    throw new Error(data.error)
                  } else {
                    prepay = data.data
                    weixin_parm = {
                      'appId': prepay.appId,
                      'timeStamp': prepay.timeStamp,
                      'nonceStr': prepay.nonceStr,
                      'package': prepay['package'],
                      'signType': prepay.signType,
                      'paySign': prepay.paySign
                    }
                    WeixinJSBridge.invoke(
                      'getBrandWCPayRequest', weixin_parm, function (res) {
                        if (res.err_msg === 'get_brand_wcpay_request:ok') {
                          _.delay(window.recharge_info.getPayInfos, 3000)
                        } else {
                          console.log(res.err_code + res.err_desc)
                        }
                      }
                    )
                  }
                }
              }
            )(this)
          }
        )
      },
      cleanError: function () {
        this.total_fee_error = false
        this.loading = false
      }
    }
  }
</script>
