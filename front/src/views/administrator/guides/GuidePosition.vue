<template>

  <PaginationTable
    tableTitle="Должности"
    tableWidth="98"
    :noTab="false"
    :addButton="true"
    :xlsxButton="true"
    getRecsURL="/backend/api/v1/guides/position/"
    addRecURL="/backend/api/v1/guides/position/"
    editRecURL="/backend/api/v1/guides/position/"
    delRecURL="/backend/api/v1/guides/position/"
    :tableHeaders="tableHeaders"
    :fieldsArray="fieldsArray"
  />

</template>

<script>
import PaginationTable from "@/components/tables/pagination_table/PaginationTable.vue";

export default {
  name: "GuidePosition",
  components: {PaginationTable},
  data() {
    return {
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
