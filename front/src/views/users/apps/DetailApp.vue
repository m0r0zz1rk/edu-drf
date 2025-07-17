<template>

  <LkPage :usePreLoader="usePreLoader">
    <slot>

      <v-card
          color="coko-blue"
          class="lk-full-page-card"
          :title="`Заявка ${this.app ? this.app.group_code : ''}`"
      >

        <v-card-text class="adaptive-tab-table-card-text" style="padding: 0;">
          <template v-if="app === null">
            <b>Загружаем информацию о заявке...</b>
          </template>

          <template v-if="app !== null">

            <v-tabs style="width: 100%; top: 0; z-index: 10; position: sticky" v-model="appTab" bg-color="coko-blue" show-arrows>

              <v-tab class="coko-tab" value="info">Информация</v-tab>
              <v-tab class="coko-tab" value="form">Анкета</v-tab>
              <v-tab v-if="(app.status === 'wait_pay') && (app.physical)" class="coko-tab" value="payment">Оплата</v-tab>
              <v-tab v-if="!(app.check_survey) && serviceLastDay" class="coko-tab" value="survey">Опрос</v-tab>
              <v-tab v-if="(app.status === 'Архив') && (app.certificate_doc_id)" class="coko-tab" value="schedule">Сертификат</v-tab>

            </v-tabs>

            <div
              style="padding-left: 5px; padding-top: 5px"
            >

              <AppInfo v-if="appTab === 'info'" :app="app"/>

              <template v-if="appTab === 'form'">

                <div v-if="formData === null">
                  <b>Подождите, получаем данные для заполнения анкеты...</b>
                </div>

                <div v-if="(formData !== null) && (app !== null)">
                  <AppForm
                    ref="appForm"
                    :studentApp="app"
                    :appType="appType"
                    :mos="formData.mo"
                    :positionCategories="formData.position_category"
                    :positions="formData.position"
                    :regions="formData.region"
                    :changeAppAttribute="changeAppField"
                  />
                </div>

              </template>

            </div>

          </template>

        </v-card-text>

        <v-divider></v-divider>

        <v-card-actions
          v-if="app !== null"
          style="background-color: white"
        >

          <v-spacer></v-spacer>

          <v-btn
              v-if="app.status === 'draft'"
              color="coko-blue"
              text="Сохранить"
              :loading="loading"
              @click="saveApp()"
          ></v-btn>

          <v-btn
              v-if="app.status === 'draft'"
              color="coko-blue"
              text="В работу"
              :loading="loading"
              @click="saveApp(true)"
          ></v-btn>

        </v-card-actions>

      </v-card>

    </slot>
  </LkPage>

</template>

<script>

// Форма для управления заявкой обучающегося
import LkPage from "@/components/LkPage.vue";
import {apiRequest} from "@/commons/apiRequest";
import {showAlert} from "@/commons/alerts";
import {convertBackendDate, convertDateToBackend} from "@/commons/date";
import AppInfo from "@/components/forms/students/detailApp/AppInfo.vue";
import AppForm from "@/components/forms/students/detailApp/AppForm.vue";

export default {
  name: 'DetailApp',
  components: {AppForm, AppInfo, LkPage},
  props: {
    // Функция для работы с анимацией загрузки
    usePreLoader: Function,
  },
  data() {
    return {
      // Объект заявки
      app: null,
      // Данные для заполнения анкеты
      formData: null,
      // Выбранная вкладка
      appTab: 'info',
      // Параметр проверки на крайний день проведения услуги
      serviceLastDay: false,
      // Параметр оторбажения анимации загрузки на элементах формы
      loading: false,
      // Тип услуги в заявке
      appType: this.$route.params.serviceType === 'course' ? 'ou' : 'iku'
    }
  },
  methods: {
    // Проверка на крайний день проведения услуги
    checkServiceLastDay() {
      let dates = this.app.service_date_range.split(' - ')
      this.serviceLastDay = convertBackendDate(dates[1]) <= new Date()
    },
    // Проверка на черновик заявки (если статус заявки "Черновик" - то открыть вкладку "Анкета")
    checkAppDraft(){
      if (this.app.status === 'draft') {
        this.appTab = 'form'
      }
    },
    // Получение массива данных для заполнения анкеты заявки
    async getFormData() {
      let formDataRequest = await apiRequest(
          '/backend/api/v1/users/form_data/',
          'GET',
          true,
          null
      )
      if (formDataRequest.error) {
        showAlert(
            'error',
            'Получение данных',
            formDataRequest.error
        )
      } else {
        this.formData = formDataRequest.success
        this.getAppInfo()
      }
    },
    // Получение информации по заявке
    async getAppInfo() {
      let url = '/backend/api/v1/users/'+this.$route.params.serviceType+'_application/'+this.$route.params.appId+'/'
      let appInfoRequest = await apiRequest(
          url,
          'GET',
          true,
          null
      )
      if (appInfoRequest.error) {
        this.$router.push('/')
        showAlert(
            'error',
            'Получение информации по заявке',
            appInfoRequest.error
        )
      } else {
        this.app = appInfoRequest
        this.checkServiceLastDay()
        this.checkAppDraft()
      }
    },
    // Изменение поля заявки
    changeAppField(field, value) {
      this.app[field] = value
    },
    // Сохранение изменений в заявке
    async saveApp(inWork = false) {
      if (confirm('Вы уверены, что хотите сохранить информацию?')) {
        if (this.app.education_date !== null && this.app.education_date instanceof Date) {
          this.app.education_date = convertDateToBackend(this.app.education_date)
        }
        this.app.in_work = inWork
        this.$refs.appForm.loading = true
        const saveAppRequest = await apiRequest(
          `/backend/api/v1/applications/${this.$route.params.serviceType}_application_user/${this.app.object_id}/`,
          'PATCH',
          true,
          this.app
        )
        if (saveAppRequest.error) {
          showAlert('error', 'Сохранение заявки', saveAppRequest.error)
        } else {
          showAlert('success', 'Сохранение заявки', saveAppRequest.success)
        }
        if (inWork) {
          this.usePreLoader()
          await this.getAppInfo()
          this.usePreLoader(true)
        }
        this.$refs.appForm.loading = false
      }
    },
  },
  mounted() {
    this.getFormData()
  }
}
</script>

<style scoped>

</style>
