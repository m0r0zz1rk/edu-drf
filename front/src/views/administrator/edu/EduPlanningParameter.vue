<template>

  <PaginationTable
    tableTitle="Параметры планирования"
    tableWidth="98"
    :noTab="false"
    :addButton="false"
    :xlsxButton="false"
    getRecsURL="/backend/api/v1/edu/planning_parameter/"
    editRecURL="/backend/api/v1/edu/planning_parameter/update/"
    :tableHeaders="tableHeaders"
    :fieldsArray="fieldsArray"
  />

</template>

<script>
import PaginationTable from "@/components/tables/pagination_table/PaginationTable.vue";

export default {
  name: "EduPlanningParameter",
  components: {PaginationTable},
  data() {
    return {
      tableHeaders: [
        {
          'title': 'Описание',
          'key': 'description'
        },
        {
          'title': 'Значение',
          'key': 'value'
        },
        {
          'title': 'Управление',
          'key': 'actions'
        }
      ],
      fieldsArray: [
        {
          ui: 'input',
          type: 'text',
          key: 'description',
          addRequired: true,
        },
        {
          ui: 'input',
          type: 'text',
          key: 'value',
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
