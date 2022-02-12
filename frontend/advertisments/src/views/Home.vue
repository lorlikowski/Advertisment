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

export default Vue.extend({
  components: {
    AdvertisementsList
  },
  data() {
    return {
      advertisements: [
        {
          title: "Pierwszy",
          owner: "1",
          description: "Pierwsze ogłoszenie na platformie",
          views: 10,
          date_start: '2022-01-10',
          date_end: '2022-01-25'
        },
        {
          title: "Toster",
          owner: "2",
          description: "Nowiutki toster o krótkim czasie zapiekania i dużej mocy",
          views: 23,
          date_start: '2022-01-10',
          date_end: '2022-01-25'
        },
        {
          title: "Trzecie",
          owner: "2",
          description: "Trzecie ogłoszenie",
          views: 23,
          date_start: '2022-01-22',
          date_end: '2022-01-25'
        }
      ]
    }
  }
})
</script>
