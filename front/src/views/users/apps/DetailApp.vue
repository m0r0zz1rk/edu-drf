<template>

  <LkPage :usePreLoader="usePreLoader">
    <slot>

      <v-card
          color="coko-blue"
          class="lk-full-page-card"
          :title="`Заявка ${this.app ? this.app.group_code : ''}`"
      >

        <v-card-text class="adaptive-tab-table-card-text" style="padding: 0;">
          <template v-if="app === null"><b>Загружаем информацию о заявке...</b></template>

          <template v-if="app !== null">

            <v-tabs style="width: 100%; top: 0; z-index: 10; position: sticky" v-model="appTab" bg-color="coko-blue" show-arrows>
              <v-tab
                class="coko-tab"
                value="info"
                text="Информация"
              />
              <v-tab
                class="coko-tab"
                value="form"
                text="Анкета"
              />
              <v-tab
                v-if="!(['draft', 'work'].includes(app.status)) && app.physical"
                class="coko-tab"
                value="payment"
                text="Оплата"
              />
              <v-tab
                v-if="['pay', 'study'].includes(app.status) && app.physical"
                class="coko-tab"
                value="study"
                text="Обучение"
              />
              <v-tab
                v-if="!(app.check_survey) && serviceLastDay"
                class="coko-tab"
                value="survey"
                text="Опрос"
              />
              <v-tab
                v-if="(app.status === 'archive') && (app.certificate_doc_id)"
                class="coko-tab"
                value="certificate"
                text="Сертификат"
              />
            </v-tabs>

            <div style="padding-left: 5px; padding-top: 5px">

              <AppInfo v-if="appTab === 'info'" :app="app"/>

              <template v-if="appTab === 'form'">

                <div v-if="formData === null">
                  <b>Подождите, получаем данные для заполнения анкеты...</b>
                </div>

                <div v-if="(formData !== null) && (app !== null)">
                  <AppForm
                    ref="appForm"
                    :studentApp="app"
                    :disabled="!(editStatuses.includes(app.status))"
                    :appType="appType"
                    :mos="formData.mo"
                    :positionCategories="formData.position_category"
                    :positions="formData.position"
                    :regions="formData.region"
                    :changeAppAttribute="changeAppField"
                  />
                </div>

              </template>

              <AppPayment
                v-if="appTab === 'payment'"
                :app="this.app"
                :appType="this.$route.params.serviceType"
                :updateAppForm="updateAppForm"
              />

              <AppStudy
                v-if="appTab === 'study'"
                :serviceType="this.$route.params.serviceType"
                :app="this.app"
              />

              <AppSurvey
                ref="appSurvey"
                v-if="appTab === 'survey'"
                :appId="this.app.object_id"
              />

              <AppCertificate
                v-if="appTab === 'certificate'"
                :certificateId="app.certificate_doc_id"
              />

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
            variant="flat"
              v-if="appTab === 'form' && editStatuses.includes(app.status)"
              color="coko-blue"
              text="Сохранить"
              :loading="loading"
              @click="saveApp(app.status === 'draft')"
          />

          <v-btn
            variant="flat"
            v-if="appTab === 'survey'"
            color="coko-blue"
            text="Завершить"
            :loading="loading"
            @click="saveSurvey()"
          />

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
import AppPayment from "@/components/forms/students/detailApp/AppPayment.vue";
import AppStudy from "@/components/forms/students/detailApp/AppStudy.vue";
import AppSurvey from "@/components/forms/students/detailApp/AppSurvey.vue";
import AppCertificate from "@/components/forms/students/detailApp/AppCertificate.vue";

export default {
  name: 'DetailApp',
  components: {AppCertificate, AppSurvey, AppStudy, AppPayment, AppForm, AppInfo, LkPage},
  props: {
    // Функция для работы с анимацией загрузки
    usePreLoader: Function,
  },
  data() {
    return {
      // Фамилия обучающегося в профиле
      profileSurname: '',
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
      appType: this.$route.params.serviceType === 'course' ? 'ou' : 'iku',
      // Статусы, при которых доступно редактирование анкеты
      editStatuses: ['draft', 'work', 'wait_pay', 'check', 'pay']
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
    // Получение фамилии обучающегося из профиля
    async getProfileSurname() {
      const surnameRequest = await apiRequest(
        '/backend/api/v1/auth/get_profile/',
        'GET',
        true,
        null
      )
      this.profileSurname = surnameRequest.surname
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
    // Проверка заполнения полей
    checkFields() {
      if (!this.app.education_doc_id) {
        showAlert('error', 'Проверка заявки', 'Выберите диплом')
        return false
      }
      if (this.app.diploma_surname !== this.profileSurname) {
        if (!this.app.surname_doc_id) {
          showAlert('error', 'Проверка заявки', 'Выберите документ о смене фамилии')
          return false
        }
      }
      return true
    },
    // Сохранение изменений в заявке
    async saveApp(inWork = false) {
      const checkApp = this.checkFields()
      if (!checkApp) return
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
        if (inWork) { await this.updateAppForm() }
        this.$refs.appForm.loading = false
      }
    },
    // Обновить форму с заявкой
    async updateAppForm() {
      this.usePreLoader()
      this.appTab = 'info'
      await this.getAppInfo()
      this.usePreLoader(true)
    },
    // Отправить данные по опросу
    async saveSurvey() {
      const appSurvey = this.$refs.appSurvey
      if (confirm('Вы уверены, что хотите завершить опрос?')) {
        if (appSurvey.surveyAnswers.filter((ans) => ans.value === null).length > 0) {
          showAlert('error', 'Опрос', 'Ответьте на все вопросы')
          return
        }
        appSurvey.loading = true
        // Преобразование массивов к вопросам с несколькими вариантами ответов в строку
        const manyIds = [...appSurvey.surveyQuestions.filter((quest) => quest.type === 'many').map((quest) => quest.object_id)]
        appSurvey.surveyAnswers.filter((ans) => manyIds.includes(ans.question_id)).map((ans) => {
          if ((ans.value !== null) && Array.isArray(ans.value)) {ans.value = ans.value.toString()}
        })
        const saveAnswersRequest = await apiRequest(
          `/backend/api/v1/users/application/survey_answers/${this.app.object_id}/`,
          'POST',
          true,
          {data: appSurvey.surveyAnswers}
        )
        if (saveAnswersRequest.success) {
          showAlert('success', 'Опросы', 'Опрос успешно пройден')
          this.updateAppForm()
        } else {
          showAlert('error', 'Опросы', saveAnswersRequest.error)
        }
        appSurvey.loading = false
      }
    }
  },
  mounted() {
    this.getProfileSurname()
    this.getFormData()
  }
}
</script>

<style scoped>

</style>
