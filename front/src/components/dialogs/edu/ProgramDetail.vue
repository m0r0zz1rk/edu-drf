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
            v-if="programObjectID !== null"
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
                  v-model="orderObject.order_number"
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
                  id="orderDate"
                  bg-color="white"
                  label="Дата приказа"
                  v-model="orderObject['order_date']"
                  prepend-icon=""
                  prepend-inner-icon="$calendar"
                  variant="solo"
                  :loading="loading"
                  clearable
                ></v-date-input>
              </v-col>

              <v-col
                cols="12"
                md="12"
                sm="12"
              >
                <template
                  v-if="orderObject.order_id"
                >

                  Скачать установленный файл:
                  <v-icon
                    icon="mdi-tray-arrow-down"
                    @click="downloadFile()"
                  />
                  <br/><br/>

                </template>

                <v-file-input
                  bg-color="white"
                  v-model="orderObject.order_file"
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
          :text="programObjectID !== null ? 'Сохранить' : 'Добавить'"
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
import contentTypeFormats from "@/commons/consts/contentTypeFormats";
import {convertDateToBackend} from "@/commons/date";

export default {
  name: "ProgramDetail",
  props: {
    adCentres: Array, // Список подразделений AD,
    audienceCategories: Array, // Список категорий слушателей,
    getRecs: Function // Функция для получения записи в пагинационной таблице
  },
  data() {
    return {
      programObjectID: '',
      dialog: false,
      loading: true,
      checkDataFill: true,
      programTab: 'info',
      programObject: {},
      orderObject: {
        'order_id': null,
        'order_number': '',
        'order_date': '',
        'order_file': null,
      },
      programDetailError: '',
      programTypes: JSON.parse(import.meta.env.VITE_PROGRAM_TYPES)
    }
  },
  methods: {
    setProgramObject(dppId) {
      this.orderObject = {
        'order_id': null,
        'order_number': '',
        'order_date': '',
        'order_file': null,
      }
      Object.keys(this.programObject).map((key) => {
        this.programObject[key] = null
      })
      Object.keys(this.orderObject).map((key) => {
        this.orderObject[key] = null
      })
      this.programObjectID = dppId
      this.dialog = true
      this.loading = true
      if (this.programObjectID !== null) {
        apiRequest(
          '/backend/api/v1/edu/program/'+this.programObjectID+'/',
          'GET',
          true,
          null
        )
          .then((data) => {
            if (data.error) {
              this.showProgramError(data.error)
            } else {
              console.log(data)
              Object.keys(data).map((key) => {
                if (!(Object.keys(this.orderObject).includes(key))) {
                  this.programObject[key] = data[key]
                }
              })
              this.programObject['categories'] = data['categories'].split(', ')
              let orderData = {}
              Object.keys(this.orderObject).map((key) => {
                if (key !== 'order_file') {
                  orderData[key] = data[key]
                }
              })
              this.orderObject = orderData
            }
            this.loading = false
          })
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
        this.loading = false
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
        if (!([
          'categories',
          'annotation',
          'object_id',
          'order_id',
          'order_number',
          'order_date',
          'order_file'].includes(key))) {
          if ((this.programObject[key] === 0) || (this.programObject[key].length === 0)) {
            this.showProgramError('Заполните все обязательные поля формы')
            this.checkDataFill = false
          }
        }
      })
      let orderKeys = Object.keys(this.orderObject)
      if (orderKeys.filter((key) =>
        ['', null, undefined].includes(this.orderObject[key])).length !== 4) {
        orderKeys.map((key) => {
          if ((key !== 'order_id') && (['', null, undefined].includes(this.orderObject[key]))) {
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
        console.log(this.programObject)
        console.log(this.orderObject)
        if (!(Object.keys(this.programObject).includes('object_id'))) {
          form.append('object_id', null)
        }
        Object.keys(this.programObject).map((key) => {
          form.append(key, this.programObject[key])
        })
        Object.keys(this.orderObject).map((key) => {
          if (this.orderObject[key] instanceof Date) {
            form.append(key, convertDateToBackend(this.orderObject[key]))
          } else {
            if (key !== 'order_file') {
              form.append(key, this.orderObject[key])
            }
          }
        })
        if (!(["string", "undefined", "null"].includes(typeof this.orderObject['order_file']))) {
          form.append('order_file', this.orderObject['order_file'])
        }
        let programRequest = await apiRequest(
          '/backend/api/v1/edu/program/create_update/',
          'POST',
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
    },
    async downloadFile() {
      let orderRequest = await apiRequest(
        '/backend/api/v1/edu/program/order_file/'+this.programObjectID+'/',
        'GET',
        true,
        false,
        true
      )
      let contentType = orderRequest.headers.get('Content-Type')
      let getBlob = await orderRequest.blob();
      let url = window.URL.createObjectURL(getBlob);
      var a = document.createElement('a');
      a.href = url;
      a.download = this.orderObject.order_number+contentTypeFormats[contentType];
      document.body.appendChild(a);
      a.click();
      a.remove();
    }
  },
  watch: {
    orderObject: function() {
      if (this.orderObject['order_date'] !== null) {
        this.orderObject['order_date'] = new Date(this.orderObject['order_date'])
      }
    }
  },
  mounted() {
    this.loading = false
  }
}
</script>

<style scoped>
  @import '../../../assets/css/alerts.css';
</style>
