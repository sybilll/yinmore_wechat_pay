require './app.less'

Vue = require './vue_local.coffee'

App = Vue.extend({})

router = new VueRouter()

router.map
  '/card_manager': component: require('./components/card_manager')
  '/': component: require('./components/card_recharge')

router.start(App, '#app')
