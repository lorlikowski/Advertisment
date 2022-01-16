<template>
  <div>
    <div v-for="advertisement in advertisements" :key="advertisement.id">
      <b-card-group deck>
        <b-card :title="advertisement.title">
          <b-card-text>
          {{advertisement.description}}
          </b-card-text>
          <template #footer>
            <span>
              <div class="d-flex justify-content-between">
                <div class="d-flex-row">
                  <div>
                    Wyświetlenia:
                    <span class="text-primary">{{advertisement.views}}</span>
                  </div>
                  <div>
                    <small class="text-muted">
                        Początek: {{advertisement.date_start}}
                    </small>
                  </div>
                  <div>
                    <small class="text-muted">
                        Koniec: {{advertisement.date_end}}
                    </small>
                  </div>
                </div>
                <div>
                  <b-button variant="outline-danger">
                    <b-icon icon="bell-fill"></b-icon>
                  </b-button>
                  <b-avatar :to="{name: 'User', params:{id: advertisement.owner}}"></b-avatar>
                  {{advertisement.owner}}
                </div>
              </div>
            </span>
          </template>
        </b-card>
      </b-card-group>
    </div>
  </div>
</template>

<script lang="ts">
import Vue from "vue";

export default Vue.extend({
  props: {
    advertisements: Array
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
