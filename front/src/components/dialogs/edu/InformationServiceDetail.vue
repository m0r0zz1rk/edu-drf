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

        <DialogContentWithError ref="content-error">

          <slot>

            <v-row
              v-if="informationService"
              dense
            >

              <v-col
                v-if="userRole === 'centre'"
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
                  v-mask="'##.##.####'"
                  v-model="informationService.date_start"
                  @input="e => e.target.value.length === 10 ? informationService.date_start = e.target.value : ''"
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
                  v-mask="'##.##.####'"
                  v-model="informationService.date_end"
                  @input="e => e.target.value.length === 10 ? informationService.date_end = e.target.value : ''"
                  prepend-icon=""
                  prepend-inner-icon="$calendar"
                  variant="solo"
                  :loading="loading"
                  clearable
                ></v-date-input>
              </v-col>

            </v-row>

          </slot>

        </DialogContentWithError>

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
import {apiRequest} from "@/commons/apiRequest";
import {showAlert} from "@/commons/alerts";
import DialogContentWithError from "@/components/dialogs/DialogContentWithError.vue";

// Компонент для работы с объектом мероприятия (просмотр, добавление и редактирование ИКУ)
export default {
  name: "InformationServiceDetail",
  components: {DialogContentWithError, PaginationTable},
  props: {
    adCentres: Array, // Список наименований подразделений ЦОКО,
    ikuTypes: Array, // Список типов мероприятий (ИКУ)
    audienceCategories: Array, // Список категорий слушателей
    getRecsFunction: Function, // Метод для вызова получения записей в пагинационной таблице в родителе
    // Роль пользователя (centre или dep)
    userRole: String,
    // ObjectGUID подразеделения пользвоателя
    userDep: String,
    // Наименование подразделения пользователя
    userDepDisplay: String
  },
  data() {
    return {
      informationServiceID: null, // object_id объекта мероприятия (при редактировании)
      dialog: false, // Параметр отображения диалогового окна
      loading: false, // Параметр отобажения индикатора загрузки на компонентах формы
      informationService: {
        "object_id": null,
        "department": null,
        "type": null,
        "name": null,
        "categories": null,
        "location": 'ГАУ ИО ЦОПМКиМКО',
        "duration": null,
        "price": null,
        "date_start": null,
        "date_end": null
      }, // установленный объект мероприятия
    }
  },
  methods: {
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
          this.$refs["content-error"].showContentError(informationServiceRequest.error)
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
          "location": 'ГАУ ИО ЦОПМКиМКО',
          "duration": null,
          "price": null,
          "date_start": null,
          "date_end": null
        }
        if (this.userRole !== 'centre') {
          this.informationService.deparment = this.userDepDisplay
        }
      }
      this.dialog = true
      this.loading = false
    },
    // Сохранение/добавление ИКУ
    async saveInformationService() {
      this.$refs["content-error"].hideContentError()
      let checkData = true
      let url = '/backend/api/v1/edu/information_service/'
      let method = 'POST'
      if (this.informationService.object_id !== null) {
        url += this.informationService.object_id+'/'
        method = 'PATCH'
      }
      if (this.userRole === 'dep') {
        this.informationService.department = this.userDepDisplay
      }
      Object.keys(this.informationService).map((key) => {
        if ((key !== 'object_id') && (
          ([undefined, null].includes(this.informationService[key]) ||
            (this.informationService[key].length === 0)))
        ) {
          this.$refs["content-error"].showContentError('Проверьте заполнение всех полей формы')
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
        url,
        method,
        true,
        body
      )
      if (addUpdateRequest.error) {
        this.$refs["content-error"].showContentError(addUpdateRequest.error)
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
    informationService: {
      handler() {
        console.log('date_start: ', this.informationService.date_start)
        if (this.informationService.date_start !== null && this.informationService.date_start.length === 10) {
          try {
            console.log('date_start: ', this.informationService.date_start)
            this.informationService.date_start = convertBackendDate(this.informationService.date_start)
          } catch (e) {
            this.informationService.date_start = new Date(this.informationService.date_start)
          }
        }
        if (this.informationService.date_end !== null && this.informationService.date_end.length === 10) {
          try {
            this.informationService.date_end = convertBackendDate(this.informationService.date_end)
          } catch (e) {
            this.informationService.date_end = new Date(this.informationService.date_end)
          }
        }
      },
      deep: true
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
