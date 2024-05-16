<template>

  <PaginationTable
    tableTitle="Государства"
    tableWidth="98"
    :noTab="false"
    :addButton="true"
    :xlsxButton="true"
    getRecsURL="/backend/api/v1/guides/admin_states/"
    addRecURL="/backend/api/v1/guides/admin_state/create/"
    editRecURL="/backend/api/v1/guides/admin_state/update/"
    delRecURL="/backend/api/v1/guides/admin_state/delete/"
    :tableHeaders="tableHeaders"
    :fieldsArray="fieldsArray"
  />

</template>

<script>
import PaginationTable from "@/components/pagination_table/PaginationTable.vue";

export default {
  name: "GuideState",
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
