<template>
  <b-container fluid="md">
    <br>
    <br>
    <b-form @submit.prevent="onSubmit" v-if="show">
      <b-form-group
        id="input-group-1"
        label="Nowe hasło:"
        label-for="input-1"
      >
        <b-form-input
          id="input-1"
          v-model="form.new_password"
          type="new_password"
          placeholder="Enter new password"
          required
        ></b-form-input>
      </b-form-group>

      <b-form-group id="input-group-2" label="Powtórz hasło:" label-for="input-2">
        <b-form-input
          id="input-2"
          v-model="form.new_password1"
          placeholder="Enter new password"
          required
        ></b-form-input>
      </b-form-group>
      <b-button type="submit" variant="primary">Submit</b-button>
    </b-form>
  </b-container>
</template>

<script lang="ts">
import Vue from "vue";

  export default Vue.extend({
    data() {
      return {
        form: {
          new_password: '',
          new_password1: '',
        },
        show: true
      }
    },
    methods: {
      onSubmit() {
        alert(JSON.stringify(this.form))
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