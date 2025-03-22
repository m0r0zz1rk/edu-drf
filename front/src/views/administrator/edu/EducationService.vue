<template>

  <PaginationTable
    ref="educationServiceTable"
    tableTitle="Курсы (ОУ)"
    tableWidth="98"
    :noTab="false"
    :addButton="true"
    :addSpecialFunction="addEditEducationService"
    :xlsxButton="true"
    getRecsURL="/backend/api/v1/edu/education_service/"
    delRecURL="/backend/api/v1/edu/education_service/"
    :onEditClick="addEditEducationService"
    :tableHeaders="tableHeaders"
    :fieldsArray="fieldsArray"
  />

  <EducationServiceDetail
    ref="educationServiceDetail"
    :getRecsFunction="getRecsEducationServiceTable"
  />

</template>

<script>
import PaginationTable from "@/components/tables/pagination_table/PaginationTable.vue";
import EducationServiceDetail from "@/components/dialogs/edu/EducationServiceDetail.vue";

export default {
  name: "EducationService",
  components: {EducationServiceDetail, PaginationTable},
  data() {
    return {
      tableHeaders: [
        {
          'title': 'ДПП',
          'key': 'program'
        },
        {
          'title': 'Место проведения',
          'key': 'location'
        },
        {
          'title': 'Дата начала обучения',
          'key': 'date_start'
        },
        {
          'title': 'Дата окончания обучения',
          'key': 'date_end'
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
          key: 'program',
          addRequired: true,
        },
        {
          ui: 'input',
          type: 'text',
          key: 'location',
          addRequired: true,
        },
        {
          ui: 'input',
          type: 'text',
          key: 'name',
          addRequired: true,
        },
        {
          ui: 'date',
          key: 'date_start',
          addRequired: true,
        },
        {
          ui: 'date',
          key: 'date_end',
          addRequired: true,
        },
        {
          ui: 'actions',
          key: 'actions'
        }
      ],
      selectedEducationServiceID: null, // object_id выбранной образовательной услуги
    }
  },
  methods: {
    async addEditEducationService(service=null) {
      if (service) {
        this.$refs.educationServiceDetail.changeServiceID(service.object_id)
      } else {
        this.$refs.educationServiceDetail.changeServiceID(null)
      }
    },
    getRecsEducationServiceTable() {
      this.$refs.educationServiceTable.getRecs()
    }
  }
}
</script>

<style scoped>

</style>
