import Vue from 'vue'
import VueRouter from 'vue-router'
import VueMoment from 'vue-moment'
import App from './App.vue'

Vue.use(VueRouter)
Vue.use(VueMoment)

Vue.config.debug = true
/* eslint-disable no-new */
new Vue(
  {
    el: '#v_header',
    data () {
    },
    methods: {
    }
  }
)

var router = new VueRouter()
window.router = router
import Recharge from './components/Recharge.vue'
import BindList from './components/BindList.vue'
import CardDetail from './components/CardDetail.vue'

router.map(
  {
    '/': { component: Recharge },
    '/CardDetail/:id': { component: CardDetail },
    '/BindList': { component: BindList }
  }
)
router.start(App, '#app')
