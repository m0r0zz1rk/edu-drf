<template>

  <PaginationTable
      tableTitle="Типы ОО"
      tableWidth="98"
      :noTab="false"
      :addButton="true"
      :xlsxButton="true"
      getRecsURL="/backend/api/v1/guides/oo_type/"
      addRecURL="/backend/api/v1/guides/oo_type/"
      editRecURL="/backend/api/v1/guides/oo_type/"
      delRecURL="/backend/api/v1/guides/oo_type/"
      :tableHeaders="tableHeaders"
      :fieldsArray="fieldsArray"
  />

</template>

<script>
import PaginationTable from "@/components/tables/pagination_table/PaginationTable.vue";

export default {
  name: "GuideOoType",
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
