<template>

  <PaginationTable
    tableTitle="Удостоверения обучающихся"
    ref="mainCertificateTable"
    tableWidth="98"
    :noTab="false"
    :addButton="false"
    :xlsxButton="false"
    :getRecsURL="'/backend/api/v1/applications/course_certificate?group='+groupCode"
    :tableHeaders="tableHeaders"
    :onEditClick="selectCertificate"
    :fieldsArray="fieldsArray"
  />

  <CokoDialog
    ref="editCertificate"
    :cardActions="true"
  >

    <template v-slot:title>
      Удостоверение заявки {{certificate?.student?.display_name}}
    </template>

    <template v-slot:text>
      <v-row
        v-if="certificate"
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
        :loading="loading"
        color="coko-blue"
        text="Сохранить"
        @click="saveCertificate()"
      />

    </template>

  </CokoDialog>

</template>

<script>

// Модуля для управления информацией об удостоверениях к заявкам на курсы
import PaginationTable from "@/components/tables/pagination_table/PaginationTable.vue";
import DocViewer from "@/components/DocViewer.vue";
import CokoDialog from "@/components/dialogs/CokoDialog.vue";
import {apiRequest} from "@/commons/apiRequest";
import {showAlert} from "@/commons/alerts";

export default {
  name: "StudentGroupCertificates",
  components: {CokoDialog, DocViewer, PaginationTable},
  props: {
    // Код учебной группы
    groupCode: String
  },
  data() {
    return {
      // Столбцы таблицы
      tableHeaders: [
        {
          'title': 'Обучающийся',
          'key': 'student'
        },
        {
          'title': 'Порядковый регистрационный номер',
          'key': 'registration_number'
        },
        {
          'title': 'Серия бланка удостоверения',
          'key': 'blank_serial'
        },
        {
          'title': 'Номер бланка удостоверения',
          'key': 'blank_number'
        },
        {
          'title': 'Управление',
          'key': 'actions'
        }
      ],
      // Описание столбцов таблицы
      fieldsArray: [
        {
          ui: 'appStudentInfo',
          key: 'student',
          addRequired: false,
        },
        {
          ui: 'input',
          type: 'text',
          key: 'registration_number',
          addRequired: true
        },
        {
          ui: 'input',
          type: 'text',
          key: 'blank_serial',
          addRequired: true
        },
        {
          ui: 'input',
          type: 'text',
          key: 'blank_number',
          addRequired: true
        },
        {
          ui: 'actions',
          key: 'actions'
        }
      ],
      // Выбранное удостоверения для редактирования
      certificate: null,
      // Параметр блокировки формы
      loading: false
    }
  },
  methods: {
    // Открыть окно для редактирования информации об удостоверении
    selectCertificate(certificate) {
      this.certificate = certificate
      this.$refs.editCertificate.dialog = true
    },
    // Проверка заполненной формы
    validateForm() {
      if (this.certificate?.registration_number === '') { return false }
      if (this.certificate?.blank_serial === '') { return false }
      return this.certificate?.blank_number !== '';
    },
    // Сохранение информации об удостоверении
    async saveCertificate() {
      if (!(this.validateForm())) {
        showAlert('error', 'Удостоверение', 'Заполните все поля формы')
        return false
      }
      this.loading = true
      try {
        const saveRequest = await apiRequest(
          `/backend/api/v1/applications/course_certificate/${this.certificate?.object_id}/`,
          'PATCH',
          true,
          {
            registration_number: this.certificate?.registration_number,
            blank_serial: this.certificate?.blank_serial,
            blank_number: this.certificate?.blank_number,
          }
        )
        if (saveRequest.success) {
          showAlert('success', 'Удостоверение', 'Данные успешно изменены')
          this.$refs.editCertificate.dialog = false
        } else if (saveRequest.error) {
          showAlert('error', 'Удостоверение', saveRequest.error)
        } else {
          showAlert('error', 'Удостоверение', 'Ошибка при выполнении запроса')
        }
      } catch(e) {
        showAlert('error', 'Удостоверение', 'Ошибка при выполнении запроса')
      }
      this.$refs.mainCertificateTable.getRecs()
      this.loading = false
    }
  }
}
</script>

<style scoped>

</style>
