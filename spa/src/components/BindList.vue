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
        <td><a @click="showConfirm(card)" href="javascript:;"><i class="remove icon"></i></a></td>
      </tr>
    </tbody>
  </table>
  <div id="card_no_bind_waring" class="ui small modal">
    <i @click="jump" class="close icon"></i>
    <img src="/static/images/warning.png">
  </div>
  <div id="confirm" class="ui small test modal transition hidden">
    <div class="header">
      是否与该油卡解绑？
    </div>
    <div class="content">
      <table class="ui celled striped unstackable table">
        <thead>
          <tr>
            <th>
              <i class="user icon"></i>{{remove_card.name}}
            </th>
            <th>
              <i class="payment icon"></i>{{remove_card.card_number}}
            </th>
          </tr>
        </thead>
      </table>
    </div>
    <div class="actions">
      <div class="ui negative button">
        取消
      </div>
      <div @click="unbind" class="ui positive right labeled icon button">
        确认
        <i class="checkmark icon"></i>
      </div>
    </div>
  </div>
</template>

<script>
  var error = require('lib/functions/error.coffee')

  import store from '../store'
  export default {
    data: function () {
      return {
        remove_card:{}
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
      showConfirm: function (card) {
        this.remove_card = card
        $('#confirm') .modal('show')
      },
      selectCard: function (card) {
        store.actions.setSelectedCard(card)
      },
      unbind: function () {
        store.actions.unbindCard(this.remove_card.id)
      },
      jump: function () {
        window.location.hash = '#!/card_manager'
      }
    }
  }
</script>
