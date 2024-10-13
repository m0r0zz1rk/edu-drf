<template>

  <PaginationTable
  tableTitle="Регионы РФ"
  tableWidth="98"
  :noTab="false"
  :addButton="true"
  :xlsxButton="true"
  getRecsURL="/backend/api/v1/guides/regions/"
  addRecURL="/backend/api/v1/guides/region/create/"
  editRecURL="/backend/api/v1/guides/region/update/"
  delRecURL="/backend/api/v1/guides/region/delete/"
  :tableHeaders="tableHeaders"
  :fieldsArray="fieldsArray"
  />

</template>

<script>

// Форма для работы с регионами РФ
import PaginationTable from "@/components/tables/pagination_table/PaginationTable.vue";

export default {
  name: 'GuideRegion',
  components: {PaginationTable},
  data() {
    return {
      // Список столбцов таблицы
      tableHeaders: [
        {
          'title': 'Название',
          'key': 'name'
        },
        {
          'title': 'Управление',
          'key': 'actions'
        }
      ],
      // Список описаний столцов таблицы
      fieldsArray: [
        {
          ui: 'input',
          type: 'text',
          key: 'name',
          addRequired: true,
        },
        {
          ui: 'actions',
          key: 'actions'
        }
      ]
    }
  }
}

</script>

<style scoped>

</style>