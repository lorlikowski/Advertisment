<template>
    <b-card :title="data.title">
        <b-card-text>
        <div><b-link :to="{name: 'AdvertisementView', params: {advertisement_id: data.id}, query: {backlink: $route.fullPath}}">Zobacz</b-link></div>
        {{data.description}}
        </b-card-text>
        <template #footer>
        <span>
            <div class="d-flex justify-content-between">
            <div class="d-flex-row">
                <div>
                Wyświetlenia:
                <span class="text-primary">{{data.views}}</span>
                </div>
                <div>
                <small class="text-muted">
                    Początek: {{data.date_start}}
                </small>
                </div>
                <div>
                <small class="text-muted">
                    Koniec: {{data.date_end}}
                </small>
                </div>
            </div>
            <div>
                <b-button v-if="follow" variant="outline-danger" v-on:click="follow_ad()">
                <b-icon icon="bell-fill"></b-icon>
                </b-button>
                <b-avatar :to="{name: 'User', params:{id: data.owner}}"></b-avatar>
                {{data.owner}}
                <div v-if="edit">
                    <b-link :to="{name: 'Edit', params:{id: data.id}}" class="card-link">Edytuj</b-link>
                </div>

            </div>
            </div>
        </span>
        </template>
    </b-card>
</template>

<script lang="ts">
import Vue, {PropType} from "vue";

import { Advertisement } from "@/store/types/advertisement"
import * as store from '@/store/modules/auth'
import * as auth_api from '@/api/auth'

export default Vue.extend({
  props: {
      data: Object as PropType<Advertisement>,
      edit: Boolean,
  },
  data() {
    return {
      following: []
    };
  },
  computed: {
      authUser() {
        return store.getters.authUser();
      },
      isAuthenticated() {
        return store.getters.isAuthenticated();
      },
      follow() {
        if (!this.following)
            return false;
        return this.isAuthenticated && (this.following.filter(el => el.object_id == this.data.id).length == 0);
    }
  },
  async created() {
      if(this.isAuthenticated) {
        const response = await auth_api.following("advertisement", this.authUser);
        this.following = response.data;
    }
  },
  methods: {
      async follow_ad() {
      try {
        const response = await auth_api.follow_advertisement(this.authUser, this.data.id);
        this.$router.go(0);
      }
      catch(ignore) {
        return;
      }
    }
  }
});
</script>

<style scoped lang="scss">

</style>
