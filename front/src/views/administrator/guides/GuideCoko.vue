<template>
  <PaginationTable
    tableTitle="Сотрудники"
    tableWidth="98"
    :noTab="false"
    :addButton="false"
    :xlsxButton="true"
    getRecsURL="/backend/api/v1/guides/cokos/"
    :tableHeaders="tableHeaders"
    :fieldsArray="fieldsArray"
  />
</template>

<script>
import PaginationTable from "@/components/pagination_table/PaginationTable.vue";

export default {
  name: "GuideCoko",
  components: {PaginationTable},
  data() {
    return {
      tableHeaders: [
        {
          'title': 'Фамилия',
          'key': 'surname'
        },
        {
          'title': 'Имя',
          'key': 'name'
        },
        {
          'title': 'Отчество',
          'key': 'patronymic'
        },
        {
          'title': 'Отображение только кураторских групп',
          'key': 'curator_groups'
        },
      ],
      fieldsArray: [
        {
          ui: 'date',
          key: 'date_create',
          addRequired: false,
        },
        {
          ui: 'input',
          type: 'text',
          key: 'surname',
          addRequired: false,
        },
        {
          ui: 'input',
          type: 'text',
          key: 'name',
          addRequired: false,
        },
        {
          ui: 'input',
          type: 'text',
          key: 'patronymic',
          addRequired: false,
        },
        {
          ui: 'cokoCuratorGroups',
          key: 'curator_groups',
          addRequired: false
        }
      ]
    }
  }
}
</script>

<style scoped>

</style>
