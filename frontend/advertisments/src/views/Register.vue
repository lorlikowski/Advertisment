<template>
  <div class="home">
    <img alt="Vue logo" src="../assets/logo.png">
    <b-container fluid="md">
      <RegisterForm/>
    </b-container>
  </div>
</template>

<script lang="ts">
import Vue from 'vue';
import RegisterForm from '@/components/RegisterForm.vue'

export default Vue.extend({
  components: {
    RegisterForm
  },
})
</script>
