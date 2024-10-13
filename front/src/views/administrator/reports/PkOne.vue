<template>

  <b style="padding-top: 15px; padding-left: 15px">
    Отчет со сведениями о деятельности организации,
    осуществляющей образовательную деятельность по ДПП
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

// Форма для формирования отчета ПК-1
import monthList from "@/commons/consts/reports/monthList";

export default {
  name: 'PkOne',
  data() {
    return {
      // Параметр отображения анимации загрузки на элементах формы
      loading: false,
      // Выбранный год
      reportYear: new Date().getFullYear(),
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