<template>

  <b style="padding-top: 15px; padding-left: 15px">
    Отчет по перечню ДПП за определенный период
  </b>

  <v-row
    style="padding-top: 15px; width: 98%; margin: 0 auto"
    dense
  >

    <v-col
        cols="12"
        md="12"
        sm="12"
    >

      <v-number-input
          label="Год"
          :loading="loading"
          :max="2099"
          :min="2020"
          v-model="reportYear"
      />

    </v-col>

    <v-col
        cols="12"
        md="12"
        sm="12"
    >

      <v-select
          bg-color="white"
          variant="solo"
          v-model="reportMonth"
          :items="months"
          item-title="title"
          item-value="key"
          label="Месяц"
          :loading="loading"
      />

    </v-col>

  </v-row>

  <div style="width: 100%; text-align: center">
    <v-btn
        color="coko-blue"
        @click="createReport()"
        text="Сформировать"
    />
  </div>

</template>

<script>

// Форма для формирования отчета с переченем ДПП
import monthList from "@/commons/consts/reports/monthList";

export default {
  name: 'DppList',
  data() {
    return {
      // Параметр отображения анимации загрузки на элементах формы
      loading: false,
      //Список месяцев с возможностью выбора всех
      months: monthList,
      // Выбранный год
      reportYear: new Date().getFullYear(),
      // Выбранный месяц
      reportMonth: 'all'
    }
  },
  methods: {
    // Отправка запроса на формирование отчета
    async createReport() {

    }
  }
}

</script>

<style scoped>

</style>