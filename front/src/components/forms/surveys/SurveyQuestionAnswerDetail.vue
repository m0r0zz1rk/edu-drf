<template>

  <v-dialog
      v-if="answer !== null"
      persistent
      v-model="dialog"
  >

    <v-card class="lk-full-page-card">
      <v-card-title class="d-flex justify-space-between align-center">

        Информация по возможному ответу

        <v-btn
            icon="mdi-close"
            color="coko-blue"
            @click="dialog = !(dialog)"
        />
      </v-card-title>

      <v-card-text>

        <DialogContentWithError
            ref="questionContentError"
        >

          <slot>

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
                      label="Ответ"
                      v-model="answer.text"
                      clearable
                      :loading="loading"
                  />
                </v-col>

              </v-row>

          </slot>

        </DialogContentWithError>

      </v-card-text>

      <v-card-actions
          style="background-color: white"
      >

        <v-spacer></v-spacer>

        <v-btn
            color="coko-blue"
            text='Удалить'
            :loading="loading"
            @click="deleteAnswer()"
        ></v-btn>

        <v-btn
            color="coko-blue"
            text='Сохранить'
            :loading="loading"
            @click="saveAnswer()"
        ></v-btn>
      </v-card-actions>

    </v-card>

  </v-dialog>

</template>

<script>

import DialogContentWithError from "@/components/dialogs/DialogContentWithError.vue";
import {apiRequest} from "@/commons/apiRequest";
import {showAlert} from "@/commons/alerts";

export default {
  name: 'SurveyQuestionAnswerDetail',
  components: {DialogContentWithError},
  props: {
    // Функция получения списка возможных ответов в таблице родительского компонента
    getAnswers: Function,
    // object_id вопроса опроса
    questionObjectID: String,
  },
  data() {
    return {
      // Объект возможного ответа
      answer: null,
      // Параметр отображения анимации загрузки на элементах формы
      loading: false,
      // Параметр отображения диалогового окна
      dialog: false
    }
  },
  methods: {
    // Сохранение информации о возможном ответе
    async saveAnswer() {
      if (this.answer.text.length === 0) {
        alert('Задайте возможный ответ')
        return false
      }
      this.loading = true
      let body = this.answer
      delete body['object_id']
      body['survey_question_id'] = this.questionObjectID
      let saveQuestionAnswerResponse = await apiRequest(
          '/backend/api/v1/surveys/survey_question_answer/'+this.answer.object_id+'/',
          'PATCH',
          true,
          body
      )
      if (saveQuestionAnswerResponse.error) {
        alert('Произошла ошибка: ' + saveQuestionAnswerResponse.error)
      } else {
        showAlert(
            'success',
            'Возможный ответ вопроса',
            saveQuestionAnswerResponse.success
        )
        this.getAnswers()
        this.dialog = false
      }
      this.loading = false
    },
    // Удаление возможного ответа
    async deleteAnswer() {
      if (confirm('Вы уверены, что хотите удалить возможный ответ?')) {
        this.loading = true
        let deleteQuestionAnswerResponse = await apiRequest(
            '/backend/api/v1/surveys/survey_question_answer/'+this.answer.object_id+'/',
            'DELETE',
            true,
            null
        )
        if (deleteQuestionAnswerResponse.error) {
          alert(deleteQuestionAnswerResponse.error)
        } else {
          showAlert(
              'success',
              'Возможный ответ вопроса',
              deleteQuestionAnswerResponse.success
          )
          this.getAnswers()
          this.dialog = false
        }
        this.loading = false
      }
    }
  }
}

</script>

<style scoped>

</style>
