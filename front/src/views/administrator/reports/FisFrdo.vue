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

  <div
      :key="key"
      style="height: 60vh"
  >
    <PaginationTable
        ref="studentGroupPaginationTable"
        tableTitle="Учебные группы"
        tableWidth="98"
        :noTab="false"
        :addButton="false"
        :xlsxButton="false"
        :getRecsURL="'/backend/api/v1/edu/student_group/?month='+backendMonthNumber"
        :tableHeaders="tableHeaders"
        :fieldsArray="fieldsArray"
    />
  </div>



  <div style="width: 100%; text-align: center">
    <v-btn
        color="coko-blue"
        @click="createReport()"
        text="Сформировать"
    />
  </div>

</template>

<script>

// Форма для формирования отчета ФИС ФРДО
import monthList from "@/commons/consts/reports/monthList";
import PaginationTable from "@/components/tables/pagination_table/PaginationTable.vue";
import studentGroupStatuses from "@/commons/consts/edu/studentGroupStatuses";
import {apiRequest} from "@/commons/apiRequest";
import {showAlert} from "@/commons/alerts";

export default {
  name: 'FisFrdo',
  components: {PaginationTable},
  data() {
    return {
      // Параметр отображения анимации загрузки на элементах формы
      loading: false,
      //Список месяцев с возможностью выбора всех
      months: monthList,
      // Выбранный месяц
      reportMonth: 'all',
      // Номер месяца, для получения учебных групп
      backendMonthNumber: 0,
      // Список столбцов для таблицы учебных групп
      tableHeaders: [
        {
          'title': 'checkbox',
          'key': 'checkbox'
        },
        {
          'title': 'Шифр',
          'key': 'code'
        },
        {
          'title': 'Наименование услуги',
          'key': 'service_name'
        },
        {
          'title': 'Начало обучения',
          'key': 'date_start'
        },
        {
          'title': 'Окончание обучения',
          'key': 'date_end'
        }
      ],
      // Описание заголовков
      fieldsArray: [
        {
          ui: 'checkbox',
          key: 'checkbox'
        },
        {
          ui: 'input',
          type: 'text',
          key: 'code',
          addRequired: true,
        },
        {
          ui: 'input',
          type: 'text',
          key: 'service_name',
          addRequired: true,
        },
        {
          ui: 'date',
          key: 'date_start',
          addRequired: true,
        },
        {
          ui: 'date',
          key: 'date_end',
          addRequired: true,
        }
      ],
      // Ключ перерисовки компонента
      key: 0
    }
  },
  methods: {
    // Отправка запроса на формирование отчета
    async createReport() {
      if (this.$refs.studentGroupPaginationTable.itemsList.length === 0) {
        showAlert('error', 'ФИС ФРДО', 'Выберите учебный группы')
        return
      }
      this.loading = true
      const serviceChartRequest = await apiRequest(
        '/backend/api/v1/reports/fis_frdo/',
        'POST',
        true,
        {group_ids: this.$refs.studentGroupPaginationTable.itemsList},
        true
      )
      if (serviceChartRequest.status === 200) {
        showAlert('success', 'ФИС ФРДО', 'Запрос обработан, файл будет отправлен на почту')
      } else {
        showAlert('error', 'ФИС ФРДО', 'Ошибка при обработке запроса')
      }
      this.loading = false
    }
  },
  watch: {
    reportMonth: function () {
      let notAll = false
      for (let i=1;i<this.months.length;i++) {
        if (this.months[i].key === this.reportMonth) {
          this.backendMonthNumber = i
          this.key += 1
          notAll = true
        }
      }
      if (!(notAll)) {
        this.backendMonthNumber = 0
        this.key += 1
      }
    },
  }
}

</script>

<style scoped>

</style>
