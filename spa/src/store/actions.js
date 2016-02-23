import Vue from 'vue'
import VueResource from 'vue-resource'
Vue.use(VueResource)

var api_card = Vue.resource('/api_card{/parm}')
// var user_info_resource = Vue.resource('/api_get_user_info{/parm}')
// var new_resource = Vue.resource('/api_new{/parm}')
// var old_resource = Vue.resource('/api_old{/parm}')
// var record_resource = Vue.resource('/api_update_last{/parm}')

export default {
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
