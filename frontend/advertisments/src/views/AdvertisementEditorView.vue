<template>
  <div>
    <b-container fluid="md">
      <advertisement-editor :data="data" @advertisement-saved="onAdvertisementSaved" />
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
      loading: true,
      data: null
    }
  },
  created() {
    this.loadEditor();
  },
  methods: {
    onAdvertisementSaved(savedAdvertisement: AdvertisementFillableData) {
      if (this.id) {
        alert(JSON.stringify(savedAdvertisement));
      }
      else {
        auth_api.createAdvertisement(savedAdvertisement);
      }
    },
    async loadEditor() {
      if (this.id == null) {
        this.data = null
      }
      else {
        const [advertisement, content] = await Promise.all([auth_api.get_advertisement(this.id), auth_api.get_advertisement_content(this.id)]);

        const data = advertisement.data;
        this.data = new AdvertisementFillableData(data.title, data.description, data.category, data.date_start, data.date_end, content.data.content);
      }
    }
  },
  watch: {
    id: 'loadEditor'
  }
})
</script>
