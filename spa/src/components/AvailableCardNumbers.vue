<style lang="less">
  .remove.icon {
    color:red;
    font-size:1.5em;
  }
  img {
    width: 100%;
  }
</style>

<template>
  <div>
    <table class="ui celled striped unstackable table">
      <thead>
        <tr>
          <th>
            <i class="payment icon"></i>卡号
          </th>
          <th>
            删除
          </th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="card in available_card_numbers">
          <td>{{card.card_number}}</td>
          <td><a @click="showConfirm(card)" href="javascript:;"><i class="remove icon"></i></a></td>
        </tr>
      </tbody>
    </table>
    <div id="card_no_bind_waring" class="ui small modal">
      <i @click="jump" class="close icon"></i>
      <img src="/static/images/warning.png">
    </div>
    <confirm header="是否删除该油卡？" :content="content" :call_back="delete"></confirm>
  </div>
</template>

<script>
  var error = require('lib/functions/error.coffee')

  import store from '../store'
  import Confirm from 'lib/components/Confirm.vue'
  export default {
    data: function () {
      return {
        remove_card: {}
      }
    },
    components: {
      Confirm
    },
    computed: {
      content () {
        return `
        <table class="ui celled striped unstackable table">
        <thead>
        <tr>
        <th>
        <i class="payment icon"></i>${ this.remove_card.card_number }
        </th>
        </tr>
        </thead>
        </table>
        `
      },
      available_card_numbers () {
        return store.state.available_card_numbers
      }
    },
    ready: function () {
      store.actions.queryAvailableCardNumbers()
    },
    methods: {
      showConfirm: function (card) {
        this.remove_card = card
        // $('#confirm') .modal('show')
        this.$broadcast('confirm')
      },
      delete: function () {
        store.actions.deleteImportCard(this.remove_card.id)
      }
    }
  }
</script>
