<template>
  <div>
    <b-row>
      <b-card-group class="col-10 col-md-6 col-lg-4" v-for="advertisement in advertisements" :key="advertisement.id">
        <advertisement :data="advertisement" :edit="edit"/>
      </b-card-group>
    </b-row>
  </div>
</template>

<script lang="ts">
import Vue, {PropType} from "vue";

import Advertisement from '@/components/Advertisement.vue'

export default Vue.extend({
  components: {
    Advertisement
  },
  props: {
    advertisements:  Array,
    edit: Boolean
  },
  data() {
    return {
      msg: "Hello",
    };
  },
});
</script>

<style scoped lang="scss">
// h3 {
//   margin: 40px 0 0;
// }
// ul {
//   list-style-type: none;
//   padding: 0;
// }
// li {
//   display: inline-block;
//   margin: 0 10px;
// }
// a {
//   color: #42b983;
// }
</style>
