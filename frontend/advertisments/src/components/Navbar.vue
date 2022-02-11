<template>
    <div id="nav">
      <router-link to="/">Home</router-link> |
      <router-link to="/users/1">Mój profil</router-link>
      <router-link to="/"> Zaloguj się</router-link>
      <router-link to="/"> Wyloguj </router-link>
    </div>
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
