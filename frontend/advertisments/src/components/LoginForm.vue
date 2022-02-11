<template>
  <b-container fluid="md">
    <br>
    <br>
    <b-form @submit="login" v-if="show">
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
          required
        ></b-form-input>
      </b-form-group>

      <b-form-group id="input-group-2" label="Hasło:" label-for="input-2">
        <b-form-input
          id="input-2"
          v-model="form.password"
          type="password"
          placeholder="Enter password"
          required
        ></b-form-input>
      </b-form-group>
      <b-button type="submit" variant="primary">Submit</b-button>
    </b-form>
    <center v-if="error">
        <p style="color:red">Błędne dane</p>
    </center>    
    <center>
        Nie jesteś jeszcze zarejestrowany? <router-link to="/register">Kliknij tutaj</router-link>
    </center>
  </b-container>
</template>

<script lang="ts">
import Vue from "vue";
import * as authStore from "@/store/modules/auth"

  export default Vue.extend({
    data() {
      return {
        form: {
          email: '',
          password: '',
        },
        show: true,
        error: false
      }
    },
    methods: {
      async login(event: Event) {
        event.preventDefault();
        
        try {
            const response = await authStore.actions.login({username: this.form.email, password: this.form.password});
            if (response) {
                this.$router.push('/');
            }
            else {
                this.error = true;
            }
        }
        catch(err) {
            console.error(err);
            this.error = true;
        }
        
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