<template>
  <v-data-table
    sticky
    v-model="itemsList"
    v-bind:class="{'adaptive-no-tab-table': noTab, 'adaptive-tab-table': !(noTab)}"
    :headers="headers"
    :mobile-breakpoint="960"
    :items="recs"
    :loading="tableLoading"
    loading-text="Подождите, идет загрузка данных..."
    :items-per-page="pageRecCount"
    :show-select="selection"
  >
    <template v-slot:top>
      <PaginationTableManage
        ref="tableManage"
        :tableTitle="tableTitle"
        :itemsCount="itemsCount"
        :foreignKey="foreignKey"
        :tableTabUrl="tableTabUrl"
        :addButton="addButton"
        :addSpecialFunction="addSpecialFunction"
        :addRecURL="addRecURL"
        :getRecs="getRecs"
        :hideSearchButton="hideSearchButton"
        :xlsxButton="xlsxButton"
        :xlsxDownload="xlsxDownload"
        :searchShowEvent="changeSearchShow"
        :mobileDisplay="mobileDisplay"
        :tableHeaders="tableHeaders"
        :fieldsArray="fieldsArray"
        :onChangeEvent="searchRecs"
        :defaultBody="defaultBody"
        :tableLoading="tableLoading"
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
        ><b>№</b></td>
        <td
          v-if="tableHeaders.filter((h) => h.key === 'checkbox').length > 0"
          style="
            text-align: center;
            background-color: #373c59;
            color: white;
          "
        >
          <v-checkbox
              :model-value="itemsList.length === recs.length"
              @click="itemAddOrDeleteInList('all')"
          />
        </td>
        <template
            v-for="column in columns"
        >

          <td
            v-if="column.key !== 'checkbox'"
            style="
              text-align: center;
              background-color: #373c59;
              color: white;
              white-space: nowrap;
            "
          >

            <b
              style="cursor: pointer"
              @click="() => {toggleSort(column)}"
            >
              {{column.title}}
            </b>

            <template
                v-if="column.key !== 'actions'"
            >

              <template v-if="isSorted(column)">
                <v-icon :icon="getSortIcon(column)"></v-icon>
              </template>

              <PaginationTableBaseField
                  :ref="'searchField_'+column.key"
                  :checkRequired="false"
                  :useInTableManage="false"
                  :field="fieldsArray.filter((field) => field.key === column.key)[0]"
                  :onChangeEvent="searchRecs"
              />

            </template>

          </td>

        </template>

      </tr>

      <tr
          v-if="mobileDisplay"
          style="position: sticky; top: 0; z-index: 5"
      >

      </tr>

    </template>

    <template v-slot:item="{ item, index }">
      <tr
        v-bind:class="{
          'v-data-table__tr v-data-table__tr--mobile': mobileDisplay,
          'table-row-click': itemSelectEvent,
          'selected-row': itemSelectEvent && selectedItemObjectID === item.object_id
        }"
        @click="itemSelectEvent && itemSelectEvent(item)"
      >
        <td
            style="text-align: center;"
        >
          <div
              v-if="mobileDisplay"
              class="v-data-table__td-title"
          >
            №
          </div>
          <div
              v-bind:class="{'v-data-table__td-value': mobileDisplay}"
          >
            {{index + ((page-1)*pageRecCount) + 1}}
          </div>
        </td>
        <td
            v-for="header in tableHeaders"
            style="text-align: center;"
        >

          <div
              v-if="mobileDisplay"
              class="v-data-table__td-title"
          >
            {{header.title}}
          </div>

          <template
              v-if="!(['actions', 'checkbox'].includes(header.key))"
          >

              <div v-if="specialFieldsList.includes(headerUi(header.key))">
                  <SpecialField
                      :ui="headerUi(header.key)"
                      :header="header"
                      :item="item"
                      :mobileDisplay="mobileDisplay"
                      :openDocViewerFunction="openDocViewerFunction"
                      :selectGroupAppFunction="selectGroupAppFunction"
                  />
              </div>

              <div
                  v-if="!(specialFieldsList.includes(headerUi(header.key)))"
                  v-bind:class="{'v-data-table__td-value': mobileDisplay}"
              >
                  <p v-if="mobileDisplay">

                    <template
                        v-if="item[header.key].constructor === String "
                    >

                      <template
                        v-if="header.key !== 'short_name'"
                      >

                        {{ item[header.key].slice(0, 25) }}

                        <template
                            v-if="item[header.key].length > 25"
                        >

                          ...

                        </template>

                      </template>

                      <template
                        v-if="header.key === 'short_name'"
                      >
                        {{ item[header.key] }}
                      </template>

                    </template>

                    <template
                        v-if="item[header.key].constructor !== String"
                    >
                      {{ item[header.key] }}
                    </template>

                  </p>

                  <p
                      v-if="!mobileDisplay"
                  >
                    {{ item[header.key] }}
                  </p>
              </div>

          </template>

          <template
              v-if="header.key === 'checkbox'"
          >
            <v-checkbox
                :model-value="itemsList.includes(item.object_id)"
                @click="itemAddOrDeleteInList(item.object_id)"
            />
          </template>

          <template v-if="header.key === 'actions'">

              <div
                v-if="!(specialFieldsList.includes(headerUi(header.key)))"
                v-bind:class="{'v-data-table__td-value': mobileDisplay}"
              >

                  <v-icon
                    v-if="!(onlyDelete)"
                    icon="mdi-pencil"
                    color="coko-blue"
                    @click="() => {
                      if (this.onEditClick) {
                        return this.onEditClick(item)
                      } else {
                        return showEditDialog(item)
                      }
                    }"
                  />

                  &nbsp;&nbsp;

                <v-icon
                    v-if="delRecURL"
                    icon="mdi-delete"
                    color="coko-blue"
                    @click="deleteItem(item.object_id)"
                />

              </div>
          </template>


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

  <PaginationTableEditDialog
    ref="editDialog"
    :tableHeaders="tableHeaders"
    :fieldsArray="fieldsArray"
    :editRecURL="editRecURL"
    :getRecs="getRecs"
    :mobileDisplay="mobileDisplay"
  />

</template>

<script>
import {apiRequest} from "@/commons/api_request";
import {showAlert} from "@/commons/alerts";
import PaginationTableManage from "@/components/tables/pagination_table/PaginationTableManage.vue";
import {xlsxDownloadFunction} from "@/commons/xlsx";
import JournalModuleBadge from "@/components/badges/journal/JournalModuleBadge.vue";
import JournalRecStatusBadge from "@/components/badges/journal/JournalRecStatusBadge.vue";
import PaginationTableAddDialog from "@/components/tables/pagination_table/dialogs/PaginationTableAddDialog.vue";
import JournalDetailInfoDialog from "@/components/dialogs/journal/JournalDetailInfoDialog.vue";
import PaginationTableBaseField from "@/components/tables/pagination_table/PaginationTableBaseField.vue";
import {useDisplay} from "vuetify";
import specialFieldsList from "@/components/tables/pagination_table/special_fields/SpecialFieldsList";
import SpecialField from "@/components/tables/pagination_table/special_fields/SpecialField.vue";
import {no} from "vuetify/locale";
import PaginationTableEditDialog from "@/components/tables/pagination_table/dialogs/PaginationTableEditDialog.vue";

// Компонент пагинационной таблицы
export default {
  name: "PaginationTable",
  components: {
      PaginationTableEditDialog,
    SpecialField,
    PaginationTableBaseField,
    JournalDetailInfoDialog,
    PaginationTableAddDialog,
    JournalRecStatusBadge,
    JournalModuleBadge,
    PaginationTableManage
  },
  props: {
    // Возможность выборки нескольких строк таблицы (checkbox)
    selection: Boolean,
    tableTitle: String, // Заголовок таблицы
    noTab: Boolean, // Отображение таблицы в карточке без верхних табов
    tableWidth: Number, // Ширина таблицы
    addButton: Boolean, //Параметр, отвечающий за отображение кнопки "Добавить"
    addSpecialFunction: Function, // Событие, вызываемое по нажатию на кнопку "Добавить" (если не подоходит стандартная форма)
    xlsxButton: Boolean, // Параметр, отвечающий за отображение кнопки "Скачать"
    hideSearchButton: Boolean, // Параметр, отвечающий за отображение кнопки поиска
    foreignKey: String, // FK-таблица,
    openTableEvent: Function, // Событий, вызываемое при выборе записи в FK таблице
    tableTabUrl: String, // URL для перехода по кнопке "Перейти к таблице" в FK таблице
    getRecsURL: String, // URL эндпоинта на получение записей с backend
    addRecURL: String, // URL эндпоинта на добавление записи
    editRecURL: String, // URL эндпоинта на обновление записи
    onEditClick: Function, // Событие, вызываемое при нажатии на иконку карандаша для редактирования (ситуативно)
    delRecURL: String, // URL эндпоинта на удаление записи
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
    itemSelectEvent: Function, // Событие, вызываемое при выборе строки в таблице
    selectedItemObjectID: String, // object_id выбранного объекта для выделения в таблице
    defaultBody: Object, // Параметры для тела запроса по умолчанию (для добавления и редактирования объектов)
    // Параметр отображение только удаления записи в поле Управление
    onlyDelete: Boolean,
    // Функция для просмотра документов
    openDocViewerFunction: Function,
    // Функция для получения полной заявки в группе и просмотра анкеты
    selectGroupAppFunction: Function,
  },
  data() {
    return {
      // Список выбранных строк таблицы (для selection)
      itemsList: [],
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
      pageTotal: 0,
      itemsCount: 0
    }
  },
  methods: {
    // Добавление или удаление элементах из списка выбранных (для checkbox)
    itemAddOrDeleteInList(item) {
      if (item === 'all') {
        if (this.itemsList.length === 0) {
          this.recs.map((rec) => {
            if (!(this.itemsList.includes(rec.object_id))) {
              this.itemsList.push(rec.object_id)
            }
          })
        } else {
          if (this.itemsList.length === this.recs.length) {
            this.itemsList = []
          } else {
            this.recs.map((rec) => {
              if (!(this.itemsList.includes(rec.object_id))) {
                this.itemsList.push(rec.object_id)
              }
            })
          }
        }
      } else {
        if (this.itemsList.includes(item)) {
          this.itemsList = this.itemsList.filter((it) => it !== item)
        } else {
          this.itemsList.push(item)
        }
      }
    },
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
    async xlsxDownload() {
      showAlert(
        'success',
        'Выгрузка Excel',
        'Скачивание файла начнется автоматически после завершения формирования'
      )
      let xlsxRequest = await apiRequest(
        this.getRecsURL+'export/',
        'get',
        true,
        null,
        true,
      )
      if (xlsxRequest.status === 200) {
        let data = await xlsxRequest.blob()
        let a = document.createElement('a')
        a.href = window.URL.createObjectURL(data)
        a.download = this.tableTitle + '.xlsx'
        a.click()
      } else {
        showAlert(
          'error',
          'Выгрузка Excel',
          'Ошибка при формировании файла'
        )
      }
      // let xlsxHeaders = []
      // this.headers.map((header) => {
      //   xlsxHeaders.push(header.title)
      // })
      // xlsxDownloadFunction(
      //   this.tableTitle,
      //   xlsxHeaders,
      //   this.recs
      // )
    },
    async getRecs() {
      this.tableLoading = true
      let start = 0
      if (this.page !== 1) {
        start = (this.page-1)*this.pageRecCount
      }
      let url = this.getRecsURL
      if (this.getRecsURL.indexOf('?') !== -1) {
        url += '&size='+this.pageRecCount+'&start='+start+this.searchString
      } else {
        url += '?size='+this.pageRecCount+'&start='+start+this.searchString
      }
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
        this.itemsCount = getRecsRequest.count
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
        if (!((['checkbox', 'actions'].includes(header.key)))) {
          this.$refs['searchField_'+header.key][0].showField = !(this.$refs['searchField_'+header.key][0].showField)
        }
      })
    },
    showEditDialog(item) {
        this.$refs.editDialog.editedItem = item
        this.$refs.editDialog.editItemDialog = true
    },
    async deleteItem(object_id) {
      if (confirm('Вы уверены, что хотите удалить запись?')) {
        let deleteRequest = await apiRequest(
            this.delRecURL+object_id+'/',
            'DELETE',
            true,
            null
        )
        if (deleteRequest.error) {
          showAlert(
              'error',
              'Удаление записи',
              deleteRequest.error
          )
        }
        if (deleteRequest.success) {
          showAlert(
              'success',
              'Удаление записи',
              deleteRequest.success
          )
          this.getRecs()
        }
      }
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
  .one-line-text {
    white-space: nowrap;
  }
</style>
