<style lang="less">
</style>

<template>

  <div class='ui center aligned basic segment'>
    <available-card-numbers></available-card-numbers>
    <div class="ui form">
      <div class="field">
        <label>请在下面输入需要导入的油卡，每一张油卡单独一行</label>
        <textarea v-model="card_numbers"></textarea>
      </div>
      <div class='ui center aligned basic segment'>
        <button @click='import' v-bind:class="{ 'disabled': loading, 'loading': loading }" class='ui orange basic button'>
          <i class='icon add'></i>
          导入
        </button>
      </div>
    </div>
  </div>
</template>

<script>
  import store from '../store'
  import AvailableCardNumbers from './AvailableCardNumbers.vue'
  export default {
    props: [],
    components: {
      AvailableCardNumbers
    },
    data: function () {
      return {
        card_numbers: ''
      }
    },
    computed: {
      loading () {
        return store.state.loading
      }
    },
    ready () {
    },
    methods: {
      import: function () {
        store.actions.setLoading(true)
        store.actions.importCardNumbers(this.card_numbers)
        this.card_numbers = ''
      }
    }
  }
</script>
