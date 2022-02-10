<template>
  <div>
    <div v-for="user in users" :key="user">
      <User :user="getUser(user)" :id="user" />
    </div>
  </div>
</template>

<script lang="ts">
import Vue from "vue";
import User from "@/components/User.vue"

export default Vue.extend({
  components: {
    User
  },
  props: {
    users: Array
  },
  data() {
    return {
      msg: "Hello",
    };
  },
  methods: {
    getUser(user: unknown) {
        let a = user;
        return {
        email: "admin@admin.com",
        is_admin: false
      }
    }
  }
});
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
