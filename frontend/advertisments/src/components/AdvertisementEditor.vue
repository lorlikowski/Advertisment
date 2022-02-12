<template>
  <div>
    <b-form @submit.prevent="onSubmit">
      <b-form-group label="Tytuł ogłoszenia">
        <b-form-input type="text" v-model="form.title" required></b-form-input>
      </b-form-group>
      <b-form-group label="Opis">
        <b-form-input
          type="text"
          v-model="form.description"
          required
        ></b-form-input>
      </b-form-group>
      <b-form-group label="Od kiedy aktywne">
        <b-form-datepicker
          v-model="form.date_start"
          required
        ></b-form-datepicker>
      </b-form-group>
      <b-form-group label="Do kiedy aktywne">
        <b-form-datepicker v-model="form.date_end" required></b-form-datepicker>
      </b-form-group>
      <b-form-group label="Treść ogłoszenia">
        <vue-editor v-model="form.content"></vue-editor>
      </b-form-group>
      <b-button type="submit" variant="primary">Zapisz</b-button>
    </b-form>
  </div>
</template>

<script lang="ts">
import Vue, { PropType } from "vue";

import { AdvertisementFillableData } from "@/store/types/advertisement";

import { VueEditor } from "vue2-editor";

export default Vue.extend({
  components: {
    VueEditor,
  },
  props: {
    data: Object as PropType<AdvertisementFillableData>,
  },
  data() {
    return {
      form: {
        title: "",
        description: "",
        content: "",
        date_start: new Date(),
        date_end: new Date(),
      },
    };
  },
  methods: {
    onSubmit() {
      this.$emit(
        "advertisement-saved",
        new AdvertisementFillableData(
          this.form.title,
          this.form.description,
          this.form.date_start,
          this.form.date_end,
          this.form.content
        )
      );
    },
  },
});
</script>

<style scoped lang="scss">
</style>
