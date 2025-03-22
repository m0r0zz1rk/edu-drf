<template>

  <PaginationTable
    tableTitle="Категории должностей"
    tableWidth="98"
    :noTab="false"
    :addButton="true"
    :xlsxButton="true"
    getRecsURL="/backend/api/v1/guides/position_category/"
    addRecURL="/backend/api/v1/guides/position_category/"
    editRecURL="/backend/api/v1/guides/position_category/"
    delRecURL="/backend/api/v1/guides/position_category/"
    :tableHeaders="tableHeaders"
    :fieldsArray="fieldsArray"
  />

</template>

<script>
import PaginationTable from "@/components/tables/pagination_table/PaginationTable.vue";

export default {
  name: "GuidePositionCategory",
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
