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
    <bind-info></bind-info>

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
    <pay-info></pay-info>
  </div>
</template>

<script>
  var error, toast, top_toast

  error = require('lib/functions/error.coffee')

  toast = require('lib/functions/toast.coffee')

  top_toast = toast.getTopRightToast()
  import store from '../store'
  import BindInfo from './BindInfo.vue'
  import PayInfo from './PayInfo.vue'
  export default {
    data: function () {
      return {
        total_fee: null,
        total_fee_error: false
      }
    },
    components: {
      BindInfo,
      PayInfo
    },
    ready: function () {
      return error.setOnErrorVm(this)
    },
    computed: {
      selected_card () {
        return store.state.selected_card
      }
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
        if (!store.state.selected_card.card_number) {
          throw new Error('没有取到充值卡号，请刷新页面')
        }
        parm = {
          total_fee: this.total_fee * 100,
          card_number: store.state.selected_card.card_number
        }
        store.actions.weixinPay(parm)
      },
      cleanError: function () {
        this.total_fee_error = false
        this.loading = false
      }
    }
  }
</script>
