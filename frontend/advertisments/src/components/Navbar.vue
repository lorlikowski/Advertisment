<template>
  <b-navbar sticky variant="light">
    <b-navbar-nav>
      <b-nav-item :to="{name: 'Home'}">Ogłoszenia</b-nav-item>
      <b-nav-item :to="{name: 'RootCategory'}">Kategorie</b-nav-item>
      <b-nav-item :to="{name: 'Search'}">Wyszukaj</b-nav-item>
      <b-nav-item :to="{name: 'Create'}" v-if="authenticated">Dodaj ogłoszenie</b-nav-item>
    </b-navbar-nav>
    <b-navbar-nav class="ml-auto">
      <b-nav-item :to="{name: 'Login'}"  v-if="!authenticated">Zaloguj się</b-nav-item>
      <b-nav-item :to="{name: 'User', params: {id: myProfile}}"  v-if="authenticated" >Mój profil</b-nav-item>
      <b-button v-on:click="logout()" v-if="authenticated" variant="success"> Wyloguj </b-button>
    </b-navbar-nav>
  </b-navbar>
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
          return authStore.getters.authUser();
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
