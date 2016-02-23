require './app.less'

Vue = require './vue_local.coffee'

App = Vue.extend({})

router = new VueRouter()

router.map
  '/': component: require('./components/card_recharge')
  '/card_manager': component: require('./components/card_manager')

router.start(App, '#app')
