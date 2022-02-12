<template>
  <div>
    <div v-for="(user, index) in users_data" v-bind:key="`user-${index}`">
      <User :user="user" :id="users[index]" />
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
    users: Array as PropType<string[]>
  },
  data() {
    return {
      users_data: [{}]
    };
  },
  async created() {
    this.users_data.pop();
    for(const user of this.users) {
      const response = await auth_api.get_user(user);
      this.users_data.push(response.data);
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
