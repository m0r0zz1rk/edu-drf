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
      :loading="loading"
      @click="createReport()"
      text="Сформировать"
    />
  </div>

</template>

<script>

// Форма для формирования отчета ПК-1
import monthList from "@/commons/consts/reports/monthList";
import {apiRequest} from "@/commons/apiRequest";
import {showAlert} from "@/commons/alerts";

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
      this.loading = true
      const serviceChartRequest = await apiRequest(
        '/backend/api/v1/reports/pk_one/',
        'POST',
        true,
        {report_year: this.reportYear},
        true
      )
      if (serviceChartRequest.status === 200) {
        showAlert('success', 'ПК-1', 'Запрос обработан, файл будет отправлен на почту')
      } else {
        showAlert('error', 'ПК-1', 'Ошибка при обработке запроса')
      }
      this.loading = false
    }
  }
}

</script>

<style scoped>

</style>
