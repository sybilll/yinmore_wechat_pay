// import _ from 'underscore'
// import Vue from 'vue'
import $ from 'jquery'
export default {
  SET_LOADING (state, loading) {
    state.loading = loading
  },
  SET_CARD_DETAIL (state, card_detail) {
    state.card_detail = card_detail
  },
  SET_SELECTED_CARD (state, card) {
    state.selected_card = card
  },
  SHOW_CARD_NO_BIND_WARING (state) {
    $('#card_no_bind_waring').modal('show')
  },
  SET_PAY_INFOS (state, pay_infos) {
    state.pay_infos = pay_infos
  },
  SET_CARDS (state, cards) {
    state.cards = cards
    if (Object.keys(state.selected_card).length === 0 && state.cards.length !== 0) { // 还没选择要充值的,默认选第一个
      state.selected_card = state.cards[0]
    }
  },
  SET_USER_INFO (state, user_info) {
    state.user_info = user_info
  }
}
