<template>
    <b-card :title="data.title">
        <b-card-text>
        {{data.description}}
        </b-card-text>
        <template #footer>
        <span>
            <div class="d-flex justify-content-between">
            <div class="d-flex-row">
                <div>
                Wyświetlenia:
                <span class="text-primary">{{data.views}}</span>
                </div>
                <div>
                <small class="text-muted">
                    Początek: {{data.date_start}}
                </small>
                </div>
                <div>
                <small class="text-muted">
                    Koniec: {{data.date_end}}
                </small>
                </div>
            </div>
            <div>
                <b-button variant="outline-danger">
                <b-icon icon="bell-fill"></b-icon>
                </b-button>
                <b-avatar :to="{name: 'User', params:{id: data.owner}}"></b-avatar>
                {{data.owner}}
                <div v-if="edit">
                    <b-link :to="{name: 'Edit', params:{id: data.id}}" class="card-link">Edytuj</b-link>
                </div>

            </div>
            </div>
        </span>
        </template>
    </b-card>
</template>

<script lang="ts">
import Vue, {PropType} from "vue";

import { Advertisement } from "@/store/types/advertisement"

export default Vue.extend({
  props: {
      data: Object as PropType<Advertisement>,
      edit: Boolean
  },
  data() {
    return {

    };
  },
  created() {
      console.log(this.data);
  }
});
</script>

<style scoped lang="scss">

</style>
