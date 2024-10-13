<template>

  <v-dialog
      persistent
      v-model="dialog"
  >

    <v-card class="lk-full-page-card">
      <v-card-title class="d-flex justify-space-between align-center">
        <v-tabs
            v-model="surveyTab"
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
              value="questions"
          >
            Вопросы
          </v-tab>

        </v-tabs>

        <v-btn
            icon="mdi-close"
            color="coko-blue"
            @click="getRecs(); dialog = !(dialog)"
        />
      </v-card-title>

      <v-card-text>

        <DialogContentWithError ref="content-error">

          <slot>

            <template v-if="surveyTab === 'info'">

              <v-row
                dense
              >

                <v-col
                    cols="12"
                    md="12"
                    sm="12"
                >

                  <v-text-field
                      bg-color="white"
                      variant="solo"
                      label="Описание"
                      v-model="surveyDescription"
                      clearable
                      :loading="loading"
                  />

                </v-col>

              </v-row>

            </template>

            <template v-if="surveyTab === 'questions'">

              <PaginationTable
                  ref="surveyQuestionTable"
                  tableTitle="Вопросы опроса"
                  tableWidth="98"
                  :noTab="false"
                  :addButton="true"
                  :xlsxButton="false"
                  :getRecsURL="'/backend/api/v1/surveys/survey_questions/?survey_id='+surveyObjectID"
                  :defaultBody="{
                    'survey_id': surveyObjectID
                  }"
                  addRecURL="/backend/api/v1/surveys/survey_questions/"
                  :tableHeaders="tableHeaders"
                  :fieldsArray="fieldsArray"
                  :itemSelectEvent="selectSurveyQuestion"
              />

            </template>

          </slot>

        </DialogContentWithError>

      </v-card-text>

      <v-divider></v-divider>

      <v-card-actions
          style="background-color: white"
      >

        <v-spacer></v-spacer>

        <v-btn
            v-if="surveyTab === 'info'"
            color="coko-blue"
            text='Сохранить'
            :loading="loading"
            @click="saveSurvey()"
        ></v-btn>
      </v-card-actions>

    </v-card>

  </v-dialog>

  <SurveyQuestionDetail
    ref="surveyQuestionDetail"
    :getQuestions="getQuestions"
  />

</template>

<script>

// Компонент для просмотра информации об опросе
import DialogContentWithError from "@/components/dialogs/DialogContentWithError.vue";
import {apiRequest} from "@/commons/api_request";
import {showAlert} from "@/commons/alerts";
import surveyQuestionTypes from "@/commons/consts/survey/surveyQuestionTypes";
import PaginationTable from "@/components/tables/pagination_table/PaginationTable.vue";
import SurveyQuestionDetail from "@/components/forms/surveys/SurveyQuestionDetail.vue";

export default {
  name: 'SurveyDetail',
  components: {
    SurveyQuestionDetail,
    PaginationTable,
    DialogContentWithError
  },
  props: {
    // Функция обновления записей в пагинационной таблице
    getRecs: Function,
  },
  data() {
    return {
      // Параметр отображения диалогового окна
      dialog: false,
      // Выбранная вкладка в диалоговом окне
      surveyTab: 'info',
      // Информация о проблеме при работе с формой
      surveyFormError: null,
      // Параметр загрузочного состояния элементов формы
      loading: false,
      // Список столбцов для таблицы с вопросами опроса
      tableHeaders: [
        {
          'title': 'Порядковый номер',
          'key': 'sequence_number'
        },
        {
          'title': 'Формулировка вопроса',
          'key': 'text'
        },
        {
          'title': 'Тип вопроса',
          'key': 'question_type'
        }
      ],
      // Описания столбцов для таблицы с вопросами опроса
      fieldsArray: [],
      // Описание опроса
      surveyDescription: '',
      // object_id опроса
      surveyObjectID: '',
      // Простой список типов вопроса
      simpleQuestionTypes: []
    }
  },
  methods: {
    // Сохранение информации по опросу
    async saveSurvey() {
      this.$refs["content-error"].hideContentError()
      if (this.surveyDescription.length === 0) {
        this.$refs["content-error"].showContentError('Описание опроса не может быть пустым')
        return false
      }
      let surveyUpdateRequest = await apiRequest(
          '/backend/api/v1/surveys/' + this.surveyObjectID + '/',
          'PATCH',
          true,
          {'description': this.surveyDescription}
      )
      if (surveyUpdateRequest.error) {
        this.$refs["content-error"].showContentError(surveyUpdateRequest.error)
      }
      if (surveyUpdateRequest.success) {
        this.dialog = false
        showAlert(
            'success',
            'Опрос',
            surveyUpdateRequest.success
        )
        this.getRecs()
      }
      this.loading = false
    },
    // Получение списка вопросов в таблице
    getQuestions() {
      this.$refs.surveyQuestionTable.getRecs()
    },
    // Фомирование списка описаний столбцов таблицы вопросов
    createFieldsArray() {
      let types = []
      surveyQuestionTypes.map((type) => {
        types.push(type.title)
      })
      this.fieldsArray = [
        {
          ui: 'input',
          type: 'number',
          key: 'sequence_number',
          addRequired: true
        },
        {
          ui: 'input',
          type: 'text',
          key: 'text',
          addRequired: true,
        },
        {
          ui: 'select',
          items: types,
          key: 'question_type',
          addRequired: true,
        },
      ]
    },
    // Выбор вопроса из таблицы вопросов
    selectSurveyQuestion(question) {
      let questionObj = question
      questionObj.survey_id = this.surveyObjectID
      this.$refs.surveyQuestionDetail.question = questionObj
      this.$refs.surveyQuestionDetail.dialog = true
    }
  },
  mounted() {
    this.createFieldsArray()
  }
}

</script>

<style scoped>

</style>