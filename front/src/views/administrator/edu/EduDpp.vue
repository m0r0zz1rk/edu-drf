<template>

  <PaginationTable
    ref="dppPaginationTable"
    v-if="fieldsArray !== null"
    tableTitle="ДПП"
    tableWidth="98"
    :noTab="false"
    :addButton="true"
    :addSpecialFunction="addProgramDetailDialog"
    :xlsxButton="true"
    getRecsURL="/backend/api/v1/edu/programs/"
    :onEditClick="setProgramEdit"
    :tableHeaders="tableHeaders"
    :fieldsArray="fieldsArray"
  />

    <ProgramDetail
      :key="programDetailKey"
      ref="programDetail"
      :audienceCategories="audienceCategories"
      :adCentres="adCentres"
      :getRecs="paginationTableGetRecs"
    />

</template>

<script>
import PaginationTable from "@/components/pagination_table/PaginationTable.vue";
import {apiRequest} from "@/commons/api_request";
import {showAlert} from "@/commons/alerts";
import ProgramDetail from "@/components/dialogs/edu/ProgramDetail.vue";

export default {
  name: "EduDpp",
  components: {ProgramDetail, PaginationTable},
  data() {
    return {
      programDetailKey: 0,
      tableHeaders: [
        {
          'title': 'Подразделение',
          'key': 'department'
        },
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
      ],
      fieldsArray: null,
      audienceCategories: [],
      adCentres: [],
    }
  },
  methods: {
    async getData() {
      let audienceCategoriesRequest = await apiRequest(
        '/backend/api/v1/guides/audience_categories/',
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
        this.fieldsArray = [
          {
            ui: 'select',
            items: this.adCentres,
            key: 'department',
            addRequired: true,
          },
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
        ]
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
