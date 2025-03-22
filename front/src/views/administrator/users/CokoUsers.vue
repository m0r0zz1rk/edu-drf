<template>
  <PaginationTable
    tableTitle="Сотрудники"
    tableWidth="98"
    :noTab="false"
    :addButton="false"
    :xlsxButton="false"
    getRecsURL="/backend/api/v1/guides/coko/"
    :tableHeaders="tableHeaders"
    :fieldsArray="fieldsArray"
  />
</template>

<script>
import PaginationTable from "@/components/tables/pagination_table/PaginationTable.vue";

export default {
  name: "CokoUsers",
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
          'title': 'Вн. телефон',
          'key': 'internal_phone'
        },
        {
          'title': 'Подразделение',
          'key': 'department'
        },
        {
          'title': 'Отображение только кураторских групп',
          'key': 'curator_groups'
        },
      ],
      fieldsArray: [
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
          ui: 'input',
          type: 'text',
          key: 'internal_phone',
          addRequired: false,
        },
        {
          ui: 'input',
          type: 'text',
          key: 'department',
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
