<template>
  <div id="app">
    <Navbar :key="login"/>
    <router-view/>
  </div>
</template>

<script lang="ts">
import Navbar from '@/components/Navbar.vue'
import * as store from '@/store/modules/auth'

export default {
  components: {
    Navbar
  },
  data() {
    return {
      login: 0
    }
  },
  async created() {
    this.login = store.actions.initialize() ? 1 : 0;
  }
}
</script>

<style lang="scss">
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  color: #2c3e50;
}

</style>
