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
                  <b-button variant="outline-danger">
                    Obserwuj
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

export default Vue.extend({
  props: {
    user: Object,
    id: String
  },
  data() {
    return {
      msg: "Hello",
    };
  },
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
