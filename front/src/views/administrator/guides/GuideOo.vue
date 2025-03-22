<template>

  <template v-if="fieldsArray === null">
    <b>Подгружаем данные, подождите...</b>
  </template>

  <PaginationTable
    v-if="fieldsArray !== null"
    tableTitle="ОО"
    tableWidth="98"
    :noTab="false"
    :addButton="true"
    :xlsxButton="true"
    getRecsURL="/backend/api/v1/guides/oo/"
    addRecURL="/backend/api/v1/guides/oo/"
    editRecURL="/backend/api/v1/guides/oo/"
    delRecURL="/backend/api/v1/guides/oo/"
    :tableHeaders="tableHeaders"
    :fieldsArray="fieldsArray"
  />

</template>

<script>
import PaginationTable from "@/components/tables/pagination_table/PaginationTable.vue";
import {apiRequest} from "@/commons/api_request";
import {showAlert} from "@/commons/alerts";

export default {
  name: "GuideOo",
  components: {PaginationTable},
  data() {
    return {
      tableHeaders: [
        {
          'title': 'Краткое наименование',
          'key': 'short_name'
        },
        {
          'title': 'Полное наименование',
          'key': 'full_name'
        },
        {
          'title': 'МО',
          'key': 'mo'
        },
        {
          'title': 'Тип ОО',
          'key': 'oo_type'
        },
        {
          'title': 'Форма',
          'key': 'form'
        },
        {
          'title': 'Управление',
          'key': 'actions'
        }
      ],
      fieldsArray: null
    }
  },
  methods: {
    async getData() {
      let moListRequest = await apiRequest(
        '/backend/api/v1/guides/mo/',
        'GET',
        true,
        null
      )
      if (moListRequest.error) {
        showAlert(
          'error',
          'Получение списка МО',
          moListRequest.error
        )
        return false
      }
      let mos = []
      moListRequest.map((mo) => {
        mos.push(mo.name)
      })
      let ooTypeListRequest = await apiRequest(
        '/backend/api/v1/guides/oo_type/',
        'GET',
        true,
        null
      )
      if (ooTypeListRequest.error) {
        showAlert(
          'error',
          'Получение списка типов ОО',
          ooTypeListRequest.error
        )
        return false
      }
      let oo_types = []
      ooTypeListRequest.map((oo_type) => {
        oo_types.push(oo_type.name)
      })
      this.fieldsArray = [
        {
          ui: 'input',
          type: 'text',
          key: 'short_name',
          addRequired: true,
        },
        {
          ui: 'input',
          type: 'text',
          key: 'full_name',
          addRequired: true,
        },
        {
          ui: 'select',
          items: mos,
          key: 'mo',
          addRequired: true
        },
        {
          ui: 'select',
          items: oo_types,
          key: 'oo_type',
          addRequired: true
        },
        {
          ui: 'input',
          type: 'text',
          key: 'form',
          addRequired: true,
        },
        {
          ui: 'actions',
          key: 'actions'
        }
      ]
    }
  },
  mounted() {
    this.getData()
  }
}
</script>

<style scoped>

</style>
