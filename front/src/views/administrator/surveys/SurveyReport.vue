<template>

  <v-row
      style="padding-top: 15px; width: 98%; margin: 0 auto"
      dense
  >

    <v-col
        cols="12"
        md="12"
        sm="12"
    >

      <v-text-field
          label="Опрос"
          :loading="loading"
          v-model="reportInfo.survey_description"
          @click="dialogSelectSurvey = true"
          readonly
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
          v-model="reportInfo.type"
          :items="reportTypes"
          item-title="title"
          item-value="key"
          label="Тип отчета"
          :loading="loading"
      />

    </v-col>

    <v-col
        v-if="reportInfo.type !== 'group'"
        cols="12"
        md="12"
        sm="12"
    >

      <v-date-input
          bg-color="white"
          v-model="reportInfo.start_period"
          label="Начало периода"
          v-mask="'##.##.####'"
          prepend-icon=""
          prepend-inner-icon="$calendar"
          variant="solo"
          :loading="loading"
          clearable
      />

    </v-col>

    <v-col
        v-if="reportInfo.type !== 'group'"
        cols="12"
        md="12"
        sm="12"
    >

      <v-date-input
          bg-color="white"
          v-model="reportInfo.end_period"
          label="Окончание периода"
          v-mask="'##.##.####'"
          prepend-icon=""
          prepend-inner-icon="$calendar"
          variant="solo"
          :loading="loading"
          clearable
      ></v-date-input>

    </v-col>

    <v-col
        v-if="reportInfo.type === 'service_type'"
        cols="12"
        md="12"
        sm="12"
    >

      <v-select
          bg-color="white"
          variant="solo"
          v-model="reportInfo.service_type"
          :items="serviceTypes"
          item-title="title"
          item-value="key"
          label="Тип услуги"
          :loading="loading"
      />

    </v-col>

    <v-col
        v-if="reportInfo.type === 'group'"
        cols="12"
        md="12"
        sm="12"
    >

      <v-text-field
          label="Учебная группа"
          :loading="loading"
          v-model="reportInfo.group_code"
          @click="dialogSelectGroup = true"
          readonly
      />

    </v-col>

  </v-row>

  <div style="width: 100%; text-align: center">
    <v-btn
        color="coko-blue"
        :loading="loading"
        @click="createReport()"
        text="Сформировать"
    />
  </div>



  <v-dialog
      persistent
      v-model="dialogSelectSurvey"
  >

    <v-card class="lk-full-page-card">
      <v-card-title class="d-flex justify-space-between align-center">
        Выбор опроса

        <v-btn
            icon="mdi-close"
            color="coko-blue"
            @click="dialogSelectSurvey = !(dialogSelectSurvey)"
        />
      </v-card-title>

      <v-card-text>

        <PaginationTable
            tableTitle="Опросы"
            tableWidth="98"
            :noTab="false"
            :addButton="false"
            :xlsxButton="false"
            getRecsURL="/backend/api/v1/surveys/surveys/"
            addRecURL="/backend/api/v1/surveys/surveys/"
            :tableHeaders="surveyTableHeaders"
            :fieldsArray="surveyFieldsArray"
            :itemSelectEvent="selectSurvey"
        />

      </v-card-text>

    </v-card>

  </v-dialog>

  <v-dialog
      persistent
      v-model="dialogSelectGroup"
  >

    <v-card class="lk-full-page-card">
      <v-card-title class="d-flex justify-space-between align-center">
        Выбор учебной группы

        <v-btn
            icon="mdi-close"
            color="coko-blue"
            @click="dialogSelectGroup = !(dialogSelectGroup)"
        />
      </v-card-title>

      <v-card-text>

        <PaginationTable
            tableTitle="Учебные группы"
            tableWidth="98"
            :noTab="false"
            :addButton="false"
            :xlsxButton="false"
            getRecsURL="/backend/api/v1/edu/student_group/"
            :tableHeaders="groupTableHeaders"
            :fieldsArray="groupFieldsArray"
            :itemSelectEvent="selectGroup"
        />

      </v-card-text>

    </v-card>

  </v-dialog>

</template>

<script>

// Форма для выгрузки отчета по опросу
import DialogContentWithError from "@/components/dialogs/DialogContentWithError.vue";
import PaginationTable from "@/components/tables/pagination_table/PaginationTable.vue";
import surveyReportTypes from "@/commons/consts/survey/surveyReportTypes";
import serviceTypes from "@/commons/consts/edu/serviceTypes";
import studentGroupStatuses from "@/commons/consts/edu/studentGroupStatuses";
import {apiRequest} from "@/commons/apiRequest";
import {showAlert} from "@/commons/alerts";
import {convertDateToBackend} from "@/commons/date";

export default {
  name: 'SurveyReport',
  components: {PaginationTable, DialogContentWithError},
  data() {
    return {
      // Отображение анимации загрузки на элеметнах формы
      loading: false,
      // Типы отчета
      reportTypes: surveyReportTypes,
      // Типы услуг
      serviceTypes: serviceTypes,
      // Объект с информацией для запроса отчета
      reportInfo: {
        survey_id: null,
        survey_description: '(не выбран)',
        type: 'all',
        start_period: new Date(),
        end_period: new Date(),
        group_code: '(не выбрана)',
        group_id: null,
        service_type: 'edu'
      },
      // Отображение диалогового окна для выбора опроса
      dialogSelectSurvey: false,
      // Заголовки таблицы для выбора опроса
      surveyTableHeaders: [
        {
          'title': 'Создатель',
          'key': 'creator_fio'
        },
        {
          'title': 'Описание опроса',
          'key': 'description'
        },
        {
          'title': 'Количество вопросов',
          'key': 'question_count'
        }
      ],
      // Описание полей таблицы для выбора опроса
      surveyFieldsArray: [
        {
          ui: 'input',
          type: 'text',
          key: 'creator_fio',
          addRequired: false,
          readOnly: true
        },
        {
          ui: 'input',
          type: 'text',
          key: 'description',
          addRequired: true,
        },
        {
          ui: 'input',
          type: 'number',
          key: 'question_count',
          addRequired: false,
          readOnly: true
        }
      ],
      // Параметр отображения диалогового окна для выбора учебной группы
      dialogSelectGroup: false,
      // Заголовки таблицы для выбора учебной группы
      groupTableHeaders: [
        {
          'title': 'Шифр',
          'key': 'code'
        },
        {
          'title': 'Статус',
          'key': 'status'
        },
        {
          'title': 'Наименование услуги',
          'key': 'service_name'
        },
        {
          'title': 'Начало обучения',
          'key': 'date_start'
        },
        {
          'title': 'Окончание обучения',
          'key': 'date_end'
        },
        {
          'title': 'Куратор',
          'key': 'curator'
        }
      ],
      // Описание полей таблицы для выбора учебной группы
      groupFieldsArray: [],
    }
  },
  methods: {
    // Выбор опроса в таблице
    selectSurvey(survey) {
      this.reportInfo.survey_id = survey.object_id
      this.reportInfo.survey_description = survey.description
      this.dialogSelectSurvey = false
    },
    // Получение статусов учебных групп и формирование списка описания полей таблицы выбора группы
    getStatuses() {
      let statuses = []
      studentGroupStatuses.map((status) => {
        statuses.push(status.title)
      })
      this.groupFieldsArray = [
        {
          ui: 'input',
          type: 'text',
          key: 'code',
          addRequired: true,
        },
        {
          ui: 'studentGroupStatus',
          items: statuses,
          key: 'status',
          addRequired: false
        },
        {
          ui: 'input',
          type: 'text',
          key: 'service_name',
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
        {
          ui: 'input',
          type: 'text',
          key: 'curator',
          addRequired: true,
        }
      ]
    },
    // Выбор учебной группы
    selectGroup(group) {
      this.reportInfo.group_id = group.object_id
      this.reportInfo.group_code = group.code
      this.dialogSelectGroup = false
    },
    // Отправка запроса на формирование отчета
    async createReport() {
      this.loading = true
      try {
        let body = this.reportInfo
        try {
          body.start_period = convertDateToBackend(this.reportInfo.start_period)
          body.end_period = convertDateToBackend(this.reportInfo.end_period)
        } catch(e) {
          body.start_period = this.reportInfo.start_period
          body.end_period = this.reportInfo.end_period
        }
        delete body.group_code
        delete body.survey_description
        const reportRequest = await apiRequest(
          '/backend/api/v1/surveys/generate_report/',
          'POST',
          true,
          body
        )
        if (reportRequest.success) {
          showAlert('success', 'Отчет по опросу', reportRequest.success)
        } else {
          showAlert('error', 'Отчет по опросу', 'Произошла ошибка при формировании отчета по опросу')
        }
      } catch(e) {
        console.log('report error: ', e)
        showAlert('error', 'Отчет по опросу', 'Произошла ошибка при формировании отчета по опросу')
      }
      this.loading = false
    }
  },
  mounted() {
    this.getStatuses()
  }
}

</script>

<style scoped>

</style>
