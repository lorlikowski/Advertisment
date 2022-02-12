<template>
    <div id="nav">
      <router-link to="/">Home</router-link> |
      <router-link :to="myProfile" v-if="authenticated">Mój profil</router-link> 
      <router-link to="/login" v-if="!authenticated"> Zaloguj się</router-link>
      <b-button v-on:click="logout()" v-if="authenticated" variant="success"> Wyloguj </b-button>
    </div>
</template>

<script lang="ts">
import Vue from "vue";
import * as authStore from "@/store/modules/auth"

  export default Vue.extend({
    computed: {
        authenticated(){
          return authStore.getters.isAuthenticated();
        },
        myProfile() {
          return "/users/" + authStore.getters.authUser();
        }
    },
    methods: {
        async logout() {
          authStore.actions.logout();
          this.$router.push('/');
        }
    }
  })
</script>

<style lang="scss">

#nav {
  padding: 30px;

  a {
    font-weight: bold;
    color: #2c3e50;

    &.router-link-exact-active {
      color: #42b983;
    }
  }
  div {
    font-weight: bold;
    color: #2c3e50;
  }
  button {
  display: block;
  margin-left: auto;
  margin-right: 0;
  margin-top: 0;
}
}
</style>
