require './style.less'
error = require 'lib/functions/error.coffee'
toast = require 'lib/functions/toast.coffee'
top_toast = toast.getTopRightToast()

module.exports =
  data:->
    pay_infos:null
  template: require('./template.html')
  ready:->
    error.setOnErrorVm(@)
    @getPayInfos()
  methods:
    getPayInfos:->
      $.ajax
        url: '/getPayInfos'
        type: 'POST'
        success: (data, status, response) =>
          if data.error != '0'
            throw new Error(data.error)
          else
            @pay_infos = data.data
