import Vue from 'vue'
import VueRouter from 'vue-router'
// import VueMoment from 'vue-moment'
import App from './App.vue'

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
import Recharge from './components/Recharge.vue'
import BindList from './components/BindList.vue'
import CardDetail from './components/CardDetail.vue'
import ImportAvailableCardNumbers from './components/ImportAvailableCardNumbers.vue'

router.map(
  {
    '/ImportAvailableCardNumbers': {name: 'ImportAvailableCardNumbers', component: ImportAvailableCardNumbers }, // 录入可用的油卡号
    '/Recharge/': { name: 'Recharge', component: Recharge }, // 为了匹配微信支付url验证，必须以/结尾 !!! 这里设置的最后的/会被取消，只有手工设了
    '/CardDetail/:id': {name: 'CardDetail', component: CardDetail },
    '/BindCard': {name: 'BindCard', component: CardDetail },
    '/BindList': {name: 'BindList', component: BindList }
  }
)
router.start(App, '#app')
