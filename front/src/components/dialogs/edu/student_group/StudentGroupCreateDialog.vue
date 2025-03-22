<template>

  <v-dialog
    persistent
    v-model="dialog"
  >

    <v-card class="lk-full-page-card">
      <v-card-title class="d-flex justify-space-between align-center">

        Новая учебная группа

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
              dense
            >

              <v-col
                cols="12"
                md="12"
                sm="12"
              >
                <v-select
                  bg-color="white"
                  variant="solo"
                  v-model="serviceType"
                  :items="serviceTypes"
                  item-title="title"
                  item-value="key"
                  label="Тип услуги"
                  :loading="loading"
                />
              </v-col>

              <v-col
                cols="12"
                md="12"
                sm="12"
              >
                <table style="border: 0">
                  <tr>
                    <td rowspan="2">
                      <p v-if="newGroup.type === 'ou'">Выбранный курс:</p>
                      <p v-if="newGroup.type === 'iku'">Выбранное мероприятие:</p>
                    </td>
                    <td style="margin-left: 15px;">

                      <b
                        v-if="newGroup.service_id === null"
                      >
                        Не выбран
                      </b>

                      <b
                        v-if="newGroup.service_id !== null"
                      >
                        {{selectedServiceName}}
                      </b>
                    </td>
                  </tr>
                  <tr>
                    <td style="margin-left: 15px">

                      <v-btn
                        color="coko-blue"
                        :loading="loading"
                        @click="serviceChooseDialog = !(serviceChooseDialog)"
                      >
                        Выбрать
                      </v-btn>

                    </td>
                  </tr>
                </table>
              </v-col>

              <v-col
                v-if="newGroup.type === 'iku'"
                cols="12"
                md="12"
                sm="12"
              >
                <v-number-input
                  bg-color="white"
                  variant="solo"
                  v-model="newGroup.plan_seats_number"
                  label="Плановое количество мест"
                  :min="1"
                  :loading="loading"
                />
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
          text="Создать"
          :loading="loading"
          @click="saveStudentGroup()"
        ></v-btn>
      </v-card-actions>

    </v-card>

  </v-dialog>

  <v-dialog
    persistent
    v-model="serviceChooseDialog"
  >

    <v-card class="lk-full-page-card">
      <v-card-title class="d-flex justify-space-between align-center">

        <p
          v-if="newGroup.type === 'ou'"
        >
          Выбор ОУ (курса)
        </p>

        <p
          v-if="newGroup.type === 'iku'"
        >
          Выбор ИКУ (мероприятия)
        </p>

        <v-btn
          icon="mdi-close"
          color="coko-blue"
          @click="serviceChooseDialog = !(serviceChooseDialog)"
        />
      </v-card-title>

      <PaginationTable
        :tableTitle="newGroup.type === 'ou' ? 'ОУ (Курс)' : 'ИКУ (Мероприятие)'"
        tableWidth="80"
        :noTab="false"
        :addButton="false"
        :xlsxButton="false"
        :getRecsURL="getRecsURL"
        :tableHeaders="
            [
              {
                'key': newGroup.type === 'ou' ? 'program' : 'name',
                'title': 'Наименование услуги'
              },
              ...servicesTableHeaders
            ]
        "
        :fieldsArray="
            [
              {
                ui: 'input',
                type: 'text',
                key: newGroup.type === 'ou' ? 'program' : 'name',
                addRequired: true,
              },
              ...servicesFieldsArray
            ]
        "
        :itemSelectEvent="serviceSelect"
      />

    </v-card>

  </v-dialog>

</template>

<script>
import KUGTable from "@/components/tables/KUGTable.vue";
import PaginationTable from "@/components/tables/pagination_table/PaginationTable.vue";
import DialogContentWithError from "@/components/dialogs/DialogContentWithError.vue";
import {apiRequest} from "@/commons/api_request";
import {showAlert} from "@/commons/alerts";

// Диалоговое окно для добавления новой учебной группы
export default {
  name: "StudentGroupCreateDialog",
  components: {DialogContentWithError, PaginationTable, KUGTable},
  props: {
    getRecsFunction: Function // Функция получения записей из пагинационной таблицы
  },
  data() {
    return {
      dialog: false, // Параметр отображения диалогового окна создания учебной группы
      serviceChooseDialog: false, // Параметр отображения диалогового окна выбора услугиб
      loading: false, // Параметр отображения загрузки на элементах формы
      serviceTypes: [
        {
          key: 'ou',
          title: 'ОУ (Курс)'
        },
        {
          key: 'iku',
          title: 'ИКУ (Мероприятие)'
        }
      ], // Типы услуг,
      serviceType: 'ou',
      newGroup: {
        type: 'ou',
        service_id: null,
        plan_seats_number: 0
      }, // Объект с информацией о новой учебной группы
      getRecsURL: '/backend/api/v1/edu/education_service/', // URL эндопинта для получения услуг
      selectedServiceName: '', // Название выбранной услуги
      servicesTableHeaders: [
        {
          'title': 'Место проведения',
          'key': 'location'
        },
        {
          'title': 'Дата начала обучения',
          'key': 'date_start'
        },
        {
          'title': 'Дата окончания обучения',
          'key': 'date_end'
        },
      ], // Заголовки столбцов пагинационной таблицы для выбора услуги
      servicesFieldsArray: [
        {
          ui: 'input',
          type: 'text',
          key: 'location',
          addRequired: true,
        },
        {
          ui: 'date',
          key: 'date_start',
          addRequired: true,
        },
        {
          ui: 'date',
          key: 'date_end',
          addRequired: true,
        },
      ], // Описание столбцов пагинационной таблицы для выбора услуги
    }
  },
  methods: {
    // Установка значений выбранной услуги в объект создаваемой группы и в текст для вывода на форму
    serviceSelect(service) {
      if (this.newGroup.type === 'ou') {
        this.selectedServiceName = service.program
      } else {
        this.selectedServiceName = service.name
      }
      this.selectedServiceName += ' (' + service.date_start + '-' + service.date_end+')'
      this.newGroup.service_id = service.object_id
      this.serviceChooseDialog = false
    },
    // Добавление новой учебной группы
    async saveStudentGroup() {
      this.$refs["content-error"].hideContentError()
      if (this.newGroup.service_id === null) {
        this.$refs["content-error"].showContentError('Выберите услугу')
        return false
      }
      if ((this.newGroup.type === 'iku') && (this.newGroup.plan_seats_number === 0)) {
        this.$refs["content-error"].showContentError('Плановое количество мест для ИКУ не может быть равно нулю')
        return false
      }
      this.loading = true
      let addRequest = await apiRequest(
        '/backend/api/v1/edu/student_group/',
        'POST',
        true,
        this.newGroup
      )
      if (addRequest.error) {
        this.$refs["content-error"].showContentError(addRequest.error)
      } else {
        showAlert(
          'success',
          'Учебная группа',
          addRequest.success
        )
        this.dialog = false
        this.getRecsFunction()
      }
      this.loading = false
    }
  },
  watch: {
    // Изменение URL эндпоинта для получения списка услуг при изменении объекта учебной группы
    serviceType: function () {
      this.selectedServiceName = ''
      this.newGroup.service_id = null
      this.newGroup.type = this.serviceType
      if (this.serviceType === 'ou') {
        this.getRecsURL = '/backend/api/v1/edu/education_service/'
      } else {
        this.getRecsURL = '/backend/api/v1/edu/information_service/'
      }
      console.log(this.newGroup)
    }
  }
}
</script>

<style scoped>

</style>
