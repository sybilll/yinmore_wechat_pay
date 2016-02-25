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
      <button @click='setAndPay(500)' class='ui yellow button'>500</button>
      <button @click='setAndPay(1000)' class='ui yellow button'>1000</button>
      <button @click='setAndPay(5000)' class='ui yellow button'>5000</button>
      <form class='ui form'>
        <div v-bind:class="{ 'error': total_fee_error }" class='field'>
          <label></label>
          <input @focus='cleanError' v-model='total_fee' type='number'  placeholder='充值金额'>
        </div>
      </form>
      <div class='ui center aligned basic segment'>
        <button @click='showConfirm' v-bind:class="{ 'disabled': loading, 'loading': loading }" class='ui orange basic button'>
          <i class='yen icon'></i>
          充值
        </button>
      </div>
    </div>
    <pay-info></pay-info>
    <confirm :header="header" :content="content" :call_back="pay"></confirm>
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
  import Confirm from 'lib/components/Confirm.vue'
  export default {
    data: function () {
      return {
        total_fee: null,
        total_fee_error: false
      }
    },
    components: {
      Confirm,
      BindInfo,
      PayInfo
    },
    ready: function () {
      return error.setOnErrorVm(this)
    },
    computed: {
      header () {
        return `确定向该油卡充值${this.total_fee}元？`
      },
      content () {
        return `
            <table class="ui celled striped unstackable table">
              <thead>
                <tr>
                  <th>
                    <i class="user icon"></i>${ this.selected_card.name }
                  </th>
                  <th>
                    <i class="payment icon"></i>${ this.selected_card.card_number }
                  </th>
                </tr>
              </thead>
            </table>
          `
      },
      selected_card () {
        return store.state.selected_card
      }
    },
    methods: {
      showConfirm: function (card) {
        this.$broadcast('confirm')
      },
      setAndPay: function (fee) {
        this.total_fee = fee
        return this.showConfirm()
      },
      pay: function () {
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
        var parm = {
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
