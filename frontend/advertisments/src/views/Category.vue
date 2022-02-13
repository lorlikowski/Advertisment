<template>
  <b-container fluid>
    <div class="content">
      <h3 v-if="category">Ogłoszenia w: {{category}}</h3>
      <h3 v-else>Kategorie ogłoszeń</h3>
    <b-row align-h="around">
      <b-col>
        <b-button v-b-toggle.collapse-3 class="m-1">Pokaż podkategorie</b-button>
        <b-link v-if="parentCategory" :to="{name: 'Category', params: {category: parentCategory}}">Powrót do: {{parentCategory}}</b-link>
      </b-col>
      <b-col cols="12" md="10">
      <b-collapse visible id="collapse-3">
        <b-list-group>
          <b-list-group-item v-for="subcategory in subcategories" :key="subcategory.name" :to="{name: 'Category', params: {category: subcategory.name, perPage: perPage}}">{{subcategory.name}}</b-list-group-item>
        </b-list-group>
      </b-collapse>
      <div class="overflower-base">
        <AdvertisementsList :advertisements="advertisements"/>
      </div>
      </b-col>
      <b-col>
      </b-col>
    </b-row>
    </div>
    <b-pagination v-if="pagination_page"
        v-model="pagination_page"
        total-rows="100"
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
      default: 25
    }
  },
  data() {
    return {
      advertisements: [],
      categories: [],
      pagination_page: null
    }
  },
  created() {
    this.pagination_page = this.page;
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
    }
  },
  methods: {
    async getAdvertisements() {
      if (this.category) {
        const advertisements = await auth_api.get_popular_advertisements_in_category(this.category, this.page, this.perPage);
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
    onPaginationChanged(new_value){
      this.$router.push(`?page=${new_value}&perPage=${this.perPage}`)
    }
  },
  computed: {
    subcategories() {
      const category = this.category || null;
      return this.categories.filter(el => el.parent == category);
    },
    parentCategory() {
      const category = this.category;
      const el = this.categories.find(el => el.name == category);
      if (el != null) {
        return el.parent;
      }
      return null
    }
  }
})
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
