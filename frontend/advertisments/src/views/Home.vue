<template>
  <div class="home">
    <img alt="Vue logo" src="../assets/logo.png">
    <b-container fluid="md">
      <AdvertisementsList :advertisements="advertisements"/>
    </b-container>
  </div>
</template>

<script lang="ts">
import Vue from 'vue';
import AdvertisementsList from '@/components/AdvertisementsList.vue';
import * as auth_api from '@/api/auth'

export default Vue.extend({
  components: {
    AdvertisementsList
  },
  data() {
    return {
      advertisements: []
    }
  },
  async created() {
    const advertisements = await auth_api.get_popular_advertisements_in_category("1", 1, 25);
    this.advertisements = advertisements.data;
  }
})
</script>
