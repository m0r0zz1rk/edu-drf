<template>

  <b style="padding-top: 15px; padding-left: 15px">
    Выгрузка анкет обучающихся за год
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

      <v-select
          bg-color="white"
          variant="solo"
          v-model="serviceType"
          :items="serviceTypes"
          item-title="title"
          item-value="key"
          label="Тип услуги"
          :loading="loading"
      />

    </v-col>

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

  </v-row>

  <div style="width: 100%; text-align: center">
    <v-btn
        color="coko-blue"
        @click="createReport()"
        text="Выгрузить"
    />
  </div>

</template>

<script>

// Форма для формирования списка анкет обучающихся за определенный год
import monthList from "@/commons/consts/reports/monthList";
import serviceTypes from "@/commons/consts/edu/serviceTypes";

export default {
  name: 'ReportForms',
  data() {
    return {
      // Параметр отображения анимации загрузки на элементах формы
      loading: false,
      // Выбранный тип услуги
      serviceType: 'edu',
      // Выбранный год
      reportYear: new Date().getFullYear(),
      // Типы услуг
      serviceTypes: serviceTypes,
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