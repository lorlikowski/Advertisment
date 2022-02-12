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
      alert(JSON.stringify(savedAdvertisement));
    }
  },
  created() {
    if (this.id) {
      alert(this.id);
    }
  }
})
</script>
