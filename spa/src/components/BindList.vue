<style lang="less">
  .remove.icon {
    color:red;
  }
  img {
    width: 100%;
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
        <th>
          解绑
        </th>
      </tr>
    </thead>
    <tbody>
      <tr v-for="card in cards">
        <td><a href="/#!/CardDetail/{{card.id}}">{{card.name}}</a></td>
        <td><a href="/#!/CardDetail/{{card.id}}">{{card.card_number}}</a></td>
        <td><a @click="unbind(card)" href="javascript:;"><i class="remove icon"></i></a></td>
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
      unbind: function (card) {
        store.actions.unbindCard(card.id)
      },
      jump: function () {
        window.location.hash = '#!/card_manager'
      }
    }
  }
</script>
