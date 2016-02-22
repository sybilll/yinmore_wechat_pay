require './admin.less'

Vue = require './vue_local.coffee'

App = Vue.extend({})

router = new VueRouter()

router.map
  '/': component: require('./components/admin_recharge')
  '/pay_request': component: require('./components/card_recharge')

router.start(App, '#admin')
