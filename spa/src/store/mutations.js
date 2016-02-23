// import _ from 'underscore'
// import Vue from 'vue'
import $ from 'jquery'
export default {
  SHOW_CARD_NO_BIND_WARING (state) {
    $('#card_no_bind_waring').modal('show')
  },
  SET_PAY_INFOS (state, pay_infos) {
    state.pay_infos = pay_infos
  },
  SET_CARDS (state, cards) {
    state.cards = cards
  },
  SET_USER_INFO (state, user_info) {
    state.user_info = user_info
  }
}
