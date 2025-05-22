<template>

  <template v-if="fieldsArray === null">
    <b>Подгружаем данные, подождите...</b>
  </template>

  <PaginationTable
    v-if="!([0, 1].includes(fieldsArray.length))"
    ref="informationServiceTable"
    tableTitle="Мероприятия (ИКУ)"
    tableWidth="98"
    :noTab="false"
    :addButton="true"
    :addSpecialFunction="addEditInformationService"
    :xlsxButton="true"
    :getRecsURL="
      userRole === 'centre' ?
        '/backend/api/v1/edu/information_service/'
        :
        `/backend/api/v1/edu/information_service?dep=${userDep}`
    "
    delRecURL="/backend/api/v1/edu/information_service/"
    :onEditClick="addEditInformationService"
    :tableHeaders="tableHeaders"
    :fieldsArray="fieldsArray"
  />

  <InformationServiceDetail
    ref="informationServiceDetail"
    :adCentres="adCentres"
    :ikuTypes="ikuTypes"
    :audienceCategories="audienceCategories"
    :getRecsFunction="getRecsInformationServiceTable"
    :userRole="userRole"
    :userDep="userDep"
    :userDepDisplay="userDepDisplay"
  />

</template>

<script>
import PaginationTable from "@/components/tables/pagination_table/PaginationTable.vue";
import {apiRequest} from "@/commons/apiRequest";
import {showAlert} from "@/commons/alerts";
import InformationServiceDetail from "@/components/dialogs/edu/InformationServiceDetail.vue";

// Компонент для работы с ИКУ (мероприятиями)
export default {
  name: "EduInformationService",
  components: {InformationServiceDetail, PaginationTable},
  props: {
    // Роль пользователя (centre или dep)
    userRole: String,
    // ObjectGUID подразеделения пользвоателя
    userDep: String,
    // Наименование подразделения пользователя
    userDepDisplay: String
  },
  data() {
    return {
      tableHeaders: [], // Заголовки пагинационной таблицы
      fieldsArray: [], // Описания полей пагинационной таблицы
      adCentres: [], // Список подразделений ЦОКО
      ikuTypes: [], // Список типов ИКУ
      audienceCategories: [] // Список категорий слушателей
    }
  },
  methods: {
    async getData() {
      if (this.userRole === 'centre') {
        this.tableHeaders = [
          {
            'title': 'Подразделение',
            'key': 'department'
          },
        ]
        const adCentresRequest = await apiRequest(
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
      let ikuTypesRequest = await apiRequest(
        '/backend/api/v1/guides/event_type/',
        'GET',
        true,
        null
      )
      if (ikuTypesRequest.error) {
        showAlert(
          'error',
          'Получение типов мероприятий',
          adCentresRequest.error
        )
      } else {
        ikuTypesRequest.map((ikuType) => {
          this.ikuTypes.push(ikuType.name)
        })
      }
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
      this.tableHeaders.push.apply(this.tableHeaders, [
        {
          'title': 'Тип',
          'key': 'type'
        },
        {
          'title': 'Наименование',
          'key': 'name'
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
      ])
      this.fieldsArray.push.apply(this.fieldsArray, [
        {
          ui: 'select',
          items: this.ikuTypes,
          key: 'type',
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
          type: 'text',
          key: 'location',
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
      ])
    },
    getRecsInformationServiceTable() {
      this.$refs.informationServiceTable.getRecs()
    },
    async addEditInformationService(service=null) {
      if (service) {
        this.$refs.informationServiceDetail.changeServiceID(service.object_id)
      } else {
        this.$refs.informationServiceDetail.changeServiceID(null)
      }
    }
  },
  mounted() {
    this.getData()
  }
}
</script>

<style scoped>

</style>
