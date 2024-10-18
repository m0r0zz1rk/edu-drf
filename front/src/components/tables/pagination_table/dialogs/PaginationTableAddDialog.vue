<template>

  <v-btn
      :icon="mobileDisplay && 'mdi-plus'"
      :prepend-icon="!(mobileDisplay) && 'mdi-plus'"
      :text="!(mobileDisplay) && 'Добавить'"
      @click="$refs.newItemDialog.dialog = true"
  />

  <CokoDialog
    ref="newItemDialog"
    :cardActions="true"
  >

    <template v-slot:title>
      Новая запись
    </template>

    <template v-slot:text>
      <v-container>
        <v-row>

          <template v-for="column in tableHeaders">

            <v-col
                v-if="column.key !== 'actions'"
                cols="12"
                md="12"
                sm="12"
            >

              <PaginationTableBaseField
                  v-if="column.key !== 'actions'"
                  :ref="'addField_'+column.key"
                  :fieldTitle="column.title"
                  :checkRequired="true"
                  :useInTableManage="true"
                  :field="fieldsArray.filter((field) => field.key === column.key)[0]"
              />

            </v-col>

          </template>

        </v-row>
        <v-alert
            id="error-add-item-alert"
            class="alert-hidden"
            style="width: 100%"
            :text="errorMessage"
            type="error"
        ></v-alert>
      </v-container>
    </template>

    <template v-slot:actions>
      <v-btn
          color="coko-blue"
          variant="text"
          @click="addItem"
          :loading="loading"
      >
        Сохранить
      </v-btn>
    </template>

  </CokoDialog>

</template>

<script>
import PaginationTableBaseField from "@/components/tables/pagination_table/PaginationTableBaseField.vue";
import {apiRequest} from "@/commons/api_request";
import {showAlert} from "@/commons/alerts";
import {getBase64} from "@/commons/files";
import fileContentTypes from "@/commons/consts/fileContentTypes";
import CokoDialog from "@/components/dialogs/CokoDialog.vue";

export default {
  name: "PaginationTableAddDialog",
  components: {CokoDialog, PaginationTableBaseField},
  props: {
    tableHeaders: Array, // Список заголовков пагинационной таблицы
    fieldsArray: Array, // Список описаний полей пагинационной таблицы
    addRecURL: String, // URL эндпоинта для добавления новой записи
    getRecs: Function, // Функция для получения записей с backend
    mobileDisplay: Boolean, // Отображение на мобильном устройстве
    defaultBody: Object // Параметры для тела запроса по умолчанию (для добавления и редактирования объектов)
  },
  data() {
    return {
      newItemDialog: false,
      errorMessage: '',
      requiredValid: false,
      loading: false
    }
  },
  methods: {
    showAddEditItemError(message) {
      this.errorMessage = message
      document.querySelector('#error-add-item-alert').classList.add('alert-visible')
      document.querySelector('#error-add-item-alert').classList.remove('alert-hidden')
    },
    checkRequired() {
      this.requiredValid = true
      let value = ''
      let addRequired = false
      this.tableHeaders.map((column) => {
        if (column.key !== 'actions') {
          value = this.$refs['addField_'+column.key][0].localValue
          addRequired = this.fieldsArray.filter((field) => field.key === column.key)[0].addRequired
          if (([null, undefined].includes(value) || value.length === 0) && addRequired) {
            this.requiredValid = false
            this.showAddEditItemError('Заполните все необходимые поля')
          }
        }
      })
    },
    async addItem() {
      this.checkRequired()
      if (this.requiredValid) {
        this.loading = true
        let body = {}
        if (this.defaultBody) {
          Object.keys(this.defaultBody).map((key) => {
            body[key] = this.defaultBody[key]
          })
        }
        if (this.fieldsArray.filter((fa) => fa.ui === 'file').length > 0) {
          body[this.fieldsArray.filter((fa) => fa.ui === 'file')[0].key] =
              await getBase64(document.querySelector('#addDialogFileInput').files[0])
        }
        this.tableHeaders.map((column) => {
          if (column.key !== 'actions') {
            if (this.fieldsArray.filter((fa) => fa.key === column.key)[0].ui !== 'file') {
              body[column.key] = this.$refs['addField_' + column.key][0].localValue
            }
          }
        })
        console.log(body)
        let addItemRequest = await apiRequest(
          this.addRecURL,
          'POST',
          true,
          body
        )
        if (addItemRequest.error) {
          this.showAddEditItemError(addItemRequest.error)
        }
        if (addItemRequest.success) {
          showAlert(
            'success',
            'Добавление записи',
            addItemRequest.success
          )
          this.$refs.newItemDialog.dialog = false
          this.getRecs()
        }
        this.loading = false
      }
    }
  }
}
</script>

<style scoped>
.alert-visible {
  z-index: 100;
}

.alert-hidden {
  display: none;
  z-index: 0;
}
</style>
