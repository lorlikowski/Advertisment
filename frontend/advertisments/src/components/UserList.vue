<template>
  <div>
    <div v-for="user in users_data" v-bind:key="user.id">
      <User :user="user" :follow="follow" :id="user.id" />
    </div>
  </div>
</template>

<script lang="ts">
import Vue, { PropType } from "vue";
import User from "@/components/User.vue"
import * as auth_api from "@/api/auth"

export default Vue.extend({
  components: {
    User
  },
  props: {
    users: Array as PropType<string[]>,
    follow: Boolean
  },
  data() {
    return {
      users_data: []
    };
  },
  created() {
    this.loadUsers();
  },
  methods: {
    async loadUsers() {
      this.users_data = [];
      const users = await Promise.allSettled(this.users.map(user => this.getUser(user)));
      this.users_data = users.filter(res => res.status == 'fulfilled').map(res => res.value);
    },
    async getUser(id: string) {
      const response = await auth_api.get_user(id);
      return {...response.data, id};
    }
  },
  watch: {
    users: 'loadUsers'
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
