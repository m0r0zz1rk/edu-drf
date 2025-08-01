<template>

  <v-dialog
    persistent
    v-model="dialog"
  >

    <v-card class="lk-full-page-card">
      <v-card-title class="d-flex justify-space-between align-center">
        <v-tabs
          v-model="educationServiceTab"
          bg-color="coko-blue"
          show-arrows
        >

          <v-tab
            class="coko-tab"
            value="dpp"
          >
            ДПП
          </v-tab>

          <v-tab
            class="coko-tab"
            value="info"
          >
            Детали
          </v-tab>

        </v-tabs>

        <v-btn
          icon="mdi-close"
          color="coko-blue"
          @click="dialog = !(dialog)"
        />
      </v-card-title>

      <v-card-text>

        <v-alert
          id="error-education-service-alert"
          class="alert-hidden"
          style="width: 100%"
          :text="educationServiceError"
          type="error"
        ></v-alert>

        <v-container>

          <DialogContentWithError ref="content-error">

            <slot>

              <template v-if="educationServiceTab === 'dpp'">

                <div v-if="educationService && educationService.program">
                  <b>Выбранная программа: </b><br/>
                  <v-expansion-panels>
                    <v-expansion-panel>
                      <v-expansion-panel-title
                        color="coko-blue"
                      >{{educationService.program.name}}</v-expansion-panel-title>
                      <v-expansion-panel-text>
                        <div v-if="userRole === 'centre'">
                          <b>Подразделение:</b><br/>
                          {{educationService.program.department}}<br/><br/>
                        </div>
                        <b>Объем часов:</b><br/>
                        {{educationService.program.duration}}<br/><br/>
                        <b>Категории слушателей:</b><br/>
                        {{educationService.program.categories}}<br/><br/>
                        <b>Аннотация:</b><br/>
                        {{educationService.program.annotation}}<br/><br/>
                        <b>Стоимость:</b><br/>
                        {{educationService.program.price}}<br/><br/>
                      </v-expansion-panel-text>
                    </v-expansion-panel>
                  </v-expansion-panels>
                </div><br/>

                <PaginationTable
                  v-if="!([0, 1].includes(programTableHeaders.length))"
                  tableTitle="ДПП"
                  tableWidth="98"
                  :noTab="false"
                  :addButton="false"
                  :xlsxButton="false"
                  :getRecsURL="
                    userRole === 'centre' ?
                      '/backend/api/v1/edu/approved_program/'
                      :
                      `/backend/api/v1/edu/approved_program?dep=${userDep}`
                  "
                  :tableHeaders="programTableHeaders"
                  :fieldsArray="programFieldsArray"
                  :itemSelectEvent="changeDpp"
                  :selectedItemObjectID="educationService.program && educationService.program.object_id"
                />

              </template>

              <template v-if="educationServiceTab === 'info'">

                <v-row
                  v-if="educationService"
                  dense
                >

                  <v-col
                    cols="12"
                    md="4"
                    sm="6"
                  >
                    <v-text-field
                      bg-color="white"
                      variant="solo"
                      v-model="educationService.location"
                      label="Место проведения*"
                      :loading="loading"
                    />
                  </v-col>

                  <v-col
                    cols="12"
                    md="4"
                    sm="6"
                  >
                    <v-date-input
                      id="orderDate"
                      bg-color="white"
                      label="Дата начала проведения*"
                      v-mask="'##.##.####'"
                      v-model="educationService.date_start"
                      @input="e => e.target.value.length === 10 ? educationService.date_start = e.target.value : ''"
                      prepend-icon=""
                      prepend-inner-icon="$calendar"
                      variant="solo"
                      :loading="loading"
                      clearable
                    ></v-date-input>
                  </v-col>

                  <v-col
                    cols="12"
                    md="4"
                    sm="6"
                  >
                    <v-date-input
                      id="orderDate"
                      bg-color="white"
                      label="Дата окончания проведения*"
                      v-mask="'##.##.####'"
                      v-model="educationService.date_end"
                      @input="e => e.target.value.length === 10 ? educationService.date_end = e.target.value : ''"
                      prepend-icon=""
                      prepend-inner-icon="$calendar"
                      variant="solo"
                      :loading="loading"
                      clearable
                    ></v-date-input>
                  </v-col>

                </v-row>

              </template>

            </slot>

          </DialogContentWithError>

        </v-container>
        <small v-if="educationServiceTab === 'info'" class="text-caption text-medium-emphasis">
          * - обязательные для заполнения поля
        </small>

      </v-card-text>

      <v-card-actions
        style="background-color: white"
      >

        <v-spacer></v-spacer>

        <v-btn
          color="coko-blue"
          :text="[undefined, null].includes(educationServiceID) ? 'Добавить' : 'Сохранить'"
          :loading="loading"
          @click="saveEducationService()"
        ></v-btn>
      </v-card-actions>

    </v-card>

  </v-dialog>

</template>

<script>
import KUGTable from "@/components/tables/KUGTable.vue";
import PaginationTable from "@/components/tables/pagination_table/PaginationTable.vue";
import {apiRequest} from "@/commons/apiRequest";
import {showAlert} from "@/commons/alerts";
import {convertBackendDate, convertDateToBackend} from "@/commons/date";
import DialogContentWithError from "@/components/dialogs/DialogContentWithError.vue";

// Компонент для добавления/изменения образовательной услуги (курса)
export default {
  name: "EducationServiceDetail",
  components: {DialogContentWithError, PaginationTable, KUGTable},
  props: {
    getRecsFunction: Function, // функция для получения записей в родительской пагинационной таблицы
                               // после добавления/обновления курса
    // Роль пользователя
    userRole: String,
    // ObjectGUID подразделения пользователя
    userDep: String
  },
  data() {
    return {
      educationServiceID: null, // object_id переданной образовательной услуги (или null)
      dialog: false, // Параметр отображения диалогового окна
      loading: true, // Параметр отображения загрузки элемент формы в диалоговом окне
      educationServiceTab: 'dpp', // Выбранная вкладка в диалоговом окне
      educationService: {
        "object_id": null,
        "program": null,
        "date_start": null,
        "date_end": null,
        "location": null
      }, // Объект образовательной услуги (при наличии)
      programTableHeaders: [], // Заголовки для пагинационной таблицы для выбора ДПП
      programFieldsArray: [] // Описание полей пагинационной таблицы для выбора ДПП
    }
  },
  methods: {
    // Получение столбцов и описаний в зависимости от роли
    getTableData() {
      if (this.userRole === 'centre') {
        this.programTableHeaders = [
          {
            'title': 'Подразделение',
            'key': 'department'
          },
        ]
        this.programFieldsArray = [
          {
            ui: 'input',
            type: 'text',
            key: 'department',
            addRequired: true,
          },
        ]
      }
      this.programFieldsArray.push.apply(this.programFieldsArray, [
        {
          ui: 'input',
          type: 'text',
          key: 'name',
          addRequired: true,
        },
        {
          ui: 'input',
          type: 'number',
          key: 'duration',
          addRequired: true,
        },
        {
          ui: 'input',
          type: 'text',
          key: 'order_number',
          addRequired: false,
        },
        {
          ui: 'date',
          key: 'order_date',
          addRequired: false,
        }
      ])
      this.programTableHeaders.push.apply(this.programTableHeaders, [
        {
          'title': 'Наименование',
          'key': 'name'
        },
        {
          'title': 'Объем (часов)',
          'key': 'duration'
        },
        {
          'title': 'Номер приказа',
          'key': 'order_number'
        },
        {
          'title': 'Дата приказа',
          'key': 'order_date'
        }
      ])
    },
    // Смена object_id образовательной услуги
    changeServiceID(object_id) {
      if (object_id === this.educationServiceID) {
        this.dialog = true
      } else {
        this.educationServiceID = object_id
      }
    },
    // Установка данных образовательной услуги (при редактировании)
    async setEducationService() {
      this.loading = true
      if (!([undefined, null].includes(this.educationServiceID))) {
        let educationServiceRequest = await apiRequest(
          '/backend/api/v1/edu/education_service/'+this.educationServiceID+'/',
          'GET',
          true,
          null
        )
        if (educationServiceRequest.error) {
          this.$refs["content-error"].showContentError(educationServiceRequest.error)
        } else {
          this.educationService = educationServiceRequest
        }
      } else {
        this.educationService = {
          "object_id": null,
          "program": null,
          "date_start": null,
          "date_end": null,
          "location": 'ГАУ ИО ЦОПМКиМКО'
        }
      }
      this.dialog = true
      this.loading = false
    },
    // Изменение выбранной ДПП при нажатии на строку таблицы
    async changeDpp(item) {
      this.loading = true
      let programRequest = await apiRequest(
        '/backend/api/v1/edu/program/'+item.object_id+'/',
        'GET',
        true,
        null
      )
      if (programRequest.error) {
        showAlert(
          'error',
          'Получение ДПП',
          programRequest.error
        )
      } else {
        this.educationService.program = programRequest
      }
      this.loading = false
    },
    // Сохранение/добавление образовательной услуги
    async saveEducationService() {
      this.$refs["content-error"].hideContentError()
      let checkData = true
      Object.keys(this.educationService).map((key) => {
        if ((key !== 'object_id') && (
          ([undefined, null].includes(this.educationService[key]) ||
          (this.educationService[key].length === 0)))
        ) {
          this.$refs["content-error"].showContentError('Не выбрано ДПП или заполнены не все поля формы')
          checkData = false
        }
      })
      if (!(checkData)) {
        return false
      }
      this.loading = true
      let body = {}
      let url = '/backend/api/v1/edu/education_service/'
      let method = 'POST'
      if (this.educationService.object_id !== null) {
        url += this.educationService.object_id+'/'
        method = 'PATCH'
      }
      Object.keys(this.educationService).map((key) => {
        if (key === 'program') {
          body[key] = this.educationService.program.object_id
        } else if (key.includes('date')) {
          body[key] = convertDateToBackend(this.educationService[key])
        } else {
          body[key] = this.educationService[key]
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
          'Образовательная услуга (курс)',
          addUpdateRequest.success
        )
        this.dialog = false
        this.getRecsFunction()
      }
      this.loading = false
    }
  },
  mounted() {
    this.getTableData()
  },
  watch: {
    // Преобразование даты форма дд.мм.гггг в объект Date при изменении информации о приказе ДПП
    educationService: {
      handler() {
        if (this.educationService.date_start !== null && this.educationService.date_start.length === 10) {
          try {
            this.educationService.date_start = convertBackendDate(this.educationService.date_start)
          } catch (e) {
            this.educationService.date_start = new Date(this.educationService.date_start)
          }
        }
        if (this.educationService.date_end !== null) {
          try {
            this.educationService.date_end = convertBackendDate(this.educationService.date_end)
          } catch (e) {
            this.educationService.date_end = new Date(this.educationService.date_end)
          }
        }
      },
      deep: true
    },
    educationServiceID: async function() {
      await this.setEducationService()
    }
  },
}
</script>

<style scoped>
  @import '../../../assets/css/alerts.css';
</style>
