<template>

  <v-dialog
    persistent
    v-model="dialog"
  >

    <v-card class="lk-full-page-card">
      <v-card-title class="d-flex justify-space-between align-center">
        <v-tabs class="guides-tabs"
                v-model="programTab"
                bg-color="coko-blue"
                show-arrows
        >

          <v-tab
            class="coko-tab"
            value="info"
          >
            Информация
          </v-tab>

          <v-tab
            class="coko-tab"
            value="order"
          >
            Приказ
          </v-tab>

          <v-tab
            v-if="programObjectID"
            class="coko-tab"
            value="kug"
          >
            КУГ
          </v-tab>

        </v-tabs>

        <v-btn
          icon="mdi-close"
          color="coko-blue"
          @click="dialog = !(dialog)"
        ></v-btn>
      </v-card-title>

      <v-card-text>

        <v-alert
          id="error-program-detail-alert"
          class="alert-hidden"
          style="width: 100%"
          :text="programDetailError"
          type="error"
        ></v-alert>

        <v-container>

          <template v-if="programTab === 'info'">

            <v-row
              dense
            >

              <v-col
                cols="12"
                md="6"
                sm="6"
              >
                <v-select
                  bg-color="white"
                  variant="solo"
                  :items="adCentres"
                  v-model="programObject.department"
                  label="Подразделение*"
                  :loading="loading"
                />
              </v-col>

              <v-col
                cols="12"
                md="6"
                sm="6"
              >
                <v-select
                  bg-color="white"
                  variant="solo"
                  :items="programTypes"
                  v-model="programObject.type"
                  label="Тип*"
                  :loading="loading"
                />
              </v-col>

              <v-col
                cols="12"
                md="12"
                sm="12"
              >
                <v-textarea
                  bg-color="white"
                  variant="solo"
                  v-model="programObject.name"
                  label="Наименование*"
                  :loading="loading"
                />
              </v-col>



              <v-col
                cols="12"
                md="6"
                sm="6"
              >
                <v-number-input
                  bg-color="white"
                  variant="solo"
                  controlVariant="split"
                  label="Объем (часов)*"
                  :min="0"
                  v-model="programObject.duration"
                  :loading="loading"
                />
              </v-col>

              <v-col
                cols="12"
                md="6"
                sm="6"
              >
                <v-number-input
                  bg-color="white"
                  variant="solo"
                  controlVariant="split"
                  label="Цена (рублей)*"
                  :min="0"
                  :step="500"
                  v-model="programObject.price"
                  :loading="loading"
                />
              </v-col>

              <v-col
                cols="12"
                md="6"
                sm="6"
              >
                <v-textarea
                  bg-color="white"
                  variant="solo"
                  label="Аннотация"
                  v-model="programObject.annotation"
                  clearable
                  :loading="loading"
                />
              </v-col>

              <v-col
                cols="12"
                md="6"
                sm="6"
              >
                <v-select
                  bg-color="white"
                  variant="solo"
                  clearable
                  chips
                  multiple
                  label="Категории слушателей"
                  :items="audienceCategories"
                  v-model="programObject.categories"
                  :loading="loading"
                />
              </v-col>

            </v-row>

          </template>

          <template v-if="programTab === 'order'">

            <v-row
              dense
            >

              <v-col
                cols="12"
                md="6"
                sm="6"
              >
                <v-text-field
                  bg-color="white"
                  variant="solo"
                  v-model="orderObject.number"
                  label="Номер приказа"
                  :loading="loading"
                />
              </v-col>

              <v-col
                cols="12"
                md="6"
                sm="6"
              >
                <v-date-input
                  id="order_date"
                  bg-color="white"
                  label="Дата приказа"
                  prepend-icon=""
                  prepend-inner-icon="$calendar"
                  variant="solo"
                  :loading="loading"
                  clearable
                  @update:modelValue="(e) => {
                    this.orderObject.date = convertDateToBackend(e)
                  }"
                ></v-date-input>
              </v-col>

              <v-col
                cols="12"
                md="12"
                sm="12"
              >
                <v-file-input
                  bg-color="white"
                  v-model="orderObject.file"
                  variant="solo"
                  label="Скан файла приказа"
                />
              </v-col>

            </v-row>

          </template>



        </v-container>
        <small class="text-caption text-medium-emphasis">* - обязательные для заполнения поля</small>

      </v-card-text>

      <v-card-actions style="background-color: white">

        <v-spacer></v-spacer>

        <v-btn
          color="coko-blue"
          :text="programObjectID ? 'Сохранить' : 'Добавить'"
          :loading="loading"
          @click="saveProgram()"
        ></v-btn>
      </v-card-actions>

    </v-card>

  </v-dialog>

</template>

<script>
import {apiRequest} from "@/commons/api_request";
import {showAlert} from "@/commons/alerts";
import {convertDateToBackend} from "@/commons/date";

export default {
  name: "ProgramDetail",
  props: {
    programObjectID: String, // object_id ДПП (если редактирование объекта),
    adCentres: Array, // Список подразделений AD,
    audienceCategories: Array, // Список категорий слушателей,
    getRecs: Function // Функция для получения записи в пагинационной таблице
  },
  data() {
    return {
      dialog: false,
      loading: true,
      checkDataFill: true,
      programTab: 'info',
      programObject: null,
      orderObject: {
        'number': '',
        'date': '',
        'file': null,
      },
      programDetailError: '',
      programTypes: JSON.parse(import.meta.env.VITE_PROGRAM_TYPES)
    }
  },
  methods: {
    convertDateToBackend,
    setProgramObject() {
      if (this.programObjectID) {

      } else {
        this.programObject = {
          'department': '',
          'name': '',
          'type': '',
          'duration': 0,
          'categories': [],
          'annotation': '',
          'price': 0
        }
      }
    },
    hideProgramError() {
      document.querySelector('#error-program-detail-alert').classList.remove('alert-visible')
      document.querySelector('#error-program-detail-alert').classList.add('alert-hidden')
    },
    showProgramError(message) {
      this.programDetailError = message
      document.querySelector('#error-program-detail-alert').classList.add('alert-visible')
      document.querySelector('#error-program-detail-alert').classList.remove('alert-hidden')
    },
    checkDataFilled() {
      Object.keys(this.programObject).map((key) => {
        if (!(['categories', 'annotation'].includes(key))) {
          if ((this.programObject[key] === 0) || (this.programObject[key].length === 0)) {
            this.showProgramError('Заполните все обязательные поля формы')
            this.checkDataFill = false
          }
        }
      })
      let orderKeys = Object.keys(this.orderObject)
      if (orderKeys.filter((key) =>
        ['', null, undefined].includes(this.orderObject[key])).length !== 3) {
        orderKeys.map((key) => {
          if (['', null, undefined].includes(this.orderObject[key])) {
            this.showProgramError('Заполните все поля приказа, либо удалите всю информацию')
            this.checkDataFill = false
          }
        })
      }
    },
    async saveProgram() {
      this.hideProgramError()
      this.checkDataFill = true
      this.checkDataFilled()
      if (this.checkDataFill) {
        this.loading = true
        let form = new FormData()
        Object.keys(this.programObject).map((key) => {
          form.append(key, this.programObject[key])
        })
        if (!(['', null, undefined].includes(this.orderObject['file']))) {
          form.append('order_number', this.orderObject['number'])
          form.append('order_date', this.orderObject['date'])
          form.append('order_file', this.orderObject['file'])
        } else {
          form.append('order_file', null)
        }
        let url = '/backend/api/v1/edu/program/create/'
        let method = 'POST'
        if (this.programObjectID) {
          url = '/backend/api/v1/edu/program/update/'
          method = 'PATCH'
        }
        let programRequest = await apiRequest(
          url,
          method,
          true,
          form,
          false,
          true
        )
        if (programRequest.error) {
          this.showProgramError(programRequest.error)
        }
        if (programRequest.success) {
          this.dialog = false
          showAlert(
            'success',
            'ДПП',
            programRequest.success
          )
          this.getRecs()
        }
        this.loading = false
      }
    }
  },
  mounted() {
    this.setProgramObject()
    this.loading = false
  }
}
</script>

<style scoped>
  @import '../../../assets/css/alerts.css';
</style>
