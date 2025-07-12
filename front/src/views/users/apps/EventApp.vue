<template>

  <PaginationTable
    tableTitle="Заявки на мероприятия"
    tableWidth="100"
    :noTab="false"
    :addButton="false"
    :xlsxButton="false"
    getRecsURL="/backend/api/v1/applications/event_application_user/"
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
  name: 'EventApp',
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
        {title: 'Шифр группы', key: 'group_code'},
        {title: 'Наименование', key: 'service_title'},
        {title: 'Сроки проведения', key: 'service_date_range'},
        {title: 'Статус', key: 'status'},
      ],
      // Описание столбцов таблицы
      fieldsArray: [
        {ui: 'input', type: 'text', key: 'date_create', addRequired: false, readOnly: true},
        {ui: 'input', type: 'text', key: 'service_type', addRequired: false},
        {ui: 'input', type: 'text', key: 'group_code', addRequired: false},
        {ui: 'input', type: 'text', key: 'service_title', addRequired: false},
        {ui: 'input', type: 'text', key: 'service_date_range', addRequired: false, readOnly: true},
        {ui: 'appStatus', key: 'status', addRequired: false},
      ]
    }
  },
  methods: {
    // Перейти на страницу заявки
    openApp(app) {
      this.usePreLoader()
      this.$router.push({path: '/student/app/event/'+app.object_id})
    }
  }
}

</script>

<style scoped>

</style>
