<style lang="less">
  img {
    width: 100%
  }
</style>

<template>
  <table class="ui celled striped unstackable table">
    <thead>
      <tr>
        <th>
          <i class="user icon"></i>持卡人
        </th>
        <th>
          <i class="payment icon"></i>卡号
        </th>
      </tr>
    </thead>
    <tbody>
      <tr v-for="card in cards">
        <td>
          <div class="field">
            <div class="ui radio checkbox">
              <input v-model="selected_card_number" @click="selectCard(card)" :value="card.card_number" type="radio" name="card_number">
              <label>{{card.name}}</label>
            </div>
          </div>
        </td>
        <td>{{card.card_number}}</td>
      </tr>
    </tbody>
  </table>
  <div id="card_no_bind_waring" class="ui small modal">
    <i @click="jump" class="close icon"></i>
    <img src="/static/images/warning.png">
  </div>
</template>

<script>
  var error = require('lib/functions/error.coffee')

  import store from '../store'
  export default {
    data: function () {
      return {
      }
    },
    computed: {
      selected_card_number () {
        return store.state.selected_card.card_number
      },
      cards () {
        return store.state.cards
      }
    },
    ready: function () {
      if (Object.keys(store.state.selected_card).length === 0 && store.state.cards.length !== 0) {// 还没选择要充值的
        this.selectCard(store.state.cards[0])
      }

      error.setOnErrorVm(this)
      store.actions.queryCards()
    },
    methods: {
      selectCard: function (card) {
        store.actions.setSelectedCard(card)
      },
      jump: function () {
        this.$router.go({ name: 'BindCard'})
      }
    }
  }
</script>
