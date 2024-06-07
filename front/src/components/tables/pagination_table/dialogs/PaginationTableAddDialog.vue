<template>
  <v-dialog
    persistent
    v-model="newItemDialog"
  >
    <template v-slot:activator="{ props }">

      <v-btn
        :icon="mobileDisplay && 'mdi-plus'"
        :prepend-icon="!(mobileDisplay) && 'mdi-plus'"
        :text="!(mobileDisplay) && 'Добавить'"
        @click="newItemDialog = !(newItemDialog)"
      />

    </template>
    <v-card>
      <v-card-title class="d-flex justify-space-between align-center">
        <span class="text-h5">Новая запись</span>
        <v-btn
          icon="mdi-close"
          color="coko-blue"
          @click="newItemDialog = !(newItemDialog)"
        ></v-btn>
      </v-card-title>

      <v-card-text>
        <v-container>
          <v-row>

            <template v-for="column in tableHeaders">

              <v-col
                v-if="column.key !== 'actions'"
                cols="12"
                md="4"
                sm="6"
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
      </v-card-text>

      <v-divider></v-divider>

      <v-card-actions>
        <v-spacer></v-spacer>
        <v-btn
          color="coko-blue"
          variant="text"
          @click="addItem"
          :loading="loading"
        >
          Сохранить
        </v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<script>
import PaginationTableBaseField from "@/components/tables/pagination_table/PaginationTableBaseField.vue";
import {apiRequest} from "@/commons/api_request";
import {showAlert} from "@/commons/alerts";

export default {
  name: "PaginationTableAddDialog",
  components: {PaginationTableBaseField},
  props: {
    tableHeaders: Array, // Список заголовков пагинационной таблицы
    fieldsArray: Array, // Список описаний полей пагинационной таблицы
    addRecURL: String, // URL эндпоинта для добавления новой записи
    getRecs: Function, // Функция для получения записей с backend
    mobileDisplay: Boolean, // Отображение на мобильном устройстве
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
        this.tableHeaders.map((column) => {
          if (column.key !== 'actions') {
            body[column.key] = this.$refs['addField_'+column.key][0].localValue
          }
        })
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
          this.newItemDialog = !this.newItemDialog
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
