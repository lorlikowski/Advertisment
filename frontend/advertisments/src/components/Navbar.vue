<template>
  <b-navbar sticky variant="light">
    <b-navbar-nav>
      <b-nav-item :to="{name: 'Home'}">Ogłoszenia</b-nav-item>
      <b-nav-item :to="{name: 'Create'}">Dodaj ogłoszenie</b-nav-item>
    </b-navbar-nav>
    <b-navbar-nav class="ml-auto">
      <b-nav-item :to="{name: 'Login'}">Zaloguj się</b-nav-item>
      <b-nav-item :to="{name: 'User', params: {id: '1'}}">Mój profil</b-nav-item>
    </b-navbar-nav>
  </b-navbar>
    <!-- <div id="nav">
      <router-link to="/">Ogłoszenia</router-link> |
      <router-link to="/users/1">Mój profil</router-link>
      <router-link to="/login"> Zaloguj się</router-link>
      <router-link to="/"> Wyloguj </router-link>
    </div> -->
</template>

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
}
</style>
