<style less>
.main.container {
    margin-top: 3.5em;
  }
</style>

<template>
  <div>
    <header class="main-header">
      <nav class="ui top fixed pointing menu">
        <a class="header item" href="/"><b>英茂冲值管理</b></a>
        <a v-link="{ name: 'admin_recharge' }" class="item"> 待处理充值 </a>
        <a v-link="{ name: 'ImportAvailableCardNumbers' }" class="item"> 可充值油卡录入 </a>
      </nav>
    </header>
    <router-view></router-view>
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
