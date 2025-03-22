<template>

  <PaginationTable
      tableTitle="МО"
      tableWidth="98"
      :noTab="false"
      :addButton="true"
      :xlsxButton="true"
      getRecsURL="/backend/api/v1/guides/mo/"
      addRecURL="/backend/api/v1/guides/mo/"
      editRecURL="/backend/api/v1/guides/mo/"
      delRecURL="/backend/api/v1/guides/mo/"
      :tableHeaders="tableHeaders"
      :fieldsArray="fieldsArray"
  />

</template>

<script>
import PaginationTable from "@/components/tables/pagination_table/PaginationTable.vue";

export default {
  name: "GuideMo",
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
