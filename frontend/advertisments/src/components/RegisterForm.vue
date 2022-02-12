<template>
  <b-container fluid="md">
    <br>
    <br>
    <b-form @submit.prevent="onSubmit" v-if="show">
      <b-form-group
        id="input-group-1"
        label="Email:"
        label-for="input-1"
      >
        <b-form-input
          id="input-1"
          v-model="form.email"
          type="email"
          placeholder="Enter email"
          autocomplete="email"
          required
        ></b-form-input>
      </b-form-group>

      <b-form-group id="input-group-2" label="Hasło:" label-for="input-2">
        <b-form-input
          id="input-2"
          v-model="form.password"
          type="password"
          placeholder="Enter password"
          autocomplete="new-password"
          required
        ></b-form-input>
      </b-form-group>

      <b-form-group id="input-group-3" label="Powtórz hasło:" label-for="input-3">
        <b-form-input
          id="input-3"
          v-model="form.password1"
          type="password"
          placeholder="Enter password"
          autocomplete="new-password"
          required
        ></b-form-input>
      </b-form-group>
      <b-button type="submit" variant="primary">Submit</b-button>
    </b-form>
    <center>
      <p v-if="success" style="color:green">Rejestracja przebiegła pomyślnie</p>
      <p v-if="error" style="color:red">Podano błędne dane</p>
    </center>
  </b-container>
</template>

<script lang="ts">
import Vue from "vue";
import * as auth_store from '@/store/modules/auth'

  export default Vue.extend({
    data() {
      return {
        form: {
          email: '',
          password: '',
          password1: '',
        },
        show: true,
        success: false,
        error: false
      }
    },
    methods: {
      async onSubmit() {
        this.success = await auth_store.actions.register(this.form);
        this.error = !this.success;
      },
    }
  })
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped lang="scss">
h3 {
  margin: 40px 0 0;
}
ul {
  list-style-type: none;
  padding: 0;
}
li {
  display: inline-block;
  margin: 0 10px;
}
a {
  color: #42b983;
}
</style>