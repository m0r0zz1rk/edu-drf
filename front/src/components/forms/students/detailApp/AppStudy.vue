<template>
  <div v-if="studyData === null"><b>Пожалуйста, подождите...</b></div>

  <div v-else>

    <div v-if="studyData.study_url !== null && studyData.study_url.length > 0">
      <v-btn
        color="coko-blue"
        text="Перейти"
        @click="openStudyURL()"
      />
    </div>

    <div v-else>
      <b>Ссылка на обучение не назначена в учебной группе. Обратитесь к администратору</b>
    </div>

  </div>

</template>

<script>
import {apiRequest} from "@/commons/apiRequest";
import {convertDateToBackend} from "@/commons/date";

export default {
  // Компонент для перехода по ссылке на обучение
  name: "AppStudy",
  props: {
    // Тип услуги (course, event)
    serviceType: String,
    // Объект заявки
    app: Object,
  },
  data() {
    return {
      // Данные по обучение
      studyData: null
    }
  },
  methods: {
    // Получить ссылку на обучение
    async getStudyURL() {
      this.studyData = await apiRequest(
        `/backend/api/v1/applications/${this.serviceType}_application_user/study_url/${this.app.object_id}/`,
        'GET',
        true,
        null
      )
    },
    // Изменить статус заявки на "Проходит обучение" если текущий статус "Оплачено"
    updateAppStatus() {
      apiRequest(
        `/backend/api/v1/applications/${this.serviceType}_application_user/${this.app.object_id}/`,
        'PATCH',
        true,
        {...this.app, status: 'study'}
      )
    },
    // Открыть ссылку на обучение в новой вкладке
    openStudyURL() {
      if (this.app.status === 'pay') {this.updateAppStatus()}
      window.open(this.studyData.study_url, '_blank')
    }
  },
  mounted() {
    this.getStudyURL()
  }
}
</script>

<style scoped>

</style>
