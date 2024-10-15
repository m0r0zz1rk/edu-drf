<template>

  <PaginationTable
      tableTitle="Заявки группы"
      tableWidth="98"
      :noTab="false"
      :addButton="false"
      :xlsxButton="false"
      :getRecsURL="
        serviceType === 'ou' ?
          '/backend/api/v1/applications/course_group_apps/'+groupId+'/'
          :
          ''
      "
      :tableHeaders="tableHeaders"
      :fieldsArray="fieldsArray"
      :openDocViewerFunction="openDocViewer"
  />

  <CokoDialog
    ref="docViewerDialog"
  >

    <template v-slot:title>
      {{docName}} обучающегося {{docFIO}}
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

export default {
  name: 'StudentGroupApps',
  components: {DocViewer, CokoDialog, PaginationTable},
  props: {
    groupId: String, // object_id учбеной группы
    serviceType: String, // Тип услуги учебной группы (ou или iku)
  },
  data() {
    return {
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
      // ФИО обучаюещегося
      docFIO: ''
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
    }
  }
}

</script>

<style scoped>

</style>