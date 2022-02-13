<template>
  <div>
    <b-container fluid="md">
      <advertisement-editor @advertisement-saved="onAdvertisementSaved" />
    </b-container>
  </div>
</template>

<script lang="ts">
import Vue from 'vue';
import AdvertisementEditor from '@/components/AdvertisementEditor.vue';
import { AdvertisementFillableData } from "@/store/types/advertisement";
import * as auth_api from '@/api/auth'



export default Vue.extend({
  components: {
    AdvertisementEditor
  },
  props: {
    id: Number
  },
  data() {
    return {
    }
  },
  methods: {
    onAdvertisementSaved(savedAdvertisement: AdvertisementFillableData) {
      if (this.id) {
        alert(JSON.stringify(savedAdvertisement));
      }
      else {
        auth_api.createAdvertisement(savedAdvertisement);
      }
    }
  }
})
</script>
