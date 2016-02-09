require './style.less'
error = require 'lib/functions/error.coffee'
toast = require 'lib/functions/toast.coffee'
top_toast = toast.getTopRightToast()

module.exports =
  data:->
    total_fee:null
  template: require('./template.html')
  components:
    'bind_info': require('../bind_info')
  methods:
    setTotalFee:(fee)->
      @total_fee = fee
    pay:->
      console.log @total_fee


