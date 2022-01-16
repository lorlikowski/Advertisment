<template>
  <div class="home">
    <img alt="Vue logo" src="../assets/logo.png">
    <b-container fluid="md">
      <!-- <AdvertisementsList :advertisements="advertisements"/> -->
      Użytkownik {{id}} wita na swoim profilu!
    </b-container>
  </div>
</template>

<script lang="ts">
import Vue from 'vue';
// import AdvertisementsList from '@/components/AdvertisementsList.vue';

export default Vue.extend({
  components: {
  },
  props: {
      id: String
  },
  data() {
    return {
    }
  }
})
</script>
