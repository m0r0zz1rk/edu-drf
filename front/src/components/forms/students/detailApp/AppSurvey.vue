<template>

  <div v-if="surveyAnswers === null"><b>Пожалуйста, подождите...</b></div>

  <div v-else>
    <template v-for="question in surveyQuestions">

      <v-textarea
        :label="question.text"
        v-if="question.type === 'short'"
        v-model="surveyAnswers.filter(ans => ans.question_id === question.object_id)[0].value"
        color="coko-blue"
        :loading="loading"
      />

      <v-select
        :label="question.text"
        v-if="['one', 'many'].includes(question.type)"
        :multiple="question.type === 'many'"
        v-model="surveyAnswers.filter(ans => ans.question_id === question.object_id)[0].value"
        bg-color="white"
        variant="solo"
        :items="question.options"
        :loading="loading"
      />

      <hr/>
    </template>
  </div>

</template>

<script>
import {apiRequest} from "@/commons/apiRequest";

export default {
  name: "AppSurvey",
  props: {
    // object_id заявки
    appId: String
  },
  data() {
    return {
      // Список полученных вопросов
      surveyQuestions: null,
      // Список ответов на вопросы
      surveyAnswers: null,
      // Индикатор блокировки элементов формы
      loading: false
    }
  },
  methods: {
    // Получить список вопросов опроса для заявки
    async getSurveyQuestions() {
      this.surveyQuestions = await apiRequest(
        `/backend/api/v1/users/application/survey_questions/${this.appId}/`,
        'GET',
        true,
        null
      )
      let answers = []
      this.surveyQuestions.forEach((quest) => {answers.push({'question_id': quest.object_id, 'value': null})})
      this.surveyAnswers = answers
    },
  },
  mounted() {
    this.getSurveyQuestions()
  }
}
</script>



<style scoped>

</style>
