<template>

  <v-card
    variant="outlined"
    class="lk-full-page-card"
  >

    <v-card-title class="d-flex justify-space-between align-center">

        Управление группой {{studentGroupInfo?.code}}

    </v-card-title>

    <v-card-text class="adaptive-tab-table-card-text" style="padding: 0;">

      <v-tabs
        :disabled="studentGroupInfo === null"
        style="width: 100%; top: 0; z-index: 10; position: sticky"
        v-model="groupTab"
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
          class="coko-tab"
          value="manage"
        >
          Управление
        </v-tab>

        <v-tab
          class="coko-tab"
          value="docs"
        >
          Документы
        </v-tab>

        <v-tab
          class="coko-tab"
          value="apps"
        >
          Заявки
        </v-tab>

        <v-tab
          class="coko-tab"
          value="schedule"
        >
          Расписание
        </v-tab>

        <v-tab
          v-if="studentGroupInfo?.service_type === 'ou' && userRole === 'centre'"
          class="coko-tab"
          value="certificate"
        >
          Удостоверения
        </v-tab>

      </v-tabs>

      <template v-if=" studentGroupInfo === null">
        <b>Пожалуйста, подождите...</b>
      </template>

      <template v-else>

        <StudentGroupInfo
          v-if="groupTab === 'info'"
          :groupInfo="studentGroupInfo"
        />

        <StudentGroupManage
          ref="groupManage"
          v-if="groupTab === 'manage'"
          :groupId="groupId"
          :groupInfo="studentGroupInfo"
          :userRole="userRole"
        />

        <StudentGroupDocs
          v-if="groupTab === 'docs'"
          :groupId="groupId"
          :studentGroupInfo="studentGroupInfo"
          :userRole="userRole"
        />

        <StudentGroupApps
          ref="studentGroupAppModule"
          v-if="groupTab === 'apps'"
          :groupId="groupId"
          :serviceType="studentGroupInfo?.service_type"
          :openDocViewer="openDocViewer"
        />

        <StudentGroupSchedule
          v-if="groupTab === 'schedule'"
          :groupId="groupId"
          :serviceType="studentGroupInfo?.service_type"
          :code="studentGroupInfo?.code"
        />

        <StudentGroupCertificates
          ref="studentGroupCertificates"
          v-if="studentGroupInfo?.service_type === 'ou' && groupTab === 'certificate' && userRole === 'centre'"
          :groupCode="studentGroupInfo?.code"
          :openDocViewer="openDocViewer"
        />

      </template>

    </v-card-text>

    <v-card-actions
      style="background-color: white"
    >

      <v-spacer />

      <template v-if=" studentGroupInfo !== null">

        <v-btn
          variant="flat"
          v-if="groupTab === 'manage'"
          color="coko-blue"
          text="Сохранить"
          :loading="loading"
          @click="saveGroup()"
        />

        <v-btn
          variant="flat"
          v-if="groupTab === 'apps' && userRole === 'centre'"
          color="coko-blue"
          text="Смена оплаты"
          :loading="loading"
          @click="$refs.paymentTypeChangeDialog.dialog = true"
        />

        <v-btn
          variant="flat"
          v-if="groupTab === 'apps' && userRole === 'centre'"
          color="coko-blue"
          text="Перенос заявок"
          :loading="loading"
          @click="getAppsToMove(); $refs.appMoveDialog.dialog = true"
        />

        <v-btn
          variant="flat"
          v-if="groupTab === 'apps' && checkData?.oo?.length !== 0"
          color="coko-blue"
          text="ОО"
          :loading="loading"
          @click="openCheckDataDialog('Проверка ОО')"
        />

        <v-btn
          variant="flat"
          v-if="groupTab === 'apps' && checkData?.edu?.length !== 0"
          color="coko-blue"
          text="Образование"
          :loading="loading"
          @click="openCheckDataDialog('Проверка образования')"
        />

        <v-btn
          variant="flat"
          v-if="groupTab === 'apps' && checkData?.pay?.length !== 0"
          color="coko-blue"
          text="Оплата"
          :loading="loading"
          @click="openCheckDataDialog('Проверка оплаты')"
        />

        <v-btn
          variant="flat"
          v-if="groupTab === 'certificate' && userRole === 'centre'"
          color="coko-blue"
          text="Генерация"
          :loading="loading"
          @click="openCertGenerate()"
        />

        <v-btn
          variant="flat"
          v-if="groupTab === 'certificate' && userRole === 'centre'"
          color="coko-blue"
          text="Файл печати"
          :loading="loading"
          @click="printFile()"
        />

        <v-btn
          variant="flat"
          v-if="groupTab === 'certificate' && userRole === 'centre'"
          color="coko-blue"
          text="Подгрузка"
          :loading="loading"
          @click="openUploadLicense()"
        />

      </template>

    </v-card-actions>

  </v-card>

  <CokoDialog ref="docViewerDialog">

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

  <CokoDialog ref="checkDataDialog" v-if="checkData !== null">

    <template v-slot:title>
      {{ checkDialogTitle }}
    </template>

    <template v-slot:text>

      <CheckOo
        v-if="checkDialogTitle === 'Проверка ОО'"
        :groupId="groupId"
        :serviceType="studentGroupInfo?.service_type"
        :ooData="checkData.oo"
        :changeCheckData="changeCheckData"
        :updateApps="updateApps"
      />

      <CheckEdu
        v-if="checkDialogTitle === 'Проверка образования'"
        :groupId="groupId"
        :serviceType="studentGroupInfo?.service_type"
        :eduData="checkData.edu"
        :changeCheckData="changeCheckData"
        :updateApps="updateApps"
      />

      <CheckPay
        v-if="checkDialogTitle === 'Проверка оплаты'"
        :groupId="groupId"
        :serviceType="studentGroupInfo?.service_type"
        :payData="checkData.pay"
        :changeCheckData="changeCheckData"
        :updateApps="updateApps"
      />

    </template>

  </CokoDialog>

  <CokoDialog v-if="userRole === 'centre'" ref="paymentTypeChangeDialog" :cardActions="true">

    <template v-slot:title>Изменение типа оплаты обучающихся</template>

    <template v-slot:text>
      Выберите тип оплаты, который необходимо установить всем обучающиимя
      <v-row
        dense
      >

        <v-col
          cols="12"
          md="12"
          sm="12"
        >
          <v-select
            bg-color="white"
            variant="solo"
            v-model="paymentType"
            :items="paymentTypes"
            item-title="title"
            item-value="key"
            label="Тип оплаты"
            :loading="loading"
          />
        </v-col>

      </v-row>

    </template>

    <template v-slot:actions>

      <v-btn
        variant="flat"
        :loading="loading"
        color="coko-blue"
        text="Сохранить"
        @click="changePaymentType()"
      />

    </template>

  </CokoDialog>

  <CokoDialog v-if="userRole === 'centre'" ref="appMoveDialog" :cardActions="true">

    <template v-slot:title>
      <div v-if="appsToMove.length === 0">
        Перенос всех заявок группы "{{studentGroupInfo?.code}}"
      </div>
      <div v-else>
        Перенос выбранных заявок группы "{{studentGroupInfo?.code}}"
      </div>

    </template>

    <template v-slot:text>

      <template v-if="appsToMove.length !== 0">
        Количество выбранных заявок: <b>{{appsToMove.length}}</b><br/>
      </template>

      <template v-if="groupForMove">
       Выбранная группа для переноса:  <b>{{groupForMove.code}}</b>
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
        :itemSelectEvent="setGroupForMove"
      />

    </template>

    <template v-slot:actions>
      <v-btn
        variant="flat"
        :disabled="groupForMove === null"
        :loading="loading"
        color="coko-blue"
        text="Переместить"
        @click="appMove()"
      />
    </template>

  </CokoDialog>

  <CokoDialog v-if="userRole === 'centre'" ref="generateCertificate" :cardActions="true">

    <template v-slot:title>
      Генерация данных об удостоверениях
    </template>

    <template v-slot:text>
      Задайте значения для первого удостоверения
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
            v-model="certificate.registration_number"
            label="Порядковый регистрационный номер*"
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
            v-model="certificate.blank_serial"
            label="Серия бланка удостоверения*"
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
            v-model="certificate.blank_number"
            label="Номер бланка удостоверения*"
            :loading="loading"
          />
        </v-col>

      </v-row>

    </template>

    <template v-slot:actions>

      <v-btn
        variant="flat"
        :loading="loading"
        color="coko-blue"
        text="Сохранить"
        @click="certificateGenerate()"
      />

    </template>

  </CokoDialog>

  <CokoDialog v-if="userRole === 'centre'" ref="uploadLicense" :cardActions="true">

    <template v-slot:title>Подгрузка сканов удостоверений</template>

    <template v-slot:text>
      Для корректной загрузки сканов удостоверений пользователей необходимо подгрузить архив в формате .rar, в
      котором располагаются сканы удостоверений пользователей cо следующим форматом имени файла:
      (регистрационный номер).pdf
      <v-row
        dense
      >

        <v-col
          cols="12"
          md="12"
          sm="12"
        >
          <v-file-input
            :loading="loading"
            label="Архив со сканами удостоверений"
            v-model="licenseArchive"
          />
        </v-col>

      </v-row>

    </template>

    <template v-slot:actions>

      <v-btn
        variant="flat"
        :loading="loading"
        color="coko-blue"
        text="Отправить"
        @click="uploadLicenses()"
      />

    </template>

  </CokoDialog>

</template>

<script>
import LkPage from "@/components/LkPage.vue";
import StudentGroupInfo from "@/components/forms/edu/student-group/StudentGroupInfo.vue";
import StudentGroupManage from "@/components/forms/edu/student-group/StudentGroupManage.vue";
import {apiRequest} from "@/commons/apiRequest";
import {showAlert} from "@/commons/alerts";
import studentGroupStatuses from "@/commons/consts/edu/studentGroupStatuses";
import StudentGroupDocs from "@/components/forms/edu/student-group/StudentGroupDocs.vue";
import studyForms from "@/commons/consts/edu/studyForms";
import StudentGroupSchedule from "@/components/forms/edu/student-group/StudentGroupSchedule.vue";
import StudentGroupApps from "@/components/forms/edu/student-group/StudentGroupApps.vue";
import CokoDialog from "@/components/dialogs/CokoDialog.vue";
import DocViewer from "@/components/DocViewer.vue";
import {useDisplay} from "vuetify";
import {CheckOo, CheckEdu, CheckPay} from "@/components/forms/edu/student-group/check-data";
import PaginationTable from "@/components/tables/pagination_table/PaginationTable.vue";
import StudentGroupCertificates from "@/components/forms/edu/student-group/StudentGroupCertificates.vue";
import {getCookie} from "@/commons/cookie";

export default {
  name: "StudentGroupForm",
  components: {
    StudentGroupCertificates,
    PaginationTable,
    CheckEdu,
    CheckOo,
    CheckPay,
    DocViewer,
    CokoDialog,
    StudentGroupApps, StudentGroupSchedule, StudentGroupDocs, StudentGroupManage, StudentGroupInfo, LkPage},
  props: {
    groupId: String, // object_id учебной группы
  },
  data() {
    return {
      // Роль пользователя
      userRole: getCookie('cokoRole'),
      groupTab: 'info', // Выбранная вкладка на форме
      loading: false, // Параметр отображения анимации загрузки на элементах формы
      // Объект с информацией об учебной группе
      studentGroupInfo: null,
      code: '', // Код учебной группы
      serviceType: '', // Тип услуги учебной группы (ou, iku)
      // Параметр проверки мобильного устройства
      mobileDisplay: useDisplay().smAndDown,
      // object_id выбранного документа,
      docId: '',
      // Выбранный тип документа
      docType: '',
      // Наименование документа,
      docName: '',
      // ФИО обучаюещегося - владельца документа
      docFIO: '',
      // Заголовок диалоговогоо окна для проверки данных
      checkDialogTitle: '',
      // Список данных для проверки
      checkData: null,
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
      // Выбранная группа для переноса
      groupForMove: null,
      // Данные для генерации удостоверений
      certificate: {
        registration_number: '',
        blank_serial: '',
        blank_number: ''
      },
      // Список выбранных заявок для переноса на вкладке "Заявки"
      appsToMove: [],
      // Архив со сканами удостоверений
      licenseArchive: null,
      // Возможные типы оплаты
      paymentTypes: [
        {key: false, title: 'Юр. лицо'},
        {key: true, title: 'Физ. лицо'}
      ],
      // Тип оплаты всех обучающихся
      paymentType: false
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
    // Сохранить информацию по учебной группе
    async saveGroup() {
      let groupInfo = this.$refs.groupManage.groupInfo
      if ((groupInfo.code === null) || (groupInfo.code.length === 0)) {
        showAlert(
          'error',
          'Изменение информации',
          'Некорректный шифр учебной группы'
        )
        return false
      }
      if (studentGroupStatuses.filter((status) => status.key === groupInfo['status']).length === 0) {
        groupInfo['status'] = studentGroupStatuses.filter((status) => status.title === groupInfo['status'])[0].key
      }
      if (studyForms.filter((form) => form.key === groupInfo['form']).length === 0) {
        groupInfo['form'] = studyForms.filter((form) => form.title === groupInfo['form'])[0].key
      }
      this.loading = true
      let updateRequest = await apiRequest(
        '/backend/api/v1/edu/student_group/'+this.groupId+'/',
        'PATCH',
        true,
        groupInfo
      )
      if (updateRequest.error) {
        showAlert('error', 'Обновление информации', updateRequest.error)
        return false
      } else {
        showAlert('success', 'Обновление информации', updateRequest.success)
        this.studentGroupInfo = null
        this.getGroupInfo()
        this.groupTab = 'info'
      }
      this.loading = false
    },
    // Получение кода учебной группы, данных для проверки и типа услуги
    async getGroupInfo() {
      if (this.studentGroupInfo === null) {
        this.loading = true
        let getGroupCodeRequest = await apiRequest(
          `/backend/api/v1/edu/student_group/${this.groupId}/`,
          'GET',
          true,
          null,
          true
        )
        if (getGroupCodeRequest.status === 200) {
          let groupInfo = await getGroupCodeRequest.json()
          this.studentGroupInfo = groupInfo
          this.code = groupInfo.code
          this.serviceType = groupInfo.service_type
          this.checkData = groupInfo.check_data
        }
        this.loading = false
      }
    },
    // Открыть диалоговое окно для проверки данных
    openCheckDataDialog(title) {
      this.checkDialogTitle = title
      this.$refs.checkDataDialog.dialog = true
    },
    // Функция для изменения объекта со списками заявок на проверку данны
    changeCheckData(type, value) {
      this.checkData[type] = value
    },
    // Выбрать группу для переноса заявок
    setGroupForMove(group) {
      this.groupForMove = group
    },
    // Перенос заявок в другую группу
    async appMove() {
      this.loading = true
      const baseUrl = '/backend/api/v1/applications/'
      let additionalUrl = this.serviceType === 'ou' ? 'course_all_move/' : 'event_all_move/'
      let body = {
        source_group_id: this.studentGroupInfo.object_id,
        destination_group_id: this.groupForMove.object_id
      }
      if (this.appsToMove.length > 0) {
        additionalUrl = this.serviceType === 'ou' ? 'course_select_move/' : 'event_select_move/'
        delete body.source_group_id
        body.apps = this.appsToMove
      }
      try {
        const oneMoveRequest = await apiRequest(
          `${baseUrl}${additionalUrl}`,
          'POST',
          true,
          body,
          true
        )
        if (oneMoveRequest.status === 200) {
          showAlert('success', 'Перенос заявки', 'Заявки успешно перенесены')
          this.$refs.appMoveDialog.dialog = false
          this.$refs.studentGroupAppModule.$refs.mainAppsTable.getRecs()
        } else {
          showAlert('error', 'Пернеос заявки', 'Произошла ошибка в процессе переноса заявок')
        }
      } catch(e) {
        showAlert('error', 'Пернеос заявки', 'Произошла ошибка в процессе переноса заявок')
      }
      this.loading = false
    },
    // Открыть диалоговое окно для генерации удостоверений
    openCertGenerate() {
      this.$refs.generateCertificate.dialog = true
    },
    // Открыть диалоговое окно для подгрузки сканов удостоверений
    openUploadLicense() {
      this.$refs.uploadLicense.dialog = true
    },
    // Отправить запрос на генерацию удостоверений
    async certificateGenerate() {
      if ((this.certificate.registration_number === '') ||
          (this.certificate.blank_serial === '') ||
          (this.certificate.blank_number === '')) {
        showAlert('error', 'Удостоверения', 'Задайте все необходимые параметры')
        return false
      }
      this.loading = true
      try {
        const saveRequest = await apiRequest(
          `/backend/api/v1/applications/course_certificate/generate/`,
          'POST',
          true,
          {
            registration_number: this.certificate?.registration_number,
            blank_serial: this.certificate?.blank_serial,
            blank_number: this.certificate?.blank_number,
            group_id: this.groupId
          }
        )
        if (saveRequest.success) {
          showAlert('success', 'Удостоверение', 'Данные успешно сгенерированы')
          this.$refs.generateCertificate.dialog = false
        } else if (saveRequest.error) {
          showAlert('error', 'Удостоверение', saveRequest.error)
        } else {
          showAlert('error', 'Удостоверение', 'Ошибка при выполнении запроса')
        }
      } catch(e) {
        showAlert('error', 'Удостоверение', 'Ошибка при выполнении запроса')
      }
      this.$refs.studentGroupCertificates.$refs.mainCertificateTable.getRecs()
      this.loading = false
    },
    // Формирование запроса на получение файла печати
    async printFile() {
      let toPrintOffice = false
      if (confirm('Отправить файл печати дополнительно в типографию?')) {
        toPrintOffice = true
      }
      this.loading = true
      try {
        const printFileRequest = await apiRequest(
          '/backend/api/v1/docs/print_file/',
          'POST',
          true,
          {group_id: this.groupId, to_print_office: toPrintOffice}
        )
        if (printFileRequest.success) {
          showAlert('success', 'Файл печати', printFileRequest.success)
        } else if (printFileRequest.error) {
          showAlert('error', 'Файл печати', printFileRequest.error)
        } else {
          showAlert(
            'error',
            'Файл печати',
            'Произошла ошибка при отправке запроса на получение файла печати'
          )
        }
      } catch (e) {
        showAlert(
          'error',
          'Файл печати',
          'Произошла ошибка при отправке запроса на получение файла печати'
        )
      }
      this.loading = false
    },
    // Получение списка заявок для переноса из таблицы на вкладке "Заявки"
    getAppsToMove() {
      this.appsToMove = this.$refs.studentGroupAppModule.$refs.mainAppsTable.itemsList
    },
    // Функция подгрузки сканов удостоверений
    async uploadLicenses() {
      if (this.licenseArchive === null) {
        showAlert('error', 'Архив', 'Выберите файл формата .rar')
        return
      }
      this.loading = true
      try {
        let formData = new FormData()
        formData.append('file', this.licenseArchive)
        formData.append('group_id', this.groupId)
        const uploadLicensesRequest = await apiRequest(
          '/backend/api/v1/docs/upload_license/',
          'POST',
          true,
          formData,
          false,
          true
        )
        if (uploadLicensesRequest.success) {
          showAlert('success', 'Сканы удостоверений', uploadLicensesRequest.success)
          this.$refs.studentGroupCertificates.$refs.mainCertificateTable.getRecs()
          this.$refs.uploadLicense.close()
        } else if (uploadLicensesRequest.error) {
          showAlert('error', 'Сканы удостоверений', uploadLicensesRequest.error)
        } else {
          showAlert(
            'error',
            'Сканы удостоверений',
            'Произошла ошибка при подгрузке сканов удостоверений'
          )
        }
      } catch (e) {
        showAlert(
          'error',
          'Файл печати',
          'Произошла ошибка при отправке запроса на получение файла печати'
        )
      }
      this.loading = false
    },
    // Обновить данные на вкладке "Заявки"
    updateApps() {
      this.$refs.studentGroupAppModule.$refs.mainAppsTable.getRecs()
    },
    //Сменить тип оплаты
    async changePaymentType() {
      this.loading = true
      const paymentChangeRequest = await apiRequest(
        '/backend/api/v1/edu/student_group/payment_type/',
        'POST',
        true,
        {group_id: this.groupId, payment_type: this.paymentType},
      )
      if (paymentChangeRequest.success) {
        showAlert('success', 'Смена типа оплаты', 'Тип оплаты успешно изменен')
        this.updateApps()
        this.$refs.paymentTypeChangeDialog.close()
      } else {
        showAlert('error', 'Смена типа оплаты', 'Ошибка при смене типа оплаты')
      }
      this.loading = false
    }
  },
  mounted() {
    this.getGroupInfo()
  }
}
</script>

<style scoped>

</style>
