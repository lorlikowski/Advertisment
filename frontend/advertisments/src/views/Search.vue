<template>
  <b-container fluid>
    <div class="content">
      <h3>Wyszukiwarka ogłoszeń</h3>
      <b-row align-h="center">
        <b-col cols="2">
          <search-form @search="searchAdvertisements" />
        </b-col>
        <b-col cols="12" md="10">
          <div class="overflower-base">
            <AdvertisementsList
              :advertisements="advertisements"
              :follow="authenticated"
            />
          </div>
        </b-col>
      </b-row>
    </div>
    <b-pagination
      v-if="pagination_page"
      v-model="pagination_page"
      :total-rows="maxCount"
      :per-page="perPage"
      first-number
      last-number
    ></b-pagination>
  </b-container>
  <!-- </div> -->
</template>

<script lang="ts">
import Vue from "vue";
import AdvertisementsList from "@/components/AdvertisementsList.vue";
import SearchForm from "@/components/SearchForm.vue";
import { AdvertisementSearch } from "@/store/types/advertisement";
import * as auth_api from "@/api/auth";
import * as authStore from "@/store/modules/auth";

type pagination = number | null;

export default Vue.extend({
  components: {
    AdvertisementsList,
    SearchForm,
  },
  data() {
    return {
      advertisements: [],
      pagination_page: 1 as pagination,
      maxCount: 240,
      last_form: null,
      perPage: 6,
    };
  },
  methods: {
    async searchAdvertisements(form: AdvertisementSearch) {
      this.last_form = form;
      this.perPage = form.limit;
      const advertisemens = await auth_api.searchAdvertisements({
        ...form,
        skip: (this.pagination_page - 1) * form.limit,
      });
      this.advertisements = advertisemens.data;
    },
  },
  watch: {
    pagination_page: function () {
      if (this.last_form) {
        this.searchAdvertisements(this.last_form);
      }
    },
  },
  computed: {
    authenticated() {
      return authStore.getters.isAuthenticated();
    },
  },
});
</script>

<style lang="scss" scoped>
.overflower-base {
  overflow-y: auto;
  overflow-x: hidden;
  max-height: 75vh;
}
.overflower {
  overflow-y: scroll;
}
.content {
  height: 85vh;
}
</style>
