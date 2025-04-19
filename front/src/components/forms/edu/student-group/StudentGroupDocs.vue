<template>

  <v-expansion-panels
    style="padding-top: 10px"
    variant="accordion"
    color="coko-blue"
  >

    <v-expansion-panel
      color="coko-blue"
      title="Информационное письмо"
    >

      <v-expansion-panel-text>

        <v-btn
          color="coko-blue"
          :loading="loading"
          @click="e => {getDoc('information_letter', 'docx')}"
        >
          Сформировать
        </v-btn>

      </v-expansion-panel-text>

    </v-expansion-panel>

    <v-expansion-panel
      color="coko-blue"
      title="Документы об оказании услуги"
    >

      <v-expansion-panel-text>

        <v-row
        dense
      >

        <v-col
          cols="12"
          md="6"
          sm="6"
        >

          <v-btn
            color="coko-blue"
            :loading="loading"
            @click="e => {getDoc('service_memo', 'docx')}"
          >
            Сформировать СЗ
          </v-btn>

        </v-col>

        <v-col
          cols="12"
          md="6"
          sm="6"
        >

          <v-btn
            color="coko-blue"
            :loading="loading"
            @click="e => {getDoc('service_order', 'docx')}"
          >
            Сформировать приказ
          </v-btn>

        </v-col>

      </v-row>

      </v-expansion-panel-text>

    </v-expansion-panel>

    <v-expansion-panel
      color="coko-blue"
      title="Договор оферты"
    >

      <v-expansion-panel-text>

        <v-row
          dense
        >

          <v-col
            cols="12"
            md="4"
            sm="6"
          >

            <v-btn
              color="coko-blue"
              :loading="loading"
              @click="e => {getDoc('offer_project', 'docx')}"
            >
              Сформировать проект
            </v-btn>

          </v-col>

          <v-col
            cols="12"
            md="4"
            sm="6"
          >

            <v-dialog
              color="coko-blue"
              :fullscreen="mobileDisplay"
              v-model="offerModal"
            >
              <template v-slot:activator="{ props: activatorProps }">
                <v-btn
                  color="coko-blue"
                  :loading="loading"
                  v-bind="activatorProps"
                  text="Загрузить скан"
                />
              </template>

              <v-card>

                <v-card-title
                  class="d-flex justify-space-between align-center"
                >
                  Загрузка скана
                </v-card-title>

                <v-card-text>
                  <v-file-input
                    :loading="loading"
                    v-model="offer"
                  />
                </v-card-text>

                <v-card-actions

                  style="background-color: white"
                >

                  <v-spacer></v-spacer>

                  <v-btn
                    color="coko-blue"
                    text="Загрузить"
                    :loading="loading"
                    @click="uploadOffer()"
                  ></v-btn>
                </v-card-actions>
              </v-card>
            </v-dialog>

          </v-col>

          <v-col
            cols="12"
            md="4"
            sm="6"
          >

            <v-btn
              color="coko-blue"
              :loading="loading"
              @click="e => getOffer()"
            >
              Скачать
            </v-btn>

          </v-col>

        </v-row>

      </v-expansion-panel-text>

    </v-expansion-panel>

    <v-expansion-panel
      v-if="studentGroupInfo?.service_type === 'ou'"
      color="coko-blue"
      title="Приказы"
    >

      <v-expansion-panel-text>

        <v-row
            dense
        >

          <v-col
              cols="12"
              md="4"
              sm="6"
          >

            <v-btn
              color="coko-blue"
              :loading="loading"
              @click="e => {getDoc('transfer_order', 'docx')}"
            >
              О зачислении
            </v-btn>

          </v-col>

          <v-col
              cols="12"
              md="4"
              sm="6"
          >

            <v-btn
              color="coko-blue"
              :loading="loading"
              @click="e => {getDoc('deduction_order', 'docx')}"
            >
              Об отчислении
            </v-btn>

          </v-col>

        </v-row>

      </v-expansion-panel-text>

    </v-expansion-panel>

    <v-expansion-panel
      color="coko-blue"
      title="Анкеты"
    >

      <v-expansion-panel-text>

        <v-btn
          color="coko-blue"
          :loading="loading"
          @click="e => {getDoc('forms', 'xlsx')}"
        >
          Скачать
        </v-btn>

      </v-expansion-panel-text>

    </v-expansion-panel>

    <v-expansion-panel
      v-if="studentGroupInfo?.service_type === 'ou'"
      color="coko-blue"
      title="Закрывной документ"
    >

      <v-expansion-panel-text>

        <v-btn
          color="coko-blue"
          :loading="loading"
          @click="e => {getDoc('close_doc', 'docx')}"
        >
          Сформировать
        </v-btn>

      </v-expansion-panel-text>

    </v-expansion-panel>

    <v-expansion-panel
      v-if="studentGroupInfo?.service_type === 'ou'"
      color="coko-blue"
      title="Ведомость удостоверений"
    >

      <v-expansion-panel-text>

        <v-text-field
          bg-color="white"
          :rules="[rules.required, ]"
          label="Номер приказа о зачислении"
          v-model="enrollNumber"
          variant="solo"
          :loading="loading"
          clearable
        />

        <v-date-input
          bg-color="white"
          label="Дата приказа о зачислении"
          v-model="enrollDate"
          prepend-icon=""
          prepend-inner-icon="$calendar"
          variant="solo"
          :loading="loading"
          clearable
        ></v-date-input>

        <v-text-field
          bg-color="white"
          :rules="[rules.required, ]"
          label="Номер приказа об отчислении"
          v-model="expNumber"
          variant="solo"
          :loading="loading"
          clearable
        />

        <v-date-input
          bg-color="white"
          label="Дата приказа об отчислении"
          v-model="expDate"
          prepend-icon=""
          prepend-inner-icon="$calendar"
          variant="solo"
          :loading="loading"
          clearable
        ></v-date-input>

        <v-btn
          color="coko-blue"
          :loading="loading"
          @click="e => {getCertificatesList()}"
        >
          Сформировать
        </v-btn>

      </v-expansion-panel-text>

    </v-expansion-panel>

    <v-expansion-panel
      color="coko-blue"
      title="Журнал"
    >

      <v-expansion-panel-text>

        <v-btn
          color="coko-blue"
          :loading="loading"
          @click="e => {getDoc('student_journal', 'xlsx')}"
        >
          Скачать
        </v-btn>

      </v-expansion-panel-text>

    </v-expansion-panel>

  </v-expansion-panels>

</template>

<script>
// Компонент для формирования документов по учебной группе
import {apiRequest} from "@/commons/apiRequest";
import {studentGroupDocTypes} from "@/commons/consts/edu/studentGroupDocTypes";
import {showAlert} from "@/commons/alerts";
import {useDisplay} from "vuetify";
import {convertDateToBackend, convertEnglishDate} from "@/commons/date";

export default {
  name: "StudentGroupDocs",
  props: {
    groupId: String, // object_id учебной группы
    // Информация по учебной группы из родителя
    studentGroupInfo: Object, // Тип услуги учебной группы
  },
  data() {
    return {
      // Индикатор загрузки на элементах формы
      loading: false,
      // Скан договора оферты
      offer: null,
      // Параметр отображения диалогового окна для подгрузки договор оферты
      offerModal: false,
      // Проверка на дисплей мобильного устройства
      mobileDisplay: useDisplay().smAndDown,
      // Правила обработки значений полей формы
      rules: {
        required: value => !!value || 'Обязательно для заполнения.',
      },
      // Номер приказа о зачислении
      enrollNumber: '',
      // Номер приказа об отчислении
      expNumber: '',
      // Дата приказа о зачиселнии
      enrollDate: null,
      // Дата приказа об отчислении
      expDate: null
    }
  },
  methods: {
    // Установить информацию для приказов об отчислении и зачислении
    setInfo() {
      this.enrollNumber = this.studentGroupInfo?.enroll_number
      this.expNumber = this.studentGroupInfo?.exp_number
      this.enrollDate = convertEnglishDate(this.studentGroupInfo?.date_enroll)
      this.expDate = convertEnglishDate(this.studentGroupInfo?.date_exp)
    },
    // Формирование запроса на получение документа запрашиваемого типа
    async getDoc(type, extension) {
      this.loading = true
      const getDocRequest = await apiRequest(
        '/backend/api/v1/edu/student_group/doc/',
        'POST',
        true,
        {group_id: this.groupId, doc_type: type},
        true
      )
      if (getDocRequest.status === 200) {
        let data = await getDocRequest.blob()
        let a = document.createElement('a')
        a.href = window.URL.createObjectURL(data)
        a.download = `${studentGroupDocTypes[type]} ${this.studentGroupInfo?.code}.${extension}`
        a.click()
      } else {
        let message = '\'Произошла ошибка при получении документа'
        let data = await getDocRequest.json()
        if (data.error) {
          message = data.error
        }
        showAlert('error', 'Документ группы', message)
      }
      this.loading = false
    },
    // Формирование запроса на получение ведомоисти удостоверений
    async getCertificatesList() {
      if ((this.enrollNumber === '') ||
          (this.expNumber === '') ||
          (this.enrollDate === null) ||
          (this.expDate === null)) {
        showAlert('error', 'Ведомость удостоверений', 'Заполните поля формы')
        return false
      }
      this.loading = true
      const certificatesListRequest = await apiRequest(
        '/backend/api/v1/edu/student_group/doc/',
        'POST',
        true,
        {
          group_id: this.groupId,
          doc_type: 'certificates_list',
          enroll_date: convertDateToBackend(new Date(this.enrollDate)),
          exp_date: convertDateToBackend(new Date(this.expDate)),
          enroll_number: this.enrollNumber,
          exp_number: this.expNumber
        },
        true
      )
      if (certificatesListRequest.status === 200) {
        let data = await certificatesListRequest.blob()
        let a = document.createElement('a')
        a.href = window.URL.createObjectURL(data)
        a.download = `Ведомость удостоверений ${this.studentGroupInfo?.code}.xlsx`
        a.click()
      } else {
        let message = '\'Произошла ошибка при получении документа'
        let data = await certificatesListRequest.json()
        if (data.error) {
          message = data.error
        }
        showAlert('error', 'Документ группы', message)
      }
      this.loading = false
    },
    // Формирование запрос на получение скана договора оферты
    async getOffer() {
      this.loading = true
      let getDocRequest = await apiRequest(
        '/backend/api/v1/edu/student_group/offer/',
        'POST',
        true,
        {group_id: this.groupId},
        true
      )
      if (getDocRequest.status === 200) {
        let data = await getDocRequest.blob()
        let a = document.createElement('a')
        a.href = window.URL.createObjectURL(data)
        a.download = `Договор оферты ${this.studentGroupInfo?.code}.pdf`
        a.click()
      } else {
        let message = '\'Произошла ошибка при получении документа'
        let data = await getDocRequest.json()
        if (data.error) {
          message = data.error
        }
        showAlert('error', 'Документ оферты', message)
      }
      this.loading = false
    },
    // Загрузить скан договора оферты
    async uploadOffer() {
      this.loading = true
      if (this.offer === null) {
        showAlert('error', 'Загрузка скана', 'Выберите документ')
        return false
      }
      let formData = new FormData()
      formData.append('file', this.offer)
      const offerUploadRequest = await apiRequest(
        '/backend/api/v1/docs/group_offer/'+this.groupId+'/',
        'PATCH',
        true,
        formData,
        true,
        true
      )
      if (offerUploadRequest.status !== 200) {
        showAlert('error', 'Загрузка скана','Произошла ошибка в процессе загрузки скана')
      } else {
        showAlert('success', 'Загрузка скана', 'Документ успешно загружен')
        this.offerModal = false
      }
      this.loading = false
    }
  },
  mounted() {
    this.setInfo()
  }
}
</script>

<style scoped>

</style>
