import Vue from 'vue'
import VueRouter from 'vue-router'
// import VueMoment from 'vue-moment'

Vue.use(VueRouter)
// Vue.use(VueMoment)

Vue.config.debug = true
// Vue.transition('slide', {
//   enterClass: 'slideInRight',
//   leaveClass: 'slideOutRight'
// })
Vue.transition('fade', {
  enterClass: 'fadeIn',
  leaveClass: 'fadeOut'
})
var router = new VueRouter()
window.router = router
import ImportAvailableCardNumbers from './components/ImportAvailableCardNumbers.vue'
var admin_recharge = require('../../static/components/admin_recharge')

router.map(
  {
    '/': {name: 'admin_recharge', component: admin_recharge },
    '/import': {name: 'ImportAvailableCardNumbers', component: ImportAvailableCardNumbers } // 录入可用的油卡号
  }
)
import Admin from './Admin.vue'
router.start(Admin, '#app')
