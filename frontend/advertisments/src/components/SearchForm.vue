<template>
  <div>
    <b-form @submit.prevent="onSubmit" @reset.prevent="onReset">
      <b-form-select
        v-model="form.ordering"
        :options="ordering_options"
      ></b-form-select>
      <b-form-group label="Tekst zawiera">
        <b-input type="text" v-model="form.title__contains"></b-input>
      </b-form-group>
      <b-form-group label="Data rozpoczęcia: od">
        <b-datepicker v-model="form.date_start__gt"></b-datepicker>
      </b-form-group>
      <b-form-group label="Data rozpoczęcia: do">
        <b-datepicker v-model="form.date_start__lt"></b-datepicker>
      </b-form-group>
      <b-form-group label="Data zakończenia: od">
        <b-datepicker v-model="form.date_end__gt"></b-datepicker>
      </b-form-group>
      <b-form-group label="Data zakończenia: do">
        <b-datepicker v-model="form.date_end__lt"></b-datepicker>
      </b-form-group>
      <b-form-group label="Wyniki na 1 stronie">
        <b-form-select
          v-model="form.limit"
          :options="limit_options"
        ></b-form-select>
      </b-form-group>
      <b-button type="submit" variant="primary">Szukaj</b-button>
      <b-button type="reset" variant="danger">Resetuj</b-button>
    </b-form>
  </div>
</template>

<script lang="ts">
import Vue from "vue";
import * as auth_store from "@/store/modules/auth";
import { AdvertisementSearch } from "@/store/types/advertisement";

function defaultForm() {
  return {
    ordering: null,
    limit: 6,
    skip: null,
    title__contains: null,
    date_start__lt: null,
    date_start__gt: null,
    date_end__lt: null,
    date_end__gt: null,
  };
}

export default Vue.extend({
  data() {
    return {
      form: defaultForm() as AdvertisementSearch,
      ordering_options: [
        { value: "title", text: "Tytuł (rosnąco)" },
        { value: "title__dsc", text: "Tytuł (malejąco)" },
        { value: "date_start", text: "Data rozpoczęcia (rosnąco)" },
        { value: "date_start__dsc", text: "Data rozpoczęcia (malejąco)" },
        { value: "date_end", text: "Data zakończenia (rosnąco)" },
        { value: "date_end__dsc", text: "Data zakończenia (malejąco)" },
        { value: "views", text: "Najmniej popularne" },
        { value: "views__dsc", text: "Najpopularniejsze" },
      ],
      limit_options: [
        { value: 6, text: "6" },
        { value: 10, text: "10" },
        { value: 12, text: "12" },
        { value: 15, text: "15" },
        { value: 20, text: "20" },
      ],
    };
  },
  methods: {
    onSubmit() {
      this.$emit("search", this.form);
    },
    onReset() {
      this.form = defaultForm();
    },
  },
});
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped lang="scss">
</style>