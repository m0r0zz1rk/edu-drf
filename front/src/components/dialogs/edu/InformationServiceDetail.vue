<template>

  <v-dialog
    persistent
    v-model="dialog"
  >

    <v-card class="lk-full-page-card">
      <v-card-title class="d-flex justify-space-between align-center">

        <p v-if="informationServiceID">Редактирование мероприятия</p>

        <p v-if="!(informationServiceID)">Добавление мероприятия</p>

        <v-btn
          icon="mdi-close"
          color="coko-blue"
          @click="dialog = !(dialog)"
        />
      </v-card-title>

      <v-card-text>

        <v-alert
          id="error-information-service-alert"
          class="alert-hidden"
          style="width: 100%"
          :text="informationServiceError"
          type="error"
        ></v-alert>

        <v-container>

            <v-row
              v-if="informationService"
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
                  v-model="informationService.department"
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
                  :items="ikuTypes"
                  v-model="informationService.type"
                  label="Тип*"
                  :loading="loading"
                />
              </v-col>

              <v-col
                cols="12"
                md="12"
                sm="12"
              >
                <v-text-field
                  bg-color="white"
                  variant="solo"
                  v-model="informationService.name"
                  label="Наименование*"
                  :loading="loading"
                />
              </v-col>

              <v-col
                cols="12"
                md="12"
                sm="12"
              >
                <v-text-field
                  bg-color="white"
                  variant="solo"
                  v-model="informationService.location"
                  label="Место проведения*"
                  :loading="loading"
                />
              </v-col>

              <v-col
                cols="12"
                md="12"
                sm="12"
              >
                <v-select
                  bg-color="white"
                  variant="solo"
                  clearable
                  chips
                  multiple
                  label="Категории слушателей"
                  :items="audienceCategories"
                  v-model="informationService.categories"
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
                  v-model="informationService.duration"
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
                  v-model="informationService.price"
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
                  label="Дата начала проведения*"
                  v-model="informationService.date_start"
                  prepend-icon=""
                  prepend-inner-icon="$calendar"
                  variant="solo"
                  :loading="loading"
                  clearable
                ></v-date-input>
              </v-col>

              <v-col
                cols="12"
                md="6"
                sm="6"
              >
                <v-date-input
                  id="orderDate"
                  bg-color="white"
                  label="Дата окончания проведения*"
                  v-model="informationService.date_end"
                  prepend-icon=""
                  prepend-inner-icon="$calendar"
                  variant="solo"
                  :loading="loading"
                  clearable
                ></v-date-input>
              </v-col>

            </v-row>

        </v-container>
        <small class="text-caption text-medium-emphasis">
          * - обязательные для заполнения поля
        </small>

      </v-card-text>

      <v-card-actions
        style="background-color: white"
      >

        <v-spacer></v-spacer>

        <v-btn
          color="coko-blue"
          :text="[undefined, null].includes(informationServiceID) ? 'Добавить' : 'Сохранить'"
          :loading="loading"
          @click="saveInformationService()"
        ></v-btn>
      </v-card-actions>

    </v-card>

  </v-dialog>

</template>

<script>
import PaginationTable from "@/components/tables/pagination_table/PaginationTable.vue";
import {convertBackendDate, convertDateToBackend} from "@/commons/date";
import {apiRequest} from "@/commons/api_request";
import {showAlert} from "@/commons/alerts";

// Компонент для работы с объектом мероприятия (просмотр, добавление и редактирование ИКУ)
export default {
  name: "InformationServiceDetail",
  components: {PaginationTable},
  props: {
    adCentres: Array, // Список наименований подразделений ЦОКО,
    ikuTypes: Array, // Список типов мероприятий (ИКУ)
    audienceCategories: Array, // Список категорий слушателей
    getRecsFunction: Function, // Метод для вызова получения записей в пагинационной таблице в родителе
  },
  data() {
    return {
      informationServiceID: null, // object_id объекта мероприятия (при редактировании)
      dialog: false, // Параметр отображения диалогового окна
      loading: false, // Параметр отобажения индикатора загрузки на компонентах формы
      informationServiceError: '', // Текст ошибки, возникшей в процессе добавления/редактирования мероприятия
      informationService: null, // установленный объект мероприятия
    }
  },
  methods: {
    // Скрыть оповещение об ошибке в процессе работы с ИКУ (мероприятием)
    hideInformationServiceError() {
      document.querySelector('#error-information-service-alert').classList.remove('alert-visible')
      document.querySelector('#error-information-service-alert').classList.add('alert-hidden')
    },
    // Показать оповещение об ошибке в процессе работы с ИКУ (мероприятием)
    showInformationServiceError(message) {
      this.informationServiceError = message
      document.querySelector('#error-information-service-alert').classList.add('alert-visible')
      document.querySelector('#error-information-service-alert').classList.remove('alert-hidden')
    },
    // Смена object_id ИКУ
    changeServiceID(object_id) {
      if (object_id === this.informationServiceID) {
        this.dialog = true
      } else {
        this.informationServiceID = object_id
      }
    },
    // Установка данных ИКУ (при редактировании)
    async setInformationService() {
      this.loading = true
      if (!([undefined, null].includes(this.informationServiceID))) {
        let informationServiceRequest = await apiRequest(
          '/backend/api/v1/edu/information_service/'+this.informationServiceID+'/',
          'GET',
          true,
          null
        )
        if (informationServiceRequest.error) {
          this.showInformationServiceError(informationServiceRequest.error)
        } else {
          this.informationService = informationServiceRequest
          this.informationService['categories'] = informationServiceRequest['categories'].split(';; ')
        }
      } else {
        this.informationService = {
          "object_id": null,
          "department": null,
          "type": null,
          "name": null,
          "categories": null,
          "location": null,
          "duration": null,
          "price": null,
          "date_start": null,
          "date_end": null
        }
      }
      this.dialog = true
      this.loading = false
    },
    // Сохранение/добавление ИКУ
    async saveInformationService() {
      this.hideInformationServiceError()
      let checkData = true
      Object.keys(this.informationService).map((key) => {
        if ((key !== 'object_id') && (
          ([undefined, null].includes(this.informationService[key]) ||
            (this.informationService[key].length === 0)))
        ) {
          this.showInformationServiceError('Проверьте заполнение всех полей формы')
          checkData = false
        }
      })
      if (!(checkData)) {
        return false
      }
      this.loading = true
      let body = {}
      Object.keys(this.informationService).map((key) => {
        if (key.includes('date')) {
          body[key] = convertDateToBackend(this.informationService[key])
        } else if (key === 'categories') {
          let cats = ''
          this.informationService['categories'].map((cat) => {
            cats += cat+';;'
          })
          body[key] = cats.slice(0, -2)
        } else {
          body[key] = this.informationService[key]
        }
      })
      let addUpdateRequest = await apiRequest(
        '/backend/api/v1/edu/information_service/',
        'POST',
        true,
        body
      )
      if (addUpdateRequest.error) {
        this.showInformationServiceError(addUpdateRequest.error)
      } else {
        showAlert(
          'success',
          'ИКУ (мероприятие)',
          addUpdateRequest.success
        )
        this.dialog = false
        this.getRecsFunction()
      }
      this.loading = false
    }
  },
  watch: {
    // Преобразование даты форма дд.мм.гггг в объект Date при изменении информации о приказе ДПП
    informationService: function() {
      if (this.informationService.date_start !== null) {
        try {
          this.informationService.date_start = convertBackendDate(this.informationService.date_start)
        } catch (e) {
          this.informationService.date_start = new Date(this.informationService.date_start)
        }
      }
      if (this.informationService.date_end !== null) {
        try {
          this.informationService.date_end = convertBackendDate(this.informationService.date_end)
        } catch (e) {
          this.informationService.date_end = new Date(this.informationService.date_end)
        }
      }
    },
    // Получение объекта ИКУ в случае изменений ID объекта
    informationServiceID: async function() {
      await this.setInformationService()
    }
  }
}
</script>

<style scoped>
  @import '../../../assets/css/alerts.css';
</style>
