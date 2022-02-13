<template>
  <b-container fluid>
    <div class="content">
      <h3>Wyszukiwarka ogłoszeń</h3>
      <b-row align-h="center">
        <b-col cols="2">
          <b-form-select
            v-model="selected_ordering"
            :options="ordering_options"
            @change="onOrderingChanged"
          ></b-form-select>
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
      @change="onPaginationChanged"
    ></b-pagination>
  </b-container>
  <!-- </div> -->
</template>

<script lang="ts">
import Vue from "vue";
import AdvertisementsList from "@/components/AdvertisementsList.vue";
import * as auth_api from "@/api/auth";
import * as authStore from "@/store/modules/auth";
import func from "vue-temp/vue-editor-bridge";

type pagination = number | null;
type ordering_type = string | null;

interface Category {
  name: string | null;
  parent: string | null;
}

export default Vue.extend({
  components: {
    AdvertisementsList,
  },
  props: {
    page: {
      type: Number,
      default: 1,
    },
    perPage: {
      type: Number,
      default: 12,
    },
    ordering: {
      type: String,
      default: "views__dsc",
    },
  },
  data() {
    return {
      advertisements: [],
      pagination_page: null as pagination,
      selected_ordering: null,
      ordering_options: [
        { value: "title", text: "Tytuł (rosnąco)" },
        { value: "title__dsc", text: "Tytuł (malejąco)" },
        { value: "date_start", text: "Data rozpoczęcia (rosnąco)" },
        { value: "date_start__dsc", text: "Data rozpoczęcia (malejąco)" },
        { value: "date_end", text: "Data zakończenia (rosnąco)" },
        { value: "date_end__dsc", text: "Data zakończenia (malejąco)" },
        { value: "views", text: "Najmniej popularne" },
        { value: "views__dsc", text: "Najpopularniejsze" },
      ],
      maxCount: 240,
    };
  },
  created() {
    this.pagination_page = this.page;
    this.selected_ordering = this.ordering;
    this.getAdvertisements();
  },
  watch: {
    category: "getAdvertisements",
    page: function () {
      this.pagination_page = this.page;
      this.getAdvertisements();
    },
    perPage: function () {
      this.getAdvertisements();
      this.$forceUpdate();
    },
    ordering: function () {
      this.selected_ordering = this.ordering;
      this.getAdvertisements();
    },
  },
  methods: {
    async getAdvertisements() {
      //   if (this.category) {
      //     let advertisements = null;
      //     if (this.ordering != 'newest') {
      //       advertisements = await auth_api.get_popular_advertisements_in_category(this.category, this.page, this.perPage);
      //     }
      //     else {
      //       advertisements = await auth_api.get_advertisements_in_category(this.category, this.page, this.perPage);
      //     }
      //     this.advertisements = advertisements.data;
      //   }
      //   else {
      //     this.advertisements = [];
      //   }
    },
    onPaginationChanged(new_value: pagination) {
      const query = { ...this.$route.query, page: new_value };
      this.$router.push({ query });
    },
    onOrderingChanged(new_value: ordering_type) {
      const query = { ...this.$route.query, ordering: new_value };
      this.$router.push({ query });
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
