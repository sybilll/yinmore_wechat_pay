<style lang="less">
</style>

<template>
  <table class="ui celled striped unstackable table">
    <thead>
      <tr>
        <th>
          流水
        </th>
        <th>
          <i class="payment icon"></i> 油卡
        </th>
        <th>
          <i class="yen icon"></i> 金额
        </th>
        <th>
          时间
        </th>
        <th>
          状态
        </th>
      </tr>
    </thead>
    <tbody>
      <tr v-for="pay_info in pay_infos">
        <td>{{pay_info.id}}</td>
        <td>{{pay_info.card_number}}</td>
        <td>{{pay_info.total_fee/100}}</td>
        <td>{{ pay_info.date}}</td>
        <td>{{ status_desc[pay_info.status] }}</td>
      </tr>
    </tbody>
  </table>
</template>

<script>
  var error = require('lib/functions/error.coffee')
  import store from '../store'
  export default {
    data: function () {
      return {
        status_desc: {
          payed: '已支付',
          recharging: '冲入油卡中...',
          recharged: '已冲入油卡'
        }
      }
    },
    computed: {
      pay_infos () {
        return store.state.pay_infos
      }
    },
    ready: function () {
      error.setOnErrorVm(this)
      store.actions.queryPayInfos()
    },
    methods: {
    }
  }
</script>
