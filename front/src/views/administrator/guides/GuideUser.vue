<template>
  <PaginationTable
      tableTitle="Журнал событий"
      tableWidth="98"
      :addButton="false"
      :xlsxButton="true"
      getRecsURL="/backend/api/v1/guides/users/"
      :tableHeaders="tableHeaders"
      :fieldsArray="fieldsArray"
  />
</template>

<script>
import PaginationTable from "@/components/pagination_table/PaginationTable.vue";

export default {
  name: "GuideUser",
  components: {PaginationTable},
  data() {
    return {
      tableHeaders: [
        {
          'title': 'Дата регистрации',
          'key': 'date_create'
        },
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
          'title': 'Дата рождения',
          'key': 'birthday'
        },
        {
          'title': 'СНИЛС',
          'key': 'snils',
        },
        {
          'title': 'Телефон',
          'key': 'phone',
        },
        {
          'title': 'Email',
          'key': 'email',
        },
        {
          'title': 'Преподаватель',
          'key': 'teacher',
        },
        {
          'title': 'Огр. по здоровью',
          'key': 'teacher',
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
          key: 'source',
          addRequired: false,
        },
      ]
    }
  }
}
</script>

<style scoped>

</style>
