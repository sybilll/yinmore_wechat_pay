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
          {{card.name}}
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

  import $ from 'jquery'
  import store from '../store'
  export default {
    props: ['card_number'],
    data: function () {
      return {
        bind_info: {
          name: '',
          card_number: ''
        }
      }
    },
    computed: {
      cards () {
        return store.state.cards
      }
    },
    ready: function () {
      error.setOnErrorVm(this)
      store.actions.queryCards()
    },
    methods: {
      jump: function () {
        window.location.hash = '#!/card_manager'
      },
      getBindInfo: function () {
        return $.ajax(
          {
            url: '/get_wechat_bind_info',
            type: 'POST',
            success: (
              function (_this) {
                return function (data, status, response) {
                  if (data.error !== '0') {
                    throw new Error(data.error)
                  } else {
                    if (data.data) {
                      _this.bind_info = data.data
                      _this.card_number = _this.bind_info.card_number
                    } else {
                      return $('#card_no_bind_waring').modal('show')
                    }
                  }
                }
              }
            )(this)
          }
        )
      }
    }
  }
</script>
