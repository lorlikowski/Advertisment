<template>
  <b-container fluid>
    <div class="content">
      <h3 v-if="category">Ogłoszenia w: {{category}} <span v-if="categoryObject">(Aktywnych: {{categoryObject.advertisements_count_active}}, archiwalnych: {{categoryObject.advertisements_count_archive}})</span></h3>
      <h3 v-else>Kategorie ogłoszeń</h3>
    <b-row align-h="center">
      <b-col>
        <b-button v-b-toggle.collapse-3 class="m-1">Pokaż podkategorie</b-button>
        <b-form-select v-model="selected_ordering" :options="ordering_options" @change="onOrderingChanged"></b-form-select>
        <b-link v-if="categoryObject && categoryObject.parent" :to="{name: 'Category', params: {category: categoryObject.parent}, query: {perPage: perPage, ordering: ordering}}">Powrót do: {{categoryObject.parent}}</b-link>
      </b-col>
      <b-col cols="12" md="10">
      <b-collapse visible id="collapse-3">
        <b-list-group>
          <b-list-group-item v-for="subcategory in subcategories" :key="subcategory.name" :to="{name: 'Category', params: {category: subcategory.name}, query: {perPage: perPage, ordering: ordering}}">{{subcategory.name}}</b-list-group-item>
        </b-list-group>
      </b-collapse>
      <div class="overflower-base">
        <AdvertisementsList :advertisements="advertisements" :follow="authenticated"/>
      </div>
      </b-col>
      <b-col>
      </b-col>
    </b-row>
    </div>
    <b-pagination v-if="pagination_page"
        v-model="pagination_page"
        :total-rows="advertisementsCount"
        :per-page="perPage"
        first-number
        last-number
        @change="onPaginationChanged"
      ></b-pagination>
  </b-container>
  <!-- </div> -->
</template>

<script lang="ts">
import Vue from 'vue';
import AdvertisementsList from '@/components/AdvertisementsList.vue';
import * as auth_api from '@/api/auth'
import * as authStore from "@/store/modules/auth"

type pagination = number | null;
type ordering_type = string | null;

interface Category {
  name: string | null,
  parent: string | null
}


export default Vue.extend({
  components: {
    AdvertisementsList
  },
  props: {
    category: String,
    page: {
      type: Number,
      default: 1
    },
    perPage: {
      type: Number,
      default: 12
    },
    ordering: {
      type: String,
      default: 'popular'
    }
  },
  data() {
    return {
      advertisements: [],
      categories: [] as Array<Category>,
      pagination_page: null as pagination,
      selected_ordering: 'popular',
      ordering_options: [{value: 'popular', text: "Najpopularniejsze"}, {value: "newest", text: "Najnowsze"}]
    }
  },
  created() {
    this.pagination_page = this.page;
    this.selected_ordering = this.ordering;
    this.getAdvertisements();
    this.getCategories();
  },
  watch: {
    category: 'getAdvertisements',
    page: function() {
      this.pagination_page = this.page;
      this.getAdvertisements();
    },
    perPage: function() {
      this.getAdvertisements();
      this.$forceUpdate();
    },
    ordering: function() {
      this.selected_ordering = this.ordering;
      this.getAdvertisements();
    }
  },
  methods: {
    async getAdvertisements() {
      if (this.category) {
        let advertisements = null;
        if (this.ordering != 'newest') {
          advertisements = await auth_api.get_popular_advertisements_in_category(this.category, this.page, this.perPage);
        }
        else {
          advertisements = await auth_api.get_advertisements_in_category(this.category, this.page, this.perPage);
        }
        this.advertisements = advertisements.data;
      }
      else {
        this.advertisements = [];
      }
    },
    async getCategories() {
      const categories = await auth_api.get_categories();
      this.categories = categories.data;
    },
    onPaginationChanged(new_value: pagination){
      const query = {...this.$route.query, page: new_value};
      this.$router.push({query});
    },
    onOrderingChanged(new_value: ordering_type) {
      const query = {...this.$route.query, ordering: new_value};
      this.$router.push({query});
    }
  },
  computed: {
    authenticated(){
      return authStore.getters.isAuthenticated();
    },
    subcategories() : Category[]{
      const category = this.category || null;
      return this.categories.filter((el: Category)  => el.parent == category);
    },
    categoryObject() : Category | undefined{
      const category = this.category;
      return this.categories.find((el: Category) => el.name == category);
    },
    advertisementsCount() {
      const obj = this.categoryObject;
      if (!obj) {
        return 0;
      }
        return obj.advertisements_count_active + obj.advertisements_count_archive;
      }
    }
  }
)
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
