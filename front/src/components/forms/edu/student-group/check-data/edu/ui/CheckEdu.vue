<template>

  <template
    v-if="internalEduData === null"
  >
    Пожалуйста, подождите..
  </template>

  <template
    v-else
  >

    <v-alert
      v-if="internalEduData.length === 0"
      color="success"
      icon="$success"
      title="Проверка ОО"
      text="Все документы были проверены"
    />

    <template
      v-if="internalEduData.length > 0 & eduApp !== null"
    >

      <v-text-field
        readonly
        label="ФИО обучающегося"
        v-model="eduApp.student"
        :loading="loading"
      />

      <v-text-field
        readonly
        label="Документ об образовании"
        v-model="docInputText"
        :loading="loading"
        @click="e => openDocViewerDialog('edu')"
      />

      <v-text-field
        v-if="eduApp.surname_doc_id !== null"
        readonly
        label="Документ о смене фамилии"
        v-model="docInputText"
        :loading="loading"
        @click="e => openDocViewerDialog('surname')"
      />

      <v-text-field
        label="Указанная фамилия"
        v-model="eduApp.diploma_surname"
        :loading="loading"
      />

      <v-text-field
        label="Серия документа"
        v-model="eduApp.education_serial"
        :loading="loading"
      />

      <v-text-field
        label="Номер документа"
        v-model="eduApp.education_number"
        :loading="loading"
      />

      <v-date-input
        format="DD.MM.YYYY"
        bg-color="white"
        label="Дата выдачи документа"
        v-model="eduApp.education_date"
        prepend-icon=""
        prepend-inner-icon="$calendar"
        variant="solo"
        :loading="loading"
        clearable
      />

      <v-card
        v-if="internalEduData.length > 0 & eduApp !== null"
      >

        <v-card-actions>

          <v-spacer />

          <v-btn
            color="coko-blue"
            text="Пропустить"
            :loading="loading"
            @click="getNext()"
          />

          <v-btn
            color="coko-blue"
            text="Подтвердить"
            :loading="loading"
            @click="saveData()"
          />


        </v-card-actions>

      </v-card>

      <CokoDialog
        ref="docViewerDialog"
        v-if="eduApp !== null"
      >

        <template v-slot:title>
          {{ dialogTitle }} {{eduApp.student}}
        </template>

        <template v-slot:text>

          <DocViewer
            fileType="student"
            :fileId="dialogTitle === 'Документ об образовании' ? eduApp.education_doc_id : eduApp.surname_doc_id"
          />

        </template>

      </CokoDialog>

    </template>

  </template>

</template>


<script>
// Проверка документов об образовании в заявках учебных групп
import CokoDialog from "@/components/dialogs/CokoDialog.vue";
import DocViewer from "@/components/DocViewer.vue";
import {endpoints} from "@/commons/endpoints";
import {apiRequest} from "@/commons/apiRequest";
import {showAlert} from "@/commons/alerts";
import {convertBackendDate, convertDateToBackend} from "@/commons/date";

export default {
  name: "CheckEdu",
  components: {DocViewer, CokoDialog},
  props: {
    // object_id учебной группы
    groupId: String,
    // Тип услуги (ou или iku)
    serviceType: String,
    // Список данных для проверки
    eduData: Array,
    // Функция изменения объекта со списками заявок на проверку данных
    changeCheckData: Function
  },
  data() {
    return {
      // Индекс для массива данных
      index: 0,
      // Текущая заявка на редактирование
      eduApp: null,
      // Индикатор лоадера
      loading: false,
      // Внутренний список с заявками для проверки ОО
      internalEduData: null,
      // Текст поля для просмотра документа об образовании
      docInputText: 'Нажмите для просмотра документа',
      // Заголовок диалогового окна
      dialogTitle: 'Документ об образовании'
    }
  },
  methods: {
    // Установка выбранной заявки в качестве редактируемой
    setApp(app) {
      this.eduApp = app
      this.eduApp.education_date = convertBackendDate(this.eduApp.education_date)
    },
    // Установка первой заявки при рендере компонента и списка заявок
    setFirstAppAndInternalEduData() {
      this.internalEduData = this.eduData
      this.setApp(this.eduData[0])
    },
    // Получить следующую заявку из списка
    getNext(afterSave = false) {
      this.eduApp = null
      if (!afterSave) {
        if (this.internalEduData.length === 0) { return }
        if (this.index >= this.internalEduData.length - 1) { this.index = -1 }
        this.index++
      }
      this.setApp(this.internalEduData[this.index])
    },
    // Зафиксировать данные и перейти к следующей заявке
    async saveData() {
      this.loading = true
      let url = endpoints['courseApplicationAdmin']
      if (this.serviceType === 'iku') { url = endpoints['eventApplicationAdmin'] }
      const ooSaveRequest = await apiRequest(
        `${url}${this.eduApp.app_id}/`,
        'PATCH',
        true,
        {
          'education_date': convertDateToBackend(this.eduApp.education_date),
          'education_serial': this.eduApp.education_serial,
          'education_number': this.eduApp.education_number,
          'diploma_surname': this.eduApp.diploma_surname,
          'education_check': true
        },
        true
      )
      if (ooSaveRequest.status === 200) {
        showAlert('success', 'Проверка ОО', 'Информация успешно сохранена')
        this.internalEduData = this.internalEduData.filter((rec) => rec.app_id !== this.eduApp.app_id)
        this.loading = false
        this.getNext(true)
      } else {
        showAlert('error', 'Проверка ОО', 'Ошибка при обновлении информации в заявке')
      }
    },
    // Открыть диалоговое окно для просмотра документа
    // type - принимает значение edu или surname
    openDocViewerDialog(type) {
      this.dialogTitle = 'Документ об образовании'
      if (type === 'surname') {
        this.dialogTitle = 'Документ о смене фамилии'
      }
      this.$refs.docViewerDialog.dialog = true
    }
  },
  mounted() {
    this.setFirstAppAndInternalEduData()
  },
  watch: {
    internalEduData: function(newValue, oldValue) {
      if (!([newValue, oldValue].includes(null)) && newValue !== this.eduData) {
        this.changeCheckData('edu', newValue)
      }
    }
  }
}
</script>

<style scoped>

</style>
