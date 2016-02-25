<style lang="less">
</style>

<template>
  <div class="ui center aligned segment">
    <h4 class="ui header">{{bind_info.name}}</h4>
    <form class="ui form">
      <div v-bind:class="{ 'error': card_number_error }" class="required field">
        <label>加油卡卡号</label>
        <input @focus="cleanError" v-model="bind_info.card_number"  v-disable="disable_edit"  required="required" type="number"  placeholder="加油卡卡号">
      </div>
      <div v-bind:class="{ 'error': name_error }" class="required field">
        <label>持卡人</label>
        <input @focus="cleanError" v-model="bind_info.name" v-disable="disable_edit" type="text"  placeholder="持卡人">
      </div>
      <div v-bind:class="{ 'error': id_number_error }" class="required field">
        <label>身份证号</label>
        <input @focus="cleanError" v-model="bind_info.id_number" v-disable="disable_edit" type="text"  placeholder="身份证号">
      </div>
      <div v-bind:class="{ 'error': phone_number_error }" class="required field">
        <label>手机号</label>
        <input @focus="cleanError" v-model="bind_info.phone_number" v-disable="disable_edit" type="text"  placeholder="手机号">
      </div>

      <div class="field">
        <label>车牌号</label>
        <input v-model="bind_info.car_number"  v-disable="disable_edit" type="text"  placeholder="车牌号">
      </div>
      <div class="field">
        <label>车型</label>
        <select v-model="bind_info.car_type" v-disable="disable_edit" class="ui fluid dropdown">
          <option selected="selected">私家车</option>
          <option>出租车</option>
          <option>驾培车</option>
          <option>公车</option>
          <option>货车</option>
          <option>摩托车</option>
        </select>
      </div>
    </form>
    <div class="ui center aligned basic segment">
      <button @click="save" v-bind:class="{ 'disabled': loading, 'loading': loading }" class="ui orange button">
        <i class="icon save"></i>保存
      </button>
    </div>
  </div>
</template>

<script>

  var error = require('lib/functions/error.coffee')
  var toast = require('lib/functions/toast.coffee')
  var top_toast = toast.getTopRightToast()
  import store from '../store'
  import $ from 'jquery'
  export default {
    data: function () {
      return {
        card_number_error: false,
        name_error: false,
        phone_number_error: false,
        id_number_error: false,
        disable_edit: true,
        button_text: '修改资料'
      }
    },
    directives: {
      disable: require('lib/directives/disable')
    },
    computed: {
      loading () {
        return store.state.loading
      },
      bind_info () {
        return store.state.card_detail
      }
    },
    ready: function () {
      error.setOnErrorVm(this)
      if (!this.$route.params.id) { // 添加页面
        this.enable()
      } else {
        store.actions.queryCardDetail(this.$route.params.id)
        this.disable()
      }
    },
    methods: {
      enable: function () {
        this.disable_edit = false
        return $(this.$el).find('.ui.orange.button').html('<i class="icon save"></i>保存')
      },
      disable: function () {
        this.disable_edit = true
        return $(this.$el).find('.ui.orange.button').html('<i class="icon file text"></i>编辑')
      },
      save: function () {
        var parm
        if (this.disable_edit) {
          return this.enable()
        } else {
          if (!this.bind_info.card_number) {
            this.card_number_error = true
            top_toast.warning('必须填入加油卡卡号')
            return
          }
          if (!this.bind_info.name) {
            this.name_error = true
            top_toast.warning('必须填入持卡人姓名')
            return
          }
          if (!this.bind_info.id_number) {
            this.id_number_error = true
            top_toast.warning('必须填入身份证号码')
            return
          }
          if (this.bind_info.id_number.trim().length !== 18) {
            this.id_number_error = true
            top_toast.warning('请输入正确的18位身份证号码')
            return
          }
          if (!this.bind_info.phone_number) {
            this.phone_number_error = true
            top_toast.warning('必须填入手机号')
            return
          }
          store.actions.setLoading(true)
          parm = {
            id: this.bind_info.id,
            card_number: this.bind_info.card_number,
            car_number: this.bind_info.car_number,
            car_type: this.bind_info.car_type,
            phone_number: this.bind_info.phone_number,
            name: this.bind_info.name,
            id_number: this.bind_info.id_number
          }
          if (!this.bind_info.id) {
            store.actions.bindCard(parm)
          } else {
            parm.id = this.bind_info.id
            store.actions.updateCardDetail(parm)
          }
        }
      },
      cleanError: function () {
        this.card_number_error = false
        this.name_error = false
        this.phone_number_error = false
        this.id_number_error = false
        this.loading = false
      }
    }
  }
</script>
