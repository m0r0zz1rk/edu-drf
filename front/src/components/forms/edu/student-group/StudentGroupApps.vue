<template>

  <PaginationTable
    tableTitle="Заявки обучающихся"
    ref="mainAppsTable"
    tableWidth="98"
    :noTab="false"
    :addButton="false"
    :xlsxButton="false"
    :getRecsURL="
        serviceType === 'ou' ?
          '/backend/api/v1/applications/course_application_admin?group_id='+groupId
          :
          '/backend/api/v1/applications/event_application_admin?group_id='+groupId
      "
    :tableHeaders="tableHeaders"
    :fieldsArray="fieldsArray"
    :openDocViewerFunction="openDocViewer"
    :selectGroupAppFunction="getAppInfo"
    :appMoveFunction="prependForAppMove"
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
        :appType="serviceType"
        :mos="formData.mo"
        :positionCategories="formData.position_category"
        :positions="formData.position"
        :regions="formData.region"
        :changeAppAttribute="changeAppField"
      />
    </template>

    <template v-slot:actions>
      <v-btn
        :loading="loading"
        color="coko-blue"
        text="Сохранить"
        @click="saveApp()"
      />
    </template>

  </CokoDialog>

  <CokoDialog
    ref="appMoveDialog"
    :cardActions="true"
  >

    <template v-slot:title>
      Выбор группы для переноса заявки "{{appForMove.student.display_name}}"
    </template>

    <template v-slot:text>

      <template v-if="groupForMove">
        <b>Выбранная группа для переноса: {{groupForMove.code}}</b>
      </template>

      <PaginationTable
        tableTitle="Учебные группы"
        tableWidth="98"
        :noTab="false"
        :addButton="false"
        :xlsxButton="false"
        getRecsURL="/backend/api/v1/edu/student_group/"
        :tableHeaders="groupTableHeaders"
        :fieldsArray="groupFieldsArray"
        :itemSelectEvent="setMoveAppGroup"
      />

    </template>

    <template v-slot:actions>
      <v-btn
        :disabled="groupForMove === null"
        :loading="loading"
        color="coko-blue"
        text="Переместить"
        @click="appMove()"
      />
    </template>

  </CokoDialog>

</template>

<script>

// Компонент для работы с заявками учебной группы
import PaginationTable from "@/components/tables/pagination_table/PaginationTable.vue";
import CokoDialog from "@/components/dialogs/CokoDialog.vue";
import DocViewer from "@/components/DocViewer.vue";
import {useDisplay} from "vuetify";
import {apiRequest} from "@/commons/apiRequest";
import {showAlert} from "@/commons/alerts";
import AppForm from "@/components/forms/students/detailApp/AppForm.vue";
import {convertDateToBackend} from "@/commons/date";
import studentGroupStatuses from "@/commons/consts/edu/studentGroupStatuses";

export default {
  name: 'StudentGroupApps',
  components: {AppForm, DocViewer, CokoDialog, PaginationTable},
  props: {
    groupId: String, // object_id учбеной группы
    serviceType: String, // Тип услуги учебной группы (ou или iku)
    // Функция для открытия просмотрщика документа
    openDocViewer: Function
  },
  data() {
    return {
      // Блокировка формы
      loading: false,
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
          'title': 'Перенос заявки',
          'key': 'app_move'
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
          ui: 'appMove',
          key: 'app_move',
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
      selectedApp: null,
      // Выбранная заявка для переноса
      appForMove: null,
      // ФИО студента из заявки для переноса
      studentMove: '',
      // object_id выбранной группы для переноса
      groupForMove: null,
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
        },
        {
          'title': 'Количество заявок',
          'key': 'apps_count'
        }
      ],
      // Описание столбцов таблицы для выбора учебной группы
      groupFieldsArray: [
        {
          ui: 'input',
          type: 'text',
          key: 'code',
          addRequired: true,
        },
        {
          ui: 'studentGroupStatus',
          items: [...studentGroupStatuses.map((status) => { return status.title })],
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
        },
        {
          ui: 'input',
          type: 'number',
          key: 'apps_count',
          addRequired: true,
        }
      ],
    }
  },
  methods: {
    // Добавление столбца с документами об образовании если тип услуги - ОУ
    appendOoColumn() {
      if (this.serviceType === 'ou') {
        this.tableHeaders.push({
          'title': 'Образование',
          'key': 'education_check'
        })
        this.fieldsArray.push({
          ui: 'appEducationCheck',
          key: 'education_check',
          addRequired: false,
        })
      }
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
        st = 'event'
      }
      let url = '/backend/api/v1/applications/'+st+'_application_user/'+app_id+'/'
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
      this.selectedApp[field] = value
    },
    // Сохранить изменения в заявке
    async saveApp() {
      this.loading = true
      if (this.selectedApp.education_date !== null && this.selectedApp.education_date instanceof Date) {
        this.selectedApp.education_date = convertDateToBackend(this.selectedApp.education_date)
      }
      this.$refs.appForm.loading = true
      let eventType = 'course'
      if (this.serviceType === 'iku') { eventType = 'event' }
      const saveAppRequest = await apiRequest(
        `/backend/api/v1/applications/${eventType}_application_admin/${this.selectedApp.object_id}/`,
        'PATCH',
        true,
        this.selectedApp
      )
      if (saveAppRequest.error) {
        showAlert(
          'error',
          'Сохранение заявки',
          saveAppRequest.error
        )
      } else {
        showAlert(
          'success',
          'Сохранение заявки',
          saveAppRequest.success
        )
      }
      this.loading = false
      this.$refs.appFormDialog.close()
    },
    // Подготовка к переносу заявки
    prependForAppMove(application) {
      this.appForMove = application
      this.$refs.appMoveDialog.dialog = true
    },
    // Фиксация группы назначения для переноса заявки
    setMoveAppGroup(group) {
      this.groupForMove = group
    },
    // Перенос заявки в другую группу
    async appMove() {
      this.loading = true
      let url = '/backend/api/v1/applications/'
      url += this.serviceType === 'ou' ? 'course_one_move/' : 'event_one_move/'
      try {
        const oneMoveRequest = await apiRequest(
          url,
          'POST',
          true,
          {
            application_id: this.appForMove.object_id,
            group_id: this.groupForMove.object_id
          },
          true
        )
        if (oneMoveRequest.status === 200) {
          showAlert('success', 'Перенос заявки', 'Заявка успешно перенесена')
          this.$refs.appMoveDialog.dialog = false
          this.$refs.mainAppsTable.getRecs()
        } else {
          showAlert('error', 'Пернеос заявки', 'Произошла ошибка в процессе переноса заявки')
        }
      } catch(e) {
        console.log('Ошибка при переносе заявки: ', e)
        showAlert('error', 'Пернеос заявки', 'Произошла ошибка в процессе переноса заявки')
      }

      this.loading = false
    }
  },
  mounted() {
    this.appendOoColumn()
    this.getFormData()
  }
}

</script>

<style scoped>

</style>
