<template>
  <div>
    <b-container fluid="md">
      <b-link v-if="backlink" :href="backlink">Powrót</b-link>
      <div v-html="content">
      </div>
    </b-container>
  </div>
</template>

<script lang="ts">
import Vue from 'vue';
import DOMPurify from 'dompurify';
import * as auth_api from '@/api/auth'

export default Vue.extend({
  props: {
    advertisement_id: Number,
    backlink: String
  },
  data() {
    return {
      content: ""
    }
  },
  watch: {
    advertisement_id: 'getAdvertisement'
  },
  async created() {
    this.getAdvertisement();
  },
  methods: {
    async getAdvertisement() {
      auth_api.update_advertisement_views(this.advertisement_id);
      const content = await auth_api.get_advertisement_content(this.advertisement_id);
      this.content = DOMPurify.sanitize(content.data.content);
    }
  }
})
</script>
