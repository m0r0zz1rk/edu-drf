<template>

  <PaginationTable
      tableTitle="Заявки обучающихся"
      tableWidth="98"
      :noTab="false"
      :addButton="false"
      :xlsxButton="false"
      :getRecsURL="
        serviceType === 'ou' ?
          '/backend/api/v1/applications/course_application_admin?group_id='+groupId
          :
          ''
      "
      :tableHeaders="tableHeaders"
      :fieldsArray="fieldsArray"
      :openDocViewerFunction="openDocViewer"
      :selectGroupAppFunction="getAppInfo"
  />

  <CokoDialog
    ref="appFormDialog"
    :cardActions="true"
  >

    <template v-slot:title>
      <p v-if="!mobileDisplay">Анкета обучающегося {{formFIO}}</p>
      <p v-if="mobileDisplay">{{formFIO.split(' ')[0]}}</p>
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

  <CokoDialog
    ref="docViewerDialog"
  >

    <template v-slot:title>
      <p v-if="!mobileDisplay">{{docName}} обучающегося {{docFIO}}</p>
      <p v-if="mobileDisplay">{{docFIO.split(' ')[0]}}</p>
    </template>

    <template v-slot:text>
      <DocViewer
        :fileId="docId"
        :fileType="docType"
      />
    </template>

  </CokoDialog>

</template>

<script>

// Компонент для работы с заявками учебной группы
import PaginationTable from "@/components/tables/pagination_table/PaginationTable.vue";
import appStatuses from "@/commons/consts/apps/appStatuses";
import CokoDialog from "@/components/dialogs/CokoDialog.vue";
import DocViewer from "@/components/DocViewer.vue";
import {useDisplay} from "vuetify";
import {apiRequest} from "@/commons/api_request";
import {showAlert} from "@/commons/alerts";
import AppForm from "@/components/forms/students/detailApp/AppForm.vue";

export default {
  name: 'StudentGroupApps',
  components: {AppForm, DocViewer, CokoDialog, PaginationTable},
  props: {
    groupId: String, // object_id учбеной группы
    serviceType: String, // Тип услуги учебной группы (ou или iku)
  },
  data() {
    return {
      // Массив данных для анкеты
      formData: null,
      // Параметр проверки мобильного устройства
      mobileDisplay: useDisplay().smAndDown,
      // Список столбцов таблицы
      tableHeaders: [
        {
          'title': 'Обучающийся',
          'key': 'student'
        },
        {
          'title': 'Дата подачи',
          'key': 'date_create'
        },
        {
          'title': 'Статус',
          'key': 'status'
        },
        {
          'title': 'Анкета',
          'key': 'form'
        },
        {
          'title': 'ОО',
          'key': 'oo'
        },
        {
          'title': 'Образование',
          'key': 'education_check'
        },
        {
          'title': 'Оплата',
          'key': 'pay_doc'
        },
        {
          'title': 'Опрос',
          'key': 'check_survey'
        }
      ],
      // Список описаний столбцов таблицы
      fieldsArray: [
        {
          ui: 'appStudentInfo',
          key: 'student',
          addRequired: false,
        },
        {
          ui: 'date',
          key: 'date_create',
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
        },
        {
          ui: 'appOoCheck',
          key: 'oo',
          addRequired: false
        },
        {
          ui: 'appEducationCheck',
          key: 'education_check',
          addRequired: false,
        },
        {
          ui: 'appPayCheck',
          key: 'pay_doc',
          addRequired: false,
        },
        {
          ui: 'appSurveyCheck',
          key: 'check_survey',
          addRequired: false
        }
      ],
      // object_id выбранного документа,
      docId: '',
      // Выбранный тип документа
      docType: '',
      // Наименование документа,
      docName: '',
      // ФИО обучаюещегося - владельца документа
      docFIO: '',
      // ФИО анкеты обучающегося
      formFIO: '',
      // Выбранная анкета
      selectedApp: null
    }
  },
  methods: {
    // Открыть окно для просмотра документа
    openDocViewer(fio, docId, docName, docType) {
      this.docType = docType
      this.docName = docName
      this.docFIO = fio
      this.docId = docId
      this.$refs.docViewerDialog.dialog = true
    },
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
    async getAppInfo(display_name, app_id) {
      this.selectedApp = null
      this.formFIO = display_name
      this.$refs.appFormDialog.dialog = true
      let st = 'course'
      if (this.serviceType !== 'ou') {
        st = 'events'
      }
      let url = '/backend/api/v1/users/'+st+'_application/'+app_id+'/'
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
