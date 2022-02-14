<template>
  <div class="home">
    <img alt="Vue logo" src="../assets/logo.png">
    <b-container fluid="md">
      <!-- <AdvertisementsList :advertisements="advertisements"/> -->
      Użytkownik {{id}} wita na swoim profilu!
      <User :user="user" :id="id" :follow="follow" v-if="user" @followed="onFollowed"/>
    </b-container>
    <UserForm v-if="isAuthenticated && authUser == id"/>
    <b-container fluid="md">
    <br>
    <br>  
    <h3>Ogłoszenia użytkownika</h3>
    <AdvertisementsList :advertisements="advertisements" :edit="id == authUser" :follow="false"/>
    </b-container>
    <b-container fluid="md">
    <br>
    <br>  
    <h3>Obserwowani użytkownicy</h3>
    <UserList :users="users" :follow="false"/>
    </b-container>
    <b-container fluid="md">
    <br>
    <br>  
    <h3>Obserwowane ogłoszenia</h3>
    <AdvertisementsList :advertisements="ads" :follow="false"/>
    </b-container>
  </div>
</template>

<script lang="ts">
import Vue from 'vue';
import User from '@/components/User.vue';
import AdvertisementsList from '@/components/AdvertisementsList.vue';
import UserList from '@/components/UserList.vue'
import UserForm from '@/components/UserForm.vue'
import * as auth_api from '@/api/auth'
import * as auth_store from '@/store/modules/auth'

export default Vue.extend({
  components: {
    User,
    AdvertisementsList,
    UserList,
    UserForm
  },
  props: {
      id: String
  },
  computed: {
    isAuthenticated() {
      return auth_store.getters.isAuthenticated();
    },
    authUser() {
      return auth_store.getters.authUser();
    },
    follow() {
      return this.isAuthenticated && this.authUser != this.id && !this.followed;
    }
  },
  data() {
    return {
      user: {},
      advertisements: [],
      ads: [],
      users: [],
      followed: false
    }
  },
  methods: {
    async getFollows(type: string, id: string) {
      if (id == this.authUser) {
        return auth_api.following_cached(type, id)
      }
      else {
        return auth_api.following(type, id);
      }
    },
    async getFollowedAdvertisements() {
      this.ads = [];
      const ads = await this.getFollows("advertisement", this.id);
      const calls = ads.map(el => auth_api.get_advertisement(el));
      const response = await Promise.allSettled(calls);
      this.ads = response.filter(res => res.status == 'fulfilled').map(res => res.value.data);
    },
    async getUsersAdvertisements() {
      this.advertisements = [];
      const advertisements = (this.authUser == this.id) ? await auth_api.my_advertisements() : await auth_api.advertisements(this.id);
      this.advertisements = advertisements.data;
    },
    async getUser() {
      this.user = {};
      const user = await auth_api.get_user(this.id);
      this.user = user.data;
    },
    async followCheck() {
      if (this.id == this.authUser) {
        return;
      }
      const follows = await this.getFollows("user", this.authUser);
      this.followed = follows.filter(el => el == this.id).length != 0;
    },
    async getFollowedUsers() {
      this.users = [];
      const users = await this.getFollows("user", this.id);
      this.users = users.map(el => el.toString());
    },
    loadAll() {
      this.followed = false;
      this.getFollowedAdvertisements();
      this.getUsersAdvertisements();
      this.getUser();
      this.getFollowedUsers();
      this.followCheck();
    },
    onFollowed() {
      this.followed = true;
    }
  },
  async created() { //TODO better await
    this.loadAll();
  },
  watch: {
      id: 'loadAll'
  }
})
</script>
