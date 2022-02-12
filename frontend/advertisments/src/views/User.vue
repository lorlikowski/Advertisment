<template>
  <div class="home">
    <img alt="Vue logo" src="../assets/logo.png">
    <b-container fluid="md">
      <!-- <AdvertisementsList :advertisements="advertisements"/> -->
      Użytkownik {{id}} wita na swoim profilu!
      <User :user="user" :id="id"/>
    </b-container>
    <UserForm/>
    <b-container fluid="md">
    <br>
    <br>  
    <h3>Ogłoszenia użytkownika</h3>
    <AdvertisementsList :advertisements="advertisements"/>
    </b-container>
    <b-container fluid="md">
    <br>
    <br>  
    <h3>Obserwowani użytkownicy</h3>
    <UserList :users="users"/>
    </b-container>
    <b-container fluid="md">
    <br>
    <br>  
    <h3>Obserwowane ogłoszenia</h3>
    <AdvertisementsList :advertisements="advertisements"/>
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
  data() {
    return {
      user: {},
      advertisements: [
        {
          title: "Pierwszy",
          owner: "1",
          description: "Pierwsze ogłoszenie na platformie",
          views: 10,
          date_start: '2022-01-10',
          date_end: '2022-01-25'
        },
        {
          title: "Toster",
          owner: "2",
          description: "Nowiutki toster o krótkim czasie zapiekania i dużej mocy",
          views: 23,
          date_start: '2022-01-10',
          date_end: '2022-01-25'
        }
      ],
      users: ["1","2","3"],
    }
  },
  async created() {
    const user = await auth_api.get_user(this.id);
    this.user = user.data;
    const advertisements = await auth_api.advertisements(this.id);
    this.advertisements = advertisements.data;
  }
})
</script>
