<template>

  <PaginationTable
      tableTitle="МО"
      tableWidth="98"
      :noTab="false"
      :addButton="true"
      :xlsxButton="true"
      getRecsURL="/backend/api/v1/guides/mos/"
      addRecURL="/backend/api/v1/guides/mo/create/"
      editRecURL="/backend/api/v1/guides/mo/update/"
      delRecURL="/backend/api/v1/guides/mo/delete/"
      :tableHeaders="tableHeaders"
      :fieldsArray="fieldsArray"
  />

</template>

<script>
import PaginationTable from "@/components/pagination_table/PaginationTable.vue";

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
