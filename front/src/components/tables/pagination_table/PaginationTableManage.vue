<template>
  <v-toolbar
    color="coko-blue"
    flat
  >
    <v-toolbar-title
      bg-color="coko-blue"
    >

      {{ tableTitle }}

      <template v-if="itemsCount > 0">
        ({{itemsCount}} эл.)
      </template>
    </v-toolbar-title>

    <v-spacer></v-spacer>

    <v-divider
      class="mx-4"
      inset
      vertical
    ></v-divider>

    <v-btn
      v-if="!(hideSearchButton) && (!(mobileDisplay) && !(hideSearchButton))"
      :loading="tableLoading"
      prepend-icon="mdi-magnify"
      text="Поиск"
      @click="searchShowEvent()"
    />

    <v-btn
        v-if="mobileDisplay"
        icon="mdi-magnify"
        @click="$refs.searchDialog.dialog = true"
    />

    <CokoDialog
      v-if="mobileDisplay"
      ref="searchDialog"
      :cardActions="true"
    >

      <template v-slot:title>
        Поиск записей
      </template>

      <template v-slot:text>
        <v-container>
          <v-row>
            <template
                v-for="field in fieldsArray"
            >
              <v-col
                  v-if="(field.key !== 'actions') && (field.ui !== 'file')"
                  cols="12"
                  md="4"
                  sm="6"
              >
                <PaginationTableBaseField
                    :useInTableManage="true"
                    :checkRequired="false"
                    :field="field"
                    :fieldTitle = "tableHeaders.filter((header) => header.key === field.key)[0].title"
                    :onChangeEvent="onChangeEvent"
                />
              </v-col>
            </template>
          </v-row>
        </v-container>
      </template>

      <template v-slot:actions>
        <v-btn
            color="coko-blue"
            variant="text"
            @click="$refs.searchDialog.dialog = false"
        >
          ОК
        </v-btn>
      </template>

    </CokoDialog>

    <v-btn v-if="xlsxButton && !(foreignKey)"
      :loading="tableLoading"
      :icon="mobileDisplay && 'mdi-file-excel'"
      :prepend-icon="!(mobileDisplay) && 'mdi-file-excel'"
      :text="!(mobileDisplay) && 'Скачать'"
      @click="xlsxDownload()"
    />

    <PaginationTableAddDialog
      v-if="addButton && !(foreignKey) && !(addSpecialFunction)"
      :tableHeaders="tableHeaders"
      :fieldsArray="fieldsArray"
      :addRecURL="addRecURL"
      :getRecs="getRecs"
      :mobileDisplay="mobileDisplay"
      :defaultBody="defaultBody"
      :tableLoading="tableLoading"
    />

    <v-btn
      v-if="addButton && !(foreignKey) && addSpecialFunction"
      :loading="tableLoading"
      :icon="mobileDisplay && 'mdi-plus'"
      :prepend-icon="!(mobileDisplay) && 'mdi-plus'"
      :text="!(mobileDisplay) && 'Добавить'"
      @click="addSpecialFunction"
    />

    <v-btn
      v-if="foreignKey"
      :loading="tableLoading"
      :icon="mobileDisplay && 'mdi-open-in-new'"
      :prepend-icon="!(mobileDisplay) && 'mdi-open-in-new'"
      :text="!(mobileDisplay) && 'Перейти к таблице'"
      @click="nextPage()"
    />

  </v-toolbar>
</template>

<script>
import PaginationTableAddDialog from "@/components/tables/pagination_table/dialogs/PaginationTableAddDialog.vue";
import PaginationTableBaseField from "@/components/tables/pagination_table/PaginationTableBaseField.vue";
import CokoDialog from "@/components/dialogs/CokoDialog.vue";

export default {
  name: "PaginationTableManage",
  components: {CokoDialog, PaginationTableBaseField, PaginationTableAddDialog},
  props: {
    tableTitle: String, // Заголовок таблицы
    itemsCount: Number, // Количество записей в базе данных
    foreignKey: String, // FK таблица
    tableTabUrl: String, //URL перехода по кнопку "Перейти к таблице (для FK таблицы)"
    addButton: Boolean, // Параметр, отвечающий за отображение кнопки "Добавить"
    addSpecialFunction: Function, // Событие, вызываемое по нажатию на кнопку "Добавить" (если не подоходит стандартная форма)
    addRecURL: String, // URL эндпоинта для добавления новой записи
    getRecs: Function, // Функция для получения записей с backend
    // Параметр, отвечающий за отображение кнопки поиска
    hideSearchButton: Boolean,
    xlsxButton: Boolean, // Параметр, отвечающий за отображение кнопки "Скачать"
    xlsxDownload: Function, // Событий, вызываемое для выгрузки записей таблцы в Excel
    searchShowEvent: Function, // Функция для изменения параметра отображения поисковых полей,
    mobileDisplay: Boolean, // Отображение на дисплее мобильного устройства
    tableHeaders: Array, // Объект fieldsArray из пагинационной таблицы (для диалогового окна поиска записей)
    fieldsArray: Array, // Объект fieldsArray из пагинационной таблицы (для диалогового окна поиска записей)
    onChangeEvent: Function, // Функция для вызова поиска записей
    defaultBody: Object, // Параметры для тела запроса по умолчанию (для добавления и редактирования объектов)
    tableLoading: Boolean
  },
  data() {
    return {
      newItemDialog: false,
      searchDialog: false,
    }
  },
  methods: {
    nextPage() {
      let route = this.$router.resolve({path: this.tableTab});
      // let route = this.$router.resolve('/link/to/page'); // This also works.
      window.open(route.href, '_blank');
    }
  }
}
</script>

<style scoped>

</style>
