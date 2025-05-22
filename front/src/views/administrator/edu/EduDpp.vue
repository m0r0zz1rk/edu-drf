<template>

  <template v-if="fieldsArray === null">
    <b>Подгружаем данные, подождите...</b>
  </template>

  <PaginationTable
    ref="dppPaginationTable"
    v-if="!([0, 1].includes(fieldsArray.length))"
    tableTitle="ДПП"
    tableWidth="98"
    :noTab="false"
    :addButton="true"
    :addSpecialFunction="addProgramDetailDialog"
    :xlsxButton="true"
    :getRecsURL="userRole === 'centre' ? '/backend/api/v1/edu/program/' : `/backend/api/v1/edu/program?dep=${userDep}`"
    delRecURL="/backend/api/v1/edu/program/"
    :onEditClick="setProgramEdit"
    :tableHeaders="tableHeaders"
    :fieldsArray="fieldsArray"
  />

    <ProgramDetail
      ref="programDetail"
      :audienceCategories="audienceCategories"
      :adCentres="adCentres"
      :getRecs="paginationTableGetRecs"
      :userRole="userRole"
      :userDepDisplay="userDepDisplay"
    />

</template>

<script>
import PaginationTable from "@/components/tables/pagination_table/PaginationTable.vue";
import {apiRequest} from "@/commons/apiRequest";
import {showAlert} from "@/commons/alerts";
import ProgramDetail from "@/components/dialogs/edu/ProgramDetail.vue";

export default {
  name: "EduDpp",
  components: {ProgramDetail, PaginationTable},
  props: {
    // Роль пользователя (dep или centre)
    userRole: String,
    // ObjectGUID подразделения пользователя
    userDep: String,
    // Наименование подразделения пользователя
    userDepDisplay: String
  },
  data() {
    return {
      tableHeaders: [],
      fieldsArray: [],
      audienceCategories: [],
      adCentres: [],
    }
  },
  methods: {
    async getData() {
      if (this.userRole !== 'dep') {
        this.tableHeaders = [{
          'title': 'Подразделение',
          'key': 'department'
        },]
        let adCentresRequest = await apiRequest(
          '/backend/api/v1/commons/ad_centres',
          'GET',
          true,
          null
        )
        if (adCentresRequest.error) {
          showAlert(
            'error',
            'Получение подразделений',
            adCentresRequest.error
          )
        } else {
          adCentresRequest.map((ad_centre) => {
            this.adCentres.push(ad_centre.display_name)
          })
        }
        this.fieldsArray = [
          {
            ui: 'select',
            items: this.adCentres,
            key: 'department',
            addRequired: true,
          },
        ]
      }
      this.tableHeaders.push.apply(this.tableHeaders, [
        {
          'title': 'Наименование',
          'key': 'name'
        },
        {
          'title': 'Объем (часов)',
          'key': 'duration'
        },
        {
          'title': 'Номер приказа',
          'key': 'order_number'
        },
        {
          'title': 'Дата приказа',
          'key': 'order_date'
        },
        {
          'title': 'Управление',
          'key': 'actions'
        }
      ])
      this.fieldsArray.push.apply(this.fieldsArray, [
        {
          ui: 'input',
          type: 'text',
          key: 'name',
          addRequired: true,
        },
        {
          ui: 'input',
          type: 'number',
          key: 'duration',
          addRequired: true,
        },
        {
          ui: 'dppOrder',
          key: 'order_number',
          addRequired: false,
        },
        {
          ui: 'date',
          key: 'order_date',
          addRequired: false,
        },
        {
          ui: 'actions',
          key: 'actions'
        }
      ])
      let audienceCategoriesRequest = await apiRequest(
        '/backend/api/v1/guides/audience_category/',
        'GET',
        true,
        null
      )
      if (audienceCategoriesRequest.error) {
        showAlert(
          'error',
          'Получение категорий слушателей',
          adCentresRequest.error
        )
      } else {
        audienceCategoriesRequest.map((category) => {
          this.audienceCategories.push(category.name)
        })
      }
    },
    addProgramDetailDialog() {
      this.$refs.programDetail.setProgramObject(null)
    },
    paginationTableGetRecs() {
      this.$refs.dppPaginationTable.getRecs()
    },
    setProgramEdit(item) {
      this.$refs.programDetail.setProgramObject(item.object_id)
    }
  },
  mounted() {
    this.getData()
  }
}
</script>

<style scoped>

</style>
