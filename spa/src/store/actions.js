import Vue from 'vue'
import VueResource from 'vue-resource'
Vue.use(VueResource)

var api_card = Vue.resource('/api_card{/parm}')
var api_pay = Vue.resource('/api_pay{/parm}')
// var user_info_resource = Vue.resource('/api_get_user_info{/parm}')
// var new_resource = Vue.resource('/api_new{/parm}')
// var old_resource = Vue.resource('/api_old{/parm}')
// var record_resource = Vue.resource('/api_update_last{/parm}')

export default {
  queryPayInfos: ({ dispatch, state }) => {
    api_pay.get().then(
      function (response) {
        console.log(response.data)
        dispatch('SET_PAY_INFOS', response.data.pay_infos)
      },
      function (response) {
      }
    )
  },
  queryCards: ({ dispatch, state }) => {
    // var parm = JSON.stringify(
    //   { god_name: god_name }
    // )
    // parm = {parm: parm}
    api_card.get().then(
      function (response) {
        dispatch('SET_CARDS', response.data.cards)
      },
      function (response) {
      }
    )
  },
  deleteTodo: 'DELETE_TODO'
}
