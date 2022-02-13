<template>
  <div class="home">
    <img alt="Vue logo" src="../assets/logo.png">
    <b-container fluid="md">
      <!-- <AdvertisementsList :advertisements="advertisements"/> -->
      Użytkownik {{id}} wita na swoim profilu!
      <User :user="user" :id="id" :follow="follow" :key="userprofile"/>
    </b-container>
    <UserForm v-if="isAuthenticated && authUser == id"/>
    <b-container fluid="md">
    <br>
    <br>  
    <h3>Ogłoszenia użytkownika</h3>
    <AdvertisementsList :advertisements="advertisements" :edit="true" :follow="false" :key="advertisementlist"/>
    </b-container>
    <b-container fluid="md">
    <br>
    <br>  
    <h3>Obserwowani użytkownicy</h3>
    <UserList :users="users" :follow="false" :key="userlist"/>
    </b-container>
    <b-container fluid="md">
    <br>
    <br>  
    <h3>Obserwowane ogłoszenia</h3>
    <AdvertisementsList :advertisements="ads" :follow="false" :key="followads" v-if="followads != 0"/>
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
      if (!this.following)
        return false;
      return this.isAuthenticated && this.authUser != this.id && (this.following.filter(el => el.object_id == this.id).length == 0);
    }
  },
  data() {
    return {
      user: {},
      advertisements: [],
      ads: [{}],
      users: [""],
      userlist: 0,
      userprofile: 0,
      advertisementlist: 0,
      followads: 0,
      following: []
    }
  },
  async created() { //TODO better await
    const user = await auth_api.get_user(this.id);
    this.user = user.data;
    this.userprofile++;

    if(this.isAuthenticated) {
      const response = await auth_api.following("user", this.authUser);
      this.following = response.data;
    }

    const advertisements = (this.authUser == this.id) ? await auth_api.my_advertisements() : await auth_api.advertisements(this.id);
    
    this.advertisements = advertisements.data;
    for (let i = 0; i < this.advertisements.length; ++i)
      Object.assign(this.advertisements[i], {"owner" : this.id});
    this.advertisementlist++;

    const users = await auth_api.following("user", this.id);
    this.users.pop();
    for (const user of users.data) {
      this.users.push(user["object_id"].toString());
    }
    this.userlist++;

    const ads = await auth_api.following("advertisement", this.id);
    this.ads.pop();
    for (const ad of ads.data) {
      this.ads.push((await auth_api.get_advertisement(ad["object_id"])).data)
    }
    this.followads++;

  },
  watch: {
      id: function reload(old, new_value) {
      this.$router.go(0);
    }
  }
})
</script>
