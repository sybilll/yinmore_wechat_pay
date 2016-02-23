import Vue from 'vue'
import VueResource from 'vue-resource'

import _ from 'underscore'
Vue.use(VueResource)

var api_card = Vue.resource('/api_card{/parm}')
var api_pay = Vue.resource('/api_pay{/parm}')
var api_wexin_prepay = Vue.resource('/api_wexin_prepay{/parm}')
// var user_info_resource = Vue.resource('/api_get_user_info{/parm}')
// var new_resource = Vue.resource('/api_new{/parm}')
// var old_resource = Vue.resource('/api_old{/parm}')
// var record_resource = Vue.resource('/api_update_last{/parm}')

export default {
  setLoading: 'SET_LOADING',
  updateCardDetail: ({ dispatch, state }, parm) => {
    parm = JSON.stringify(parm)
    api_card.update(parm).then(
      function (response) {
        dispatch('SET_LOADING', false)
        if (response.data.error !== '0') {
          throw new Error(response.data.error)
        } else {
          window.router.go({ path: '/BindList'})
        }
      },
      function (response) {
      }
    )
  },
  weixinPay: ({ dispatch, state }, parm) => {
    parm = JSON.stringify(parm)
    parm = {parm: parm}
    api_wexin_prepay.get(parm).then(
      function (response) {
        console.log(response.data)
        if (response.data.error !== '0') {
          throw new Error(response.data.error)
        } else {
          var prepay = response.data.prepay
          var weixin_parm = {
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
                alert(res.err_code + res.err_desc)
                console.log(res.err_code + res.err_desc)
              }
            }
          )
        }
      },
      function (response) {
      }
    )
  },
  setSelectedCard: 'SET_SELECTED_CARD',
  queryPayInfos: ({ dispatch, state }) => {
    api_pay.get().then(
      function (response) {
        dispatch('SET_PAY_INFOS', response.data.pay_infos)
      },
      function (response) {
      }
    )
  },
  queryCardDetail: ({ dispatch, state }, id) => {
    var parm = JSON.stringify(
      { id: id }
    )
    parm = {parm: parm}
    api_card.get(parm).then(
      function (response) {
        if (response.data.cards.length === 0) {
          throw new Error('没有查到数据')
        } else {
          dispatch('SET_CARD_DETAIL', response.data.cards[0])
        }
      },
      function (response) {
      }
    )
  },
  queryCards: ({ dispatch, state }) => {
    api_card.get().then(
      function (response) {
        if (response.data.cards.length === 0) {
          dispatch('SHOW_CARD_NO_BIND_WARING')
        } else {
          dispatch('SET_CARDS', response.data.cards)
        }
      },
      function (response) {
      }
    )
  },
  deleteTodo: 'DELETE_TODO'
}
