<style less>
</style>

<template>
  <div>
    <header class="main-header">
      <nav class="ui bottom fixed pointing two item menu ">
        <a class="item" v-link="{ name: 'Recharge' }">油卡冲值</a>
        <a class="item" v-link="{ name: 'BindList' }">油卡管理</a>
      </nav>
      <div class="banner">
        <img src="/static/images/header_01.png" />
      </div>
    </header>
    <router-view class="animated" transition="slide"></router-view>
  </div>
</template>

<script>
  export default {
    data () {
      return {
      }
    },
    components: {
    }
  }
</script>
