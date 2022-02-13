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
      <b-form-group label="Kategoria">
        <b-form-input
          type="text"
          v-model="form.category"
          :disabled="data != null"
        ></b-form-input>
      </b-form-group>
      <b-form-group label="Od kiedy aktywne">
        <b-form-datepicker
          v-model="form.date_start"
          required
        ></b-form-datepicker>
        <b-form-timepicker v-model="form.time_start" locale="pl" required>
        </b-form-timepicker>
      </b-form-group>
      <b-form-group label="Do kiedy aktywne">
        <b-form-datepicker v-model="form.date_end" required></b-form-datepicker>
        <b-form-timepicker v-model="form.time_end" locale="pl" required>
        </b-form-timepicker>
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

function to_DateTime(date: string, time: string) {
  return new Date(date + ' ' + time);
}

function extractDate(date: Date) {
  const ISO = date.toISOString();
  return ISO.substring(0, ISO.lastIndexOf('T'));
}

function extractTime(date: Date) {
  return `${date.getUTCHours()}:${date.getUTCMinutes()}`;
}

function defaultForm() {
  const dt = new Date();
  return {
        title: "",
        description: "",
        content: "",
        category: null,
        date_start: extractDate(dt),
        date_end: extractDate(dt),
        time_start: extractTime(dt),
        time_end: extractTime(dt)
      }
}

export default Vue.extend({
  components: {
    VueEditor,
  },
  props: {
    data: Object as PropType<AdvertisementFillableData>,
  },
  data() {
    return {
      form: defaultForm()
    };
  },
  created() {
    this.loadData();
  },
  methods: {
    onSubmit() {
      this.$emit(
        "advertisement-saved",
        new AdvertisementFillableData(
          this.form.title,
          this.form.description,
          this.form.category,
          to_DateTime(this.form.date_start, this.form.time_start),
          to_DateTime(this.form.date_end, this.form.time_end),
          this.form.content
        )
      );
    },
    loadData() {
      if (this.data == null) {
        this.form = defaultForm();
      }
      else {
        this.form = Object.assign(this.form, this.data);
        this.form.date_start = extractDate(this.data.date_start);
        this.form.time_start = extractTime(this.data.date_start)
        this.form.date_end = extractDate(this.data.date_end);
        this.form.time_end = extractTime(this.data.date_end);
      }
    },
  },
  watch: {
    data: 'loadData'
  }
});
</script>

<style scoped lang="scss">
</style>
