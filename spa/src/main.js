import Vue from 'vue'
import VueRouter from 'vue-router'
import App from './App.vue'

Vue.use(VueRouter)

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
import Recharge from './components/Recharge.vue'

router.map(
  {
    '/': {
      component: Recharge
    }
  }
)
router.start(App, '#app')
