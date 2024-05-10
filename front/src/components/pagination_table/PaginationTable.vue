<template>
  <v-data-table
    sticky
    class="adaptive-no-tab-table"
    :headers="headers"
    :mobile-breakpoint="960"
    :items="recs"
    :loading="tableLoading"
    loading-text="Подождите, идет загрузка данных..."
    :items-per-page="pageRecCount"
  >
    <template v-slot:top>
      <PaginationTableManage
        ref="tableManage"
        :tableTitle="tableTitle"
        :foreignKey="foreignKey"
        :tableTabUrl="tableTabUrl"
        :addButton="addButton"
        :xlsxButton="xlsxButton"
        :xlsxDownload="xlsxDownload"
        :searchShowEvent="changeSearchShow"
        :mobileDisplay="mobileDisplay"
        :tableHeaders="tableHeaders"
        :fieldsArray="fieldsArray"
        :onChangeEvent="searchRecs"
      />
    </template>

    <template v-slot:headers="{ columns, isSorted, getSortIcon, toggleSort }">
      <tr v-if="!(mobileDisplay)" style="position: sticky; top: 0; z-index: 5">
        <td
          style="
            text-align: center;
            background-color: #373c59;
            color: white;
          "
        >№</td>
        <td
          style="
            text-align: center;
            background-color: #373c59;
            color: white;
          "
          v-for="column in columns"
        >
          <b
            style="cursor: pointer"
            @click="() => {toggleSort(column)}"
          >
            {{column.title}}
          </b>

          <template v-if="isSorted(column)">
            <v-icon :icon="getSortIcon(column)"></v-icon>
          </template>

          <PaginationTableSearchField
            :ref="'searchField_'+column.key"
            :useInTableManage="false"
            :field="fieldsArray.filter((field) => field.key === column.key)[0]"
            :onChangeEvent="searchRecs"
          />

        </td>
      </tr>

      <tr v-if="mobileDisplay" style="position: sticky; top: 0; z-index: 5">

      </tr>

    </template>

    <template v-slot:item="{ item, index }">
      <tr v-bind:class="{'v-data-table__tr v-data-table__tr--mobile': mobileDisplay}">
        <td>
          <div v-if="mobileDisplay" class="v-data-table__td-title">№</div>
          <div v-bind:class="{'v-data-table__td-value': mobileDisplay}">
            {{index + ((page-1)*pageRecCount) + 1}}
          </div>
        </td>
        <td v-for="header in tableHeaders" style="text-align: center;">
          <div v-if="mobileDisplay" class="v-data-table__td-title">{{header.title}}</div>
          <div v-if="specialFieldsList.includes(headerUi(header.key))">
            <SpecialField
              :ui="headerUi(header.key)"
              :header="header"
              :item="item"
              :mobileDisplay="mobileDisplay"
            />
          </div>
          <div
            v-if="!(specialFieldsList.includes(headerUi(header.key)))"
            v-bind:class="{'v-data-table__td-value': mobileDisplay}"
          >
            {{ item[header.key] }}
          </div>
        </td>
      </tr>
    </template>

    <template v-slot:bottom>
      <v-toolbar
        color="coko-blue"
        flat
      >
        <div style="width: 30vw; padding-top: 15px; padding-left: 15px">
          <v-select
            :items="pageRecCountOptions"
            label="Записей на странице"
            v-model="pageRecCount" />
        </div>

        <v-divider
          class="mx-4"
          inset
          vertical
        ></v-divider>

        <div style="width: 60vw; margin: 0 auto;">
          <v-pagination
            v-model="page"
            :length="pageTotal"
          ></v-pagination>
        </div>

      </v-toolbar>
    </template>

    <template v-slot:loading>
      <v-skeleton-loader :type="'table-row@'+pageRecCount"></v-skeleton-loader>
    </template>

  </v-data-table>
</template>

<script>
import {apiRequest} from "@/commons/api_request";
import {showAlert} from "@/commons/alerts";
import PaginationTableManage from "@/components/pagination_table/PaginationTableManage.vue";
import {xlsxDownloadFunction} from "@/commons/xlsx";
import JournalModuleBadge from "@/components/badges/journal/JournalModuleBadge.vue";
import JournalRecStatusBadge from "@/components/badges/journal/JournalRecStatusBadge.vue";
import PaginationTableAddDialog from "@/components/pagination_table/dialogs/PaginationTableAddDialog.vue";
import JournalDetailInfoDialog from "@/components/pagination_table/dialogs/JournalDetailInfoDialog.vue";
import PaginationTableSearchField from "@/components/pagination_table/PaginationTableSearchField.vue";
import {useDisplay} from "vuetify";
import specialFieldsList from "@/components/pagination_table/special_fields/SpecialFieldsList";
import SpecialField from "@/components/pagination_table/special_fields/SpecialField.vue";

export default {
  name: "PaginationTable",
  components: {
      SpecialField,
    PaginationTableSearchField,
    JournalDetailInfoDialog,
    PaginationTableAddDialog,
    JournalRecStatusBadge,
    JournalModuleBadge,
    PaginationTableManage
  },
  props: {
    tableTitle: String, // Заголовок таблицы
    tableWidth: Number, // Ширина таблицы
    addButton: Boolean, //Параметр, отвечающий за отображение кнопки "Добавить"
    xlsxButton: Boolean, // Параметр, отвечающий за отображение кнопки "Скачать"
    foreignKey: String, // FK-таблица,
    openTableEvent: Function, // Событий, вызываемое при выборе записи в FK таблице
    tableTabUrl: String, // URL для перехода по кнопке "Перейти к таблице" в FK таблице
    getRecsURL: String, // URL эндпоинта на получение записей с backend
    addUpdateRecURL: String, // URL эндпоинта для добавления/обновления записи на backend
    tableHeaders: Array, /* Список заголовков:
      {
        title - Наименование столбца в таблице,
        key - Наименование поля в БД
      }*/
    fieldsArray: Array, /* Описание столбцов:
      {
        ui - Тип элемента интерфейса,
        type - Тип поля для ввода данных (только для ui: input)
        maxLength: Максимальная длина значения поля (только для ui: input и type: Text)
        tab: При наличии нескольких вкладок на форме с указанной таблицей (только для ui: fk)
        displayFields: Отображаемые поля выбранного объекта, формат: {
          field - наименование поля из БД,
          attr - атрибут (в случае если значение по field является Object, если нет - null)
        } (только для ui: fk)
        tableTab - Адрес для перехода по кнопку "Перейти к таблице" (только для ui: fk)
        getRecsURL - URL эндпоинта на получение записей с backend (только для ui: fk)
        tableColumns - список заголовков (по аналогии выше, только для ui: fk)
        fieldsArray - описание столбцов (по аналогии вышле, только для ui: fk)
        key - совпадение с alias из tableColumns родительской таблицы для связи заголовка и описания,
        addRequired: Проверка на обязательное заполнение при добавлении/редактировании записи
      }*/
  },
  data() {
    return {
      specialFieldsList: specialFieldsList,
      searchValues: [],
      searchString: '',
      headers: [],
      recs: [],
      totalRecs: 0,
      pageRecCountOptions: JSON.parse(import.meta.env.VITE_PAGE_RECS_COUNT_OPTIONS),
      tableLoading: false,
      filterString: '',
      pageRecCount: 0,
      mobileDisplay: useDisplay().smAndDown,
      page: 1,
      pageTotal: 0
    }
  },
  methods: {
    initSearchValues() {
      this.fieldsArray.map((field) => {
        this.searchValues[field.key] = ''
      })
    },
    headerUi(key) {
      try {
        let ui = ''
        this.fieldsArray.map((field) => {
          if (field.key === key) {
            ui = field.ui
          }
        })
        return ui
      } catch (e) {
        return ''
      }
    },
    xlsxDownload() {
      showAlert(
        'success',
        'Выгрузка Excel',
        'Скачивание файла начнется автоматически после завершения формирования'
      )
      let xlsxHeaders = []
      this.headers.map((header) => {
        xlsxHeaders.push(header.title)
      })
      xlsxDownloadFunction(
        this.tableTitle,
        xlsxHeaders,
        this.recs
      )
    },
    async getRecs() {
      this.tableLoading = true
      let start = 0
      if (this.page !== 1) {
        start = ((this.page-1)*this.pageRecCount)+1
      }
      let url = this.getRecsURL+'?size='+this.pageRecCount+'&start='+start+this.searchString
      if (this.filterString.length > 0) {
        url += '&' + this.filterString
      }
      let getRecsRequest = await apiRequest(
        url,
        'GET',
        true,
        null
      )
      if (getRecsRequest.results) {
        this.pageTotal = Math.ceil(getRecsRequest.count/this.pageRecCount)
        this.recs = getRecsRequest.results
      } else {
        let error = 'Произошла ошибка, повторите попытку позже'
        if (getRecsRequest.error) {
          error = getRecsRequest.error
        }
        showAlert(
          'error',
          'Получение записей',
          getRecsRequest.error
        )
      }
      this.tableLoading = false
    },
    searchRecs(key, value) {
      this.searchValues[key] = value
      this.searchString = ''
      Object.keys(this.searchValues).map((key) => {
        if (this.searchValues[key] !== '') {
          this.searchString += '&'+key+'='+ this.searchValues[key]
        }
      })
      this.getRecs()
    },
    changeSearchShow() {
      this.tableHeaders.map((header) => {
        this.$refs['searchField_'+header.key][0].showField = !(this.$refs['searchField_'+header.key][0].showField)
      })
    }
  },
  mounted() {
    this.initSearchValues()
    this.headers = this.tableHeaders
    this.pageRecCount = this.pageRecCountOptions[0]
    this.getRecs()
  },
  watch: {
    page: function() {
      this.getRecs()
    },
    pageRecCount: function() {
      if (this.page === 1) {
        this.getRecs()
      } else {
        this.page = 1
      }

    }
  }
}
</script>

<style scoped>

</style>
