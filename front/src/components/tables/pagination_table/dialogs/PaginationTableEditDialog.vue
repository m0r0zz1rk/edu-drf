<template>

  <CokoDialog
    ref="editItemDialog"
    :cardActions="true"
  >

    <template v-slot:title>
      Редактирование записи
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
                  :ref="'editField_'+column.key"
                  :fieldTitle="column.title"
                  :checkRequired="true"
                  :value="editedItem[column.key]"
                  :useInTableManage="true"
                  :field="fieldsArray.filter((field) => field.key === column.key)[0]"
              />

            </v-col>

          </template>


        </v-row>
        <v-alert
            id="error-edit-item-alert"
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
          @click="editItem()"
          :loading="loading"
      >
        Сохранить
      </v-btn>
    </template>

  </CokoDialog>
</template>

<script>
import PaginationTableBaseField from "@/components/tables/pagination_table/PaginationTableBaseField.vue";
import {apiRequest} from "@/commons/apiRequest";
import {showAlert} from "@/commons/alerts";
import CokoDialog from "@/components/dialogs/CokoDialog.vue";

export default {
  name: "PaginationTableEditDialog",
  components: {CokoDialog, PaginationTableBaseField},
  props: {
    tableHeaders: Array, // Список заголовков пагинационной таблицы
    fieldsArray: Array, // Список описаний полей пагинационной таблицы
    editRecURL: String, // URL эндпоинта для редактирования записи
    getRecs: Function, // Функция для получения записей с backend
    mobileDisplay: Boolean, // Отображение на мобильном устройстве
    defaultBody: Object, // Параметры для тела запроса по умолчанию (для добавления и редактирования объектов)
  },
  data() {
    return {
      editItemDialog: false,
      editedItem: null,
      errorMessage: '',
      requiredValid: false,
      loading: false
    }
  },
  methods: {
    showEditItemError(message) {
      this.errorMessage = message
      document.querySelector('#error-edit-item-alert').classList.add('alert-visible')
      document.querySelector('#error-edit-item-alert').classList.remove('alert-hidden')
    },
    checkRequired() {
      this.requiredValid = true
      let value = ''
      let addRequired = false
      this.tableHeaders.map((column) => {
        if (column.key !== 'actions') {
          value = this.$refs['editField_'+column.key][0].localValue
          addRequired = this.fieldsArray.filter((field) => field.key === column.key)[0].addRequired
          if (([null, undefined].includes(value) || value.length === 0) && addRequired) {
            this.requiredValid = false
            this.showEditItemError('Заполните все необходимые поля')
          }
        }
      })
    },
    async editItem() {
      this.checkRequired()
      if (this.requiredValid) {
        this.loading = true
        let body = {
          'object_id': this.editedItem.object_id
        }
        if (this.defaultBody) {
          Object.keys(this.defaultBody).map((key) => {
            body[key] = this.defaultBody[key]
          })
        }
        this.tableHeaders.map((column) => {
          if (column.key !== 'actions') {
            body[column.key] = this.$refs['editField_'+column.key][0].localValue
          }
        })
        let addItemRequest = await apiRequest(
            `${this.editRecURL}${this.editedItem.object_id}/`,
            'PATCH',
            true,
            body
        )
        if (addItemRequest.error) {
          this.showEditItemError(addItemRequest.error)
        }
        if (addItemRequest.success) {
          showAlert(
              'success',
              'Обновление записи',
              addItemRequest.success
          )
          this.$refs.editItemDialog.dialog = false
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
