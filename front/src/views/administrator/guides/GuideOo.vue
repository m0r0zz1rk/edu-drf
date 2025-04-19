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
import {apiRequest} from "@/commons/apiRequest";
import {showAlert} from "@/commons/alerts";
import {tableColumns} from "@/commons/table-data/tableColumns";
import {getOoFieldsArray} from "@/commons/table-data/get-data-for-fields-array/getOoFieldsArray";

export default {
  name: "GuideOo",
  components: {PaginationTable},
  data() {
    return {
      // Список столбцов для таблицы
      tableHeaders: tableColumns['oo'].tableHeaders,
      // Описания столбцов для таблицы
      fieldsArray: null
    }
  },
  methods: {
    async setFieldsArray() {
      this.fieldsArray = await getOoFieldsArray()
    }
  },
  mounted() {
    this.setFieldsArray()
  }
}
</script>

<style scoped>

</style>
