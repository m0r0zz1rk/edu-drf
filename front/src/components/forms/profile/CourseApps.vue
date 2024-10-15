<template>

  <PaginationTable
      tableTitle="Заявки на курсы"
      tableWidth="98"
      :noTab="false"
      :addButton="false"
      :xlsxButton="false"
      :getRecsURL="'/backend/api/v1/users/course_application/?profile_id='+profileUuid"
      :tableHeaders="tableHeaders"
      :fieldsArray="fieldsArray"
      :selectGroupAppFunction="getAppInfo"
  />

  <CokoDialog
      ref="appFormDialog"
      :cardActions="true"
  >

    <template v-slot:title>
      <p v-if="!mobileDisplay">Анкета в группу {{formGroup}}</p>
      <p v-if="mobileDisplay">{{formGroup}}</p>
    </template>

    <template v-slot:text>
      <v-skeleton-loader
          v-if="selectedApp === null"
          height="100%"
          type="paragraph"
      />

      <AppForm
          v-if="selectedApp !== null"
          ref="appForm"
          :disabled="false"
          :studentApp="selectedApp"
          :mos="formData.mo"
          :positionCategories="formData.position_category"
          :positions="formData.position"
          :regions="formData.region"
          :changeAppAttribute="changeAppField"
      />
    </template>

    <template v-slot:actions>
      <v-btn
          color="coko-blue"
          text="Сохранить"
          @click="saveApp()"
      />
    </template>

  </CokoDialog>

</template>

<script>

// Компонент для работы с заявками обучающегося на курсы
import PaginationTable from "@/components/tables/pagination_table/PaginationTable.vue";
import {apiRequest} from "@/commons/api_request";
import {showAlert} from "@/commons/alerts";
import CokoDialog from "@/components/dialogs/CokoDialog.vue";
import AppForm from "@/components/forms/students/detailApp/AppForm.vue";
import {useDisplay} from "vuetify";

export default {
  name: 'CourseApps',
  components: {AppForm, CokoDialog, PaginationTable},
  props: {
    // object_id профиля обучающегося
    profileUuid: String,
  },
  data() {
    return {
      // Параметр проверки мобильного устройства
      mobileDisplay: useDisplay().smAndDown,
      // Список столбцов таблицы
      tableHeaders: [
        {
          'title': 'Дата подачи',
          'key': 'date_create'
        },
        {
          'title': 'Группа',
          'key': 'group_code'
        },
        {
          'title': 'Статус',
          'key': 'status'
        },
        {
          'title': 'Анкета',
          'key': 'form'
        }
      ],
      // Список описаний столбцов таблицы
      fieldsArray: [
        {
          ui: 'date',
          key: 'date_create',
          addRequired: false,
        },
        {
          ui: 'input',
          type: 'text',
          key: 'group_code',
          addRequired: false,
        },
        {
          ui: 'appStatus',
          key: 'status',
          addRequired: false
        },
        {
          ui: 'appFormView',
          key: 'form',
          addRequired: false
        }
      ],
      // Массив данных для работы с анкетами заявок
      formData: null,
      // Выбранная заявка
      selectedApp: null,
      // Шифр группы
      formGroup: ''
    }
  },
  methods: {
    // Получение массива данных для работы с анкетой
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
      }
    },
    // Получение информации по заявке
    async getAppInfo(group_code, app_id) {
      this.selectedApp = null
      this.formGroup = group_code
      this.$refs.appFormDialog.dialog = true
      let st = 'course'
      if (this.serviceType !== 'ou') {
        st = 'events'
      }
      let url = '/backend/api/v1/users/course_application/'+app_id+'/'
      let appInfoRequest = await apiRequest(
          url,
          'GET',
          true,
          null
      )
      if (appInfoRequest.error) {
        showAlert(
            'error',
            'Получение информации по заявке',
            appInfoRequest.error
        )
      } else {
        this.selectedApp = appInfoRequest
      }
    },
    // Изменение поля анкеты заявки
    changeAppField(field, value) {

    },
    // Сохранить изменения в заявке
    saveApp() {

    }
  },
  mounted() {
    this.getFormData()
  }
}

</script>

<style scoped>

</style>