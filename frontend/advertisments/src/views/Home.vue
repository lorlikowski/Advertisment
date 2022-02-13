<template>
  <div>
    <b-container fluid="md" class="content">
      <h3>Najpopularniejsze ogłoszenia</h3>
      <AdvertisementsList :advertisements="advertisements" :follow="authenticated" class="overflower-base"/>

      <b-pagination v-if="pagination_page"
        v-model="pagination_page"
        :total-rows="maxAdvertisements"
        :per-page="perPage"
        first-number
        last-number
        @change="onPaginationChanged"
      ></b-pagination>
    </b-container>
  </div>
</template>

<script lang="ts">
import Vue from 'vue';
import AdvertisementsList from '@/components/AdvertisementsList.vue';
import * as auth_api from '@/api/auth'
import * as authStore from "@/store/modules/auth"

export default Vue.extend({
  components: {
    AdvertisementsList
  },
  props: {
    page: {
      type: Number,
      default: 1
    },
    perPage: {
      type: Number,
      default: 12
    }
  },
  data() {
    return {
      advertisements: [],
      pagination_page: null,
      maxAdvertisements: 240
    }
  },
  created() {
    this.pagination_page = this.page;
    this.getAdvertisements();
  },
  methods: {
    async getAdvertisements() {
      const advertisements = await auth_api.get_popular_advertisements(this.page, this.perPage);
      this.advertisements = advertisements.data;
    },
    onPaginationChanged(new_value){
      this.$router.push(`?page=${new_value}&perPage=${this.perPage}`)
    }
  },
  watch: {
    page: function() {
      this.pagination_page = this.page;
      this.getAdvertisements();
    },
    perPage: function() {
      this.getAdvertisements();
      this.$forceUpdate();
    }
  },
  computed: {
    authenticated(){
      return authStore.getters.isAuthenticated();
    },
  }
})
</script>

<style lang="scss" scoped>
.content {
  height: 85vh;
}
.overflower-base {
    overflow-y: auto;
    overflow-x: hidden;
    height: 80vh;
  }
</style>
