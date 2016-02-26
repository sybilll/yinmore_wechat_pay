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
Vue.transition(
  'fade',
  {
    enterClass: 'fadeIn',
    leaveClass: 'fadeOut'
  }
)
var router = new VueRouter()
window.router = router
import Recharge from './components/Recharge.vue'
import BindList from './components/BindList.vue'
import CardDetail from './components/CardDetail.vue'
import ImportAvailableCardNumbers from './components/ImportAvailableCardNumbers.vue'

router.map(
  {
    '/ImportAvailableCardNumbers': {name: 'ImportAvailableCardNumbers', component: ImportAvailableCardNumbers }, // 录入可用的油卡号
    // 为了匹配微信支付url验证，必须以/结尾 !!! 这里设置的最后的/会被取消，只有手工设了
    // 手工设置的，到了/#!/CardDetail/31 后，再点击会变为/#!/CardDetail/Recharge/导致无法跳转
    // 改为进入Recharge后，由程序为其加上最后的/
    '/Recharge': { name: 'Recharge', component: Recharge },
    '/CardDetail/:id': {name: 'CardDetail', component: CardDetail },
    '/BindCard': {name: 'BindCard', component: CardDetail },
    '/BindList': {name: 'BindList', component: BindList }
  }
)
router.start(App, '#app')
