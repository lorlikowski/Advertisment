<template>
  <div class="home">
    <img alt="Vue logo" src="../assets/logo.png">
    <b-container fluid="md">
      <LoginForm/>
    </b-container>
  </div>
</template>

<script lang="ts">
import Vue from 'vue';
import LoginForm from '@/components/LoginForm.vue'

export default Vue.extend({
  components: {
    LoginForm
  },
})
</script>
