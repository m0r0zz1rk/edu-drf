<template>

    <PaginationTable
      tableTitle="Заявки на курсы"
      tableWidth="100"
      :noTab="false"
      :addButton="false"
      :xlsxButton="false"
      getRecsURL="/backend/api/v1/applications/course_application_user/"
      :tableHeaders="tableHeaders"
      :fieldsArray="fieldsArray"
      :itemSelectEvent="openApp"
    />

</template>

<script>

// Форма для просмотра активных заявок на курсы
import {apiRequest} from "@/commons/apiRequest";
import {showAlert} from "@/commons/alerts";
import AppStatusBadge from "@/components/badges/students/AppStatusBadge.vue";
import PaginationTable from "@/components/tables/pagination_table/PaginationTable.vue";

export default {
  name: 'CourseApp',
  props: {
    // Функция для показа анимации загрузки
    usePreLoader: Function,
  },
  components: {PaginationTable, AppStatusBadge},
  data() {
    return {
      // Список подразделений с заявками
      apps: null,
      // Массив для открытых раскрывающихся панелей с заявками
      departmentsPanels: [],
      // Столбцы таблицы для просмотра заявок
      tableHeaders: [
        {title: 'Дата подачи заявки', key: 'date_create'},
        {title: 'Тип услуги', key: 'service_type'},
        {title: 'Наименование', key: 'service_title'},
        {title: 'Сроки проведения', key: 'service_date_range'},
        {title: 'Статус', key: 'status'},
      ],
      // Описание столбцов таблицы
      fieldsArray: [
        {ui: 'input', type: 'text', key: 'date_create', addRequired: false},
        {ui: 'input', type: 'text', key: 'service_type', addRequired: false},
        {ui: 'input', type: 'text', key: 'service_title', addRequired: false},
        {ui: 'input', type: 'text', key: 'service_date_range', addRequired: false},
        {ui: 'appStatus', key: 'status', addRequired: false},
      ]
    }
  },
  methods: {
    // Перейти на страницу заявки
    openApp(app) {
      this.usePreLoader()
      this.$router.push({path: '/student/app/course/'+app.object_id})
    }
  }
}

</script>

<style scoped>

</style>
