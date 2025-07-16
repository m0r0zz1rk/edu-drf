<template>

  <PaginationTable
    tableTitle="Архивные заявки на курсы"
    tableWidth="100"
    :noTab="false"
    :addButton="false"
    :xlsxButton="false"
    getRecsURL="/backend/api/v1/applications/course_application_user/archive"
    :tableHeaders="tableHeaders"
    :fieldsArray="fieldsArray"
    :itemSelectEvent="openApp"
  />

</template>

<script>

// Форма для просмотра активных заявок на курсы
import AppStatusBadge from "@/components/badges/students/AppStatusBadge.vue";
import PaginationTable from "@/components/tables/pagination_table/PaginationTable.vue";

export default {
  name: 'ArchiveCourseApp',
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
        {title: 'Шифр группы', key: 'group_code'},
        {title: 'Наименование', key: 'service_title'},
        {title: 'Сроки проведения', key: 'service_date_range'}
      ],
      // Описание столбцов таблицы
      fieldsArray: [
        {ui: 'input', type: 'text', key: 'date_create', addRequired: false, readOnly: true},
        {ui: 'input', type: 'text', key: 'group_code', addRequired: false},
        {ui: 'input', type: 'text', key: 'service_title', addRequired: false},
        {ui: 'input', type: 'text', key: 'service_date_range', addRequired: false, readOnly: true}
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
