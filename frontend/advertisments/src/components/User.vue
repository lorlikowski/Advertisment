<template>
    <div>
      <b-card-group deck>
        <b-card title="Profil użytkownika">
          <template #footer>
            <span>
              <div class="d-flex justify-content-between">
                <div class="d-flex-row">
                  <div>
                    e-mail:
                    <span class="text-primary">{{user.email}}</span>
                  </div>
                  <div>
                    admin:
                    <span class="text-primary" v-if="user.is_admin">TAK</span>
                    <span class="text-primary" v-else>NIE</span>
                  </div>
                </div>
                <div>
                  <b-button v-if="follow" variant="outline-danger" v-on:click="follow_user()">
                  <b-icon icon="bell-fill"></b-icon>
                  </b-button>
                  <b-avatar :to="{name: 'User', params:{id: id}}"></b-avatar>
                </div>
              </div>
            </span>
          </template>
        </b-card>
      </b-card-group>
    </div>
</template>

<script lang="ts">
import Vue from "vue";
import * as api from '@/api/auth'
import * as store from '@/store/modules/auth'

export default Vue.extend({
  props: {
    user: Object,
    id: String,
    follow: Boolean
  },
  computed: {
    authUser() {
      return store.getters.authUser();
    }
  },
  data() {
    return {
      msg: "Hello",
    };
  },
  methods: {
    async follow_user() {
      try {
        const response = await api.follow_user(this.authUser, this.id);
        this.$router.go(0);
      }
      catch(ignore) {
        return;
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
