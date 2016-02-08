###
管理油卡，
###
require './style.less'
module.exports =
  data:->
    current_view:'card_bind'
    user_info:null
  created:->
  methods:
    change:(view)->
      @current_view = view
  template: require('./template.html')
  components:
    "card_bind": require '../card_bind'
    "card_info": require '../card_info'
