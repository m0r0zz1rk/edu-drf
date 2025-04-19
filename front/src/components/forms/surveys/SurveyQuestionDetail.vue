<template>

  <v-dialog
      persistent
      v-model="dialog"
  >

    <v-card class="lk-full-page-card">
      <v-card-title class="d-flex justify-space-between align-center">
        <v-tabs
            v-model="questionTab"
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
              v-if="question.question_type !== 'Короткий ответ'"
              class="coko-tab"
              value="answers"
          >
            Возможные ответы
          </v-tab>

        </v-tabs>

        <v-btn
            icon="mdi-close"
            color="coko-blue"
            @click="getQuestions(); dialog = !(dialog)"
        />
      </v-card-title>

      <v-card-text>

        <DialogContentWithError
            ref="questionContentError"
        >

          <slot>

            <template v-if="questionTab === 'info'">

              <v-row
                  dense
              >

                <v-col
                    cols="12"
                    md="12"
                    sm="12"
                >

                  <v-number-input
                      bg-color="white"
                      variant="solo"
                      min="0"
                      label="Порядковый номер"
                      v-model="question.sequence_number"
                      clearable
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
                      label="Формулировка вопроса"
                      v-model="question.text"
                      clearable
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
                      v-model="question.question_type"
                      :items="questionTypes"
                      item-title="title"
                      item-value="key"
                      label="Тип вопроса"
                      :loading="loading"
                  />

                </v-col>

              </v-row>

            </template>

            <template v-if="questionTab === 'answers'">

              <PaginationTable
                  ref="questionAnswersTable"
                  tableTitle="Возможные ответы"
                  tableWidth="98"
                  :noTab="false"
                  :addButton="true"
                  :xlsxButton="false"
                  :getRecsURL="'/backend/api/v1/surveys/survey_question_answer/?survey_question_id='+question.object_id"
                  :defaultBody="{
                    'survey_question_id': question.object_id
                  }"
                  addRecURL="/backend/api/v1/surveys/survey_question_answer/"
                  editRecURL="/backend/api/v1/surveys/survey_question_answer/"
                  :tableHeaders="tableHeaders"
                  :fieldsArray="fieldsArray"
                  :itemSelectEvent="selectQuestionAnswer"
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
            color="coko-blue"
            text='Удалить'
            :loading="loading"
            @click="deleteQuestion()"
        ></v-btn>

        <v-btn
            color="coko-blue"
            text='Сохранить'
            :loading="loading"
            @click="saveQuestion()"
        ></v-btn>
      </v-card-actions>

    </v-card>

  </v-dialog>

  <SurveyQuestionAnswerDetail
      v-if="question !== null"
      ref="surveyQuestionAnswerDetail"
      :questionObjectID="question.object_id"
      :getAnswers="getAnswers"
  />


</template>

<script>

import PaginationTable from "@/components/tables/pagination_table/PaginationTable.vue";
import DialogContentWithError from "@/components/dialogs/DialogContentWithError.vue";
import surveyQuestionTypes from "@/commons/consts/survey/surveyQuestionTypes";
import {apiRequest} from "@/commons/apiRequest";
import {showAlert} from "@/commons/alerts";
import SurveyQuestionAnswerDetail from "@/components/forms/surveys/SurveyQuestionAnswerDetail.vue";

export default {
  name: 'SurveyQuestionDetail',
  components: {SurveyQuestionAnswerDetail, DialogContentWithError, PaginationTable},
  props: {
    // Функция получения списка вопросов в таблице родительского компонента
    getQuestions: Function,
  },
  data() {
    return {
      // Параметр отображения диалогового окна
      dialog: false,
      // Параметр отображения анимации загрузки на элементах формы
      loading: false,
      // Объект вопроса
      question: null,
      // Выбранная вкладка диалогового окна
      questionTab: 'info',
      // Список типов вопросов
      questionTypes: surveyQuestionTypes,
      // Список столбцов для таблицы с возможными ответами вопроса
      tableHeaders: [
        {
          'title': 'Ответ',
          'key': 'text'
        }
      ],
      // Описания столбцов для таблицы с вопросами опроса
      fieldsArray: [
          {
            ui: 'input',
            type: 'text',
            key: 'text',
            addRequired: true,
          }
      ],
    }
  },
  methods: {
    async saveQuestion() {
      if ([undefined, null, ''].includes(this.question.sequence_number)) {
        alert('Заполните порядковый номер вопроса')
        return false
      }
      if (this.question.text.length === 0) {
        alert('Заполните формулировку вопроса')
        return false
      }
      this.loading = true
      let saveQuestionResponse = await apiRequest(
          '/backend/api/v1/surveys/survey_questions/'+this.question.object_id+'/',
          'PATCH',
          true,
          this.question
      )
      if (saveQuestionResponse.error) {
        alert('Произошла ошибка: ' + saveQuestionResponse.error)
      } else {
        showAlert(
            'success',
            'Вопрос опроса',
            saveQuestionResponse.success
        )
        this.getQuestions()
        this.dialog = false
      }
      this.loading = false
    },
    async deleteQuestion() {
      if (confirm('Вы уверены, что хотите удалить вопрос?')) {
        this.loading = true
        let deleteQuestionResponse = await apiRequest(
            '/backend/api/v1/surveys/survey_questions/'+this.question.object_id+'/',
            'DELETE',
            true,
            {
              survey_id: this.question.survey_id
            }
        )
        if (deleteQuestionResponse.error) {
          alert(deleteQuestionResponse.error)
        } else {
          showAlert(
              'success',
              'Вопрос опроса',
              deleteQuestionResponse.success
          )
          this.getQuestions()
          this.dialog = false
        }
        this.loading = false
      }
    },
    selectQuestionAnswer(answer) {
      this.$refs.surveyQuestionAnswerDetail.answer = answer
      this.$refs.surveyQuestionAnswerDetail.dialog = true
    },
    getAnswers() {
      this.$refs.questionAnswersTable.getRecs()
    }
  }
}

</script>

<style scoped>

</style>
