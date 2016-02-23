import Vue from 'vue'
import VueRouter from 'vue-router'
import VueMoment from 'vue-moment'
import App from './App.vue'

Vue.use(VueRouter)
Vue.use(VueMoment)

Vue.config.debug = true

var router = new VueRouter()
window.router = router
import Recharge from './components/Recharge.vue'
import BindList from './components/BindList.vue'
import CardDetail from './components/CardDetail.vue'

router.map(
  {
    '/Recharge': { name: 'Recharge', component: Recharge },
    '/CardDetail/:id': {name: 'CardDetail', component: CardDetail },
    '/BindList': {name: 'BindList', component: BindList }
  }
)
router.start(App, '#app')
