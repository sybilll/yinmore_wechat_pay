// import _ from 'underscore'
// import Vue from 'vue'

export default {
  SET_PAY_INFOS (state, pay_infos) {
    console.log(pay_infos)
    state.pay_infos = pay_infos
    console.log(state.pay_infos)
  },
  SET_CARDS (state, cards) {
    state.cards = cards
  },
  SET_USER_INFO (state, user_info) {
    state.user_info = user_info
  }
}
