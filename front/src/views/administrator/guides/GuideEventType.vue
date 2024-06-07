<template>

  <PaginationTable
    tableTitle="Типы мероприятий"
    tableWidth="98"
    :noTab="false"
    :addButton="true"
    :xlsxButton="true"
    getRecsURL="/backend/api/v1/guides/event_types/"
    addRecURL="/backend/api/v1/guides/event_type/create/"
    editRecURL="/backend/api/v1/guides/event_type/update/"
    delRecURL="/backend/api/v1/guides/event_type/delete/"
    :tableHeaders="tableHeaders"
    :fieldsArray="fieldsArray"
  />

</template>

<script>
import PaginationTable from "@/components/tables/pagination_table/PaginationTable.vue";

export default {
  name: "GuideEventType",
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
