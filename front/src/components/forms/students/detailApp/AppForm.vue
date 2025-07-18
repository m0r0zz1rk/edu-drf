<template>

  <template
    v-if="internalApp !== null"
  >

    <v-select
        color="coko-blue"
        v-model="internalApp.region_id"
        :items="regions"
        item-title="name"
        item-value="object_id"
        label="Регион*"
        :readonly="disabled"
        :loading="loading"
    />

    <v-select
        v-if="internalApp.region_name === 'Иркутская область'"
        color="coko-blue"
        v-model="internalApp.mo_id"
        :items="mos"
        item-title="name"
        item-value="object_id"
        label="МО*"
        :readonly="disabled"
        :loading="loading"
    />

    <v-select
        color="coko-blue"
        v-model="internalApp.work_less"
        :items="booleanOptions"
        item-title="title"
        item-value="key"
        label="Безработный*"
        :readonly="disabled"
        :loading="loading"
    />

    <template v-if="!(internalApp.work_less)">

      Образовательная организация:<br/>
      <v-btn
        color="coko-blue"
        v-if="(!disabled) && (internalApp.region_name === 'Иркутская область') && (internalApp.mo_id !== null)"
        text="Справочник"
        @click="$refs.ooSelectDialog.dialog = true"
        :readonly="disabled"
        :loading="loading"
      />
      <v-textarea
        color="coko-blue"
        v-model="oo"
        :label="
            internalApp.region_name === 'Иркутская область' ?
              internalApp.mo_id === null ?
                'Введите название ОО (для выбора из справочника выберите МО)*'
                :
                'Введите название ОО или выберите из справочника*'
              :
              'Введите название ОО*'
        "
        :readonly="disabled"
        :loading="loading"
      />
      <v-select
          color="coko-blue"
          v-model="internalApp.position_category_id"
          :items="positionCategories"
          item-title="name"
          item-value="object_id"
          label="Категория должности*"
          :readonly="disabled"
          :loading="loading"
      />
      <v-select
          color="coko-blue"
          v-model="internalApp.position_id"
          :items="positions"
          item-title="name"
          item-value="object_id"
          label="Должность*"
          :readonly="disabled"
          :loading="loading"
      />

    </template>

    <template v-if="appType === 'ou'">

      <v-select
        color="coko-blue"
        v-model="internalApp.education_level"
        :items="educationLevels"
        item-title="title"
        item-value="key"
        label="Уровень образования*"
        :readonly="disabled"
        :loading="loading"
      />

      <v-select
        v-if="internalApp.education_level === 'student'"
        color="coko-blue"
        v-model="internalApp.education_category"
        :items="educationCategories"
        item-title="title"
        item-value="key"
        label="Категория получаемого образования*"
        :readonly="disabled"
        :loading="loading"
      />

      <p
        v-if="internalApp.education_level !== 'student'"
      >
        Диплом об образовании <b style="color:red">(НЕ О ПРОФЕССИОНАЛЬНОЙ ПЕРЕПОДГОТОВКЕ)</b>:
      </p>

      <p
        v-if="internalApp.education_level === 'student'"
      >
        Справка об обучении:
      </p>
      <template
        v-if="internalApp.education_doc_id !== null"
      >
        <v-icon
          color="coko-blue"
          icon="mdi-file-document-outline"
          @click="openDocViewer(
                'Просмотр документа',
                internalApp.education_doc_id,
                'Документ',
                'student'
            )"
        />
        <br/>
      </template>

      <p
        v-if="internalApp.education_doc_id === null"
      >
        <b>(Не выбран)</b>
      </p>
      <v-btn
        v-if="(!disabled)"
        color="coko-blue"
        text="Выбрать"
        @click="$refs.educationDocSelectDialog.dialog = true"
        :readonly="disabled"
        :loading="loading"
      />
      <br/><br/>
      <template
        v-if="internalApp.education_level !== 'student'"
      >

        <v-text-field
          color="coko-blue"
          v-model="internalApp.diploma_surname"
          label="Фамиилия в дипломе*"
          :readonly="disabled"
          :loading="loading"
        />

        <template
          v-if="internalApp.diploma_surname !== internalApp.profile_surname"
        >

          Документ о смене фамилии:<br/>
          <template
            v-if="internalApp.surname_doc_id !== null"
          >
            <v-icon
              v-if="internalApp.surname_doc_id !== null"
              color="coko-blue"
              icon="mdi-file-document-outline"
              @click="openDocViewer(
                'Просмотр документа',
                internalApp.surname_doc_id,
                'Документ',
                'student'
            )"
            />
            <br/>
          </template>

          <p
            v-if="internalApp.surname_doc_id === null"
          >
            <b>(Не выбран)</b>
          </p>
          <v-btn
            v-if="(!disabled)"
            color="coko-blue"
            text="Выбрать"
            @click="$refs.surnameDocSelectDialog.dialog = true"
            :readonly="disabled"
            :loading="loading"
          />
          <br/><br/>

        </template>

        <v-text-field
          color="coko-blue"
          v-model="internalApp.education_serial"
          :rules="[rules.education_serial,]"
          label="Серия диплома*"
          :readonly="disabled"
          :loading="loading"
        />

        <v-text-field
          color="coko-blue"
          v-model="internalApp.education_number"
          :rules="[rules.education_number,]"
          label="Номер диплома*"
          :readonly="disabled"
          :loading="loading"
        />

        <v-date-input
          color="coko-blue"
          v-model="internalApp.education_date"
          label="Дата выдачи диплома*"
          prepend-icon=""
          prepend-inner-icon="$calendar"
          variant="solo"
          :disabled="disabled"
          :loading="loading"
          clearable
        />

      </template>

    </template>

    <v-select
        color="coko-blue"
        v-model="internalApp.physical"
        :items="booleanOptions"
        item-title="title"
        item-value="key"
        label="Физическое лицо*"
        :readonly="disabled"
        :loading="loading"
    />

    <template
      v-if="appType === 'ou'"
    >

      <v-select
          color="coko-blue"
          v-model="internalApp.certificate_mail"
          :items="booleanOptions"
          item-title="title"
          item-value="key"
          label="Отправка удостоверения почтой*"
          :readonly="disabled"
          :loading="loading"
      />

      <v-textarea
          v-if="internalApp.certificate_mail"
          color="coko-blue"
          v-model="internalApp.mail_address"
          label="Почтовый адрес для отправки удостоверения"
          :readonly="disabled"
          :loading="loading"
      />

    </template>


  </template>

  <CokoDialog
    ref="ooSelectDialog"
    :cardActions="false"
  >

    <template v-slot:title>
      Справочник ОО
    </template>

    <template v-slot:text>
      <PaginationTable
          v-if="ooFieldsArray !== null"
          tableTitle="ОО"
          tableWidth="100"
          :noTab="false"
          :addButton="false"
          :xlsxButton="false"
          :getRecsURL="'/backend/api/v1/users/oos/'+internalApp.mo_id+'/'"
          :tableHeaders="ooTableHeaders"
          :fieldsArray="ooFieldsArray"
          :itemSelectEvent="selectOo"
      />
    </template>

  </CokoDialog>

  <CokoDialog
      ref="educationDocSelectDialog"
      :cardActions="false"
  >

    <template v-slot:title>
      Документы обучающегося
    </template>

    <template v-slot:text>
      <PaginationTable
          :tableTitle="
            internalApp.education_level === 'student' ? 'Справки об обучении' : 'Дипломы'
          "
          tableWidth="100"
          :noTab="false"
          :hideSearchButton="true"
          :addButton="true"
          :xlsxButton="false"
          :getRecsURL="internalApp.education_level === 'student' ? getTrainingURL : getDiplomaURL"
          addRecURL="/backend/api/v1/docs/upload_student_doc/"
          :openDocViewerFunction="openDocViewer"
          :tableHeaders="docTableHeaders"
          :fieldsArray="docFieldsArray"
          :itemSelectEvent="selectEduDoc"
          :defaultBody="{
            'doc_type': internalApp.education_level === 'student' ? 'training_certificate' : 'diploma'
          }"
          :haveChooseButton="true"
      />
    </template>

  </CokoDialog>

  <CokoDialog
      ref="surnameDocSelectDialog"
      :cardActions="false"
  >

    <template v-slot:title>
      Документы обучающегося
    </template>

    <template v-slot:text>
      <PaginationTable
          tableTitle="Документ о смене фамилии"
          tableWidth="100"
          :noTab="false"
          :hideSearchButton="true"
          :addButton="true"
          :xlsxButton="false"
          :getRecsURL="getChangeSurnameURL"
          addRecURL="/backend/api/v1/docs/upload_student_doc/"
          :openDocViewerFunction="openDocViewer"
          :tableHeaders="docTableHeaders"
          :fieldsArray="docFieldsArray"
          :itemSelectEvent="selectSurnameDoc"
          :defaultBody="{'doc_type': 'change_surname'}"
          :haveChooseButton="true"
      />
    </template>

  </CokoDialog>

  <CokoDialog
      ref="docViewerDialog"
  >

    <template v-slot:title>
      <p v-if="!mobileDisplay">Просмотр документа</p>
      <p v-if="mobileDisplay">Документ</p>
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

// Форма для просмотра и редактирования анкеты заявки обучающегося
import AppStatusBadge from "@/components/badges/students/AppStatusBadge.vue";
import CokoDialog from "@/components/dialogs/CokoDialog.vue";
import PaginationTable from "@/components/tables/pagination_table/PaginationTable.vue";
import {apiRequest} from "@/commons/apiRequest";
import {showAlert} from "@/commons/alerts";
import educationLevels from "@/commons/consts/apps/educationLevels";
import educationCategories from "@/commons/consts/apps/educationCategories";
import {convertBackendDate, convertDateToBackend} from "@/commons/date";
import {useDisplay} from "vuetify";

export default {
  name: 'AppForm',
  components: {PaginationTable, CokoDialog, AppStatusBadge},
  props: {
    // Объект заявки обучающегося
    studentApp: Object,
    // Тип заявки (ou, iku)
    appType: String,
    // Функция изменения атрибутов объекта заявки в родительском компоненте
    changeAppAttribute: Function,
    // Список регионов РФ
    regions: Array,
    // Список МО
    mos: Array,
    // Список категорий должностей
    positionCategories: Array,
    // Список должностей
    positions: Array,
  },
  data() {
    return {
      // Параметр блокировки редактирования элементов формы
      disabled: this.studentApp.status !== 'draft',
      // Параметр проверки мобильного устройства
      mobileDisplay: useDisplay().smAndDown,
      // Выбранный документ
      docId: null,
      // URL для получения списка справок об обучении
      getTrainingURL: '/backend/api/v1/docs/student_docs/?doc_type=training_certificate',
      // URL для получения списка дипломов
      getDiplomaURL: '/backend/api/v1/docs/student_docs/?doc_type=diploma',
      // URL для получения списка документов о смене фамилии
      getChangeSurnameURL: '/backend/api/v1/docs/student_docs/?doc_type=change_surname',
      // Тип документа
      docType: null,
      // Параметр отображения анимации загрузки на элементах формы
      loading: false,
      // Варианты для выпадающего списка "Безработный" и "Физическое лицо"
      booleanOptions: [
        {key: true, title: 'Да'},
        {key: false, title: 'Нет'},
      ],
      // Внутренний объект заявки
      internalApp: null,
      // Выбранная ОО
      oo: '',
      // Список столбцов для таблицы справочника ОО
      ooTableHeaders: [
        {'title': 'Краткое наименование', 'key': 'short_name'},
        {'title': 'Полное наименование', 'key': 'full_name'},
        {'title': 'Тип ОО', 'key': 'oo_type'}
      ],
      // Список описаний столбцов таблицы справочника ОО
      ooFieldsArray: null,
      // Уровни образования
      educationLevels: educationLevels,
      // Категории получаемого образования
      educationCategories: educationCategories,
      // Наименование выбранного документа об образовании/справки об обучении
      eduDoc: '',
      // Список столбцов таблицы выбора документа об образовании / документа о смене фамилии
      docTableHeaders: [
        {title: 'Дата добавления', key: 'date_create'},
        {title: 'Документ', key: 'file'}
      ],
      // Список описаний столбцов таблицы выбора документа об образовании / документа о смене фамилии
      docFieldsArray: [
        {ui: 'date', key: 'date_create', readOnly: true, addRequired: false,},
        {ui: 'file', key: 'file', addRequired: true}
      ],
      // Регулярное выражение для серии диплома
      educationSerialRegEx: /^[а-яА-ЯёЁ0-9]+$/,
      // Регулярное выражение для номера диплома
      educationNumberRegEx: /^[0-9]+$/,
      // Правила заполнения для полей "Серия диплома" и "Номер диплома"
      rules: {
        education_serial: value => this.educationSerialRegEx.test(value) || 'Некорректная серия диплома.',
        education_number: value => this.educationNumberRegEx.test(value) || 'Некорректный номер диплома.',
      }
    }
  },
  methods: {
    // Открыть окно для просмотра документа
    openDocViewer(fio, docId, docName, docType) {
      this.docId = docId
      this.$refs.docViewerDialog.dialog = true
      this.docType = docType
    },
    // Установка внутреннего объекта заявки
    setInternalApp() {
      this.internalApp = this.studentApp
      this.oo = this.studentApp.oo_name
      try {
        this.internalApp.education_date = convertBackendDate(this.internalApp.education_date)
      } catch (e) {}
      if (this.studentApp.diploma_surname === '') {
        this.internalApp.diploma_surname = this.internalApp.profile_surname
      }
    },
    // Получение списка типов ОО и установка списка описаний столбцов таблицы справочника ОО
    async getOoTypes() {
      let ooTypeListRequest = await apiRequest(
          '/backend/api/v1/users/oo_types/',
          'GET',
          true,
          null
      )
      if (ooTypeListRequest.error) {
        showAlert(
            'error',
            'Получение списка типов ОО',
            ooTypeListRequest.error
        )
        return false
      }
      let oo_types = []
      ooTypeListRequest.map((oo_type) => {
        oo_types.push(oo_type.name)
      })
      this.ooFieldsArray = [
        {
          ui: 'input',
          type: 'text',
          key: 'short_name',
          addRequired: true,
        },
        {
          ui: 'input',
          type: 'text',
          key: 'full_name',
          addRequired: true,
        },
        {
          ui: 'select',
          items: oo_types,
          key: 'oo_type',
          addRequired: true
        }
      ]
    },
    // Установить ОО, выбранную из справочника
    selectOo(oo) {
      this.internalApp.oo_id = oo.object_id
      this.internalApp.oo_name = oo.full_name
      this.oo = oo.full_name
      this.$refs.ooSelectDialog.dialog = false
    },
    // Установить выбранный документ об образовании
    selectEduDoc(doc) {
      this.internalApp.education_doc_name = doc.doc_name
      this.internalApp.education_doc_file = doc.file
      this.internalApp.education_doc_id = doc.object_id
      this.$refs.educationDocSelectDialog.dialog = false
    },
    // Установить выбранный документ о смене фамилии
    selectSurnameDoc(doc) {
      this.internalApp.surname_doc_name = doc.doc_name
      this.internalApp.surname_doc_file = doc.file
      this.internalApp.surname_doc_id = doc.object_id
      this.$refs.surnameDocSelectDialog.dialog = false
    },
  },
  watch: {
    'internalApp.region_id': function (newValue, oldValue) {
      if (oldValue !== null) {
        const newRegName = this.regions.filter((reg) => reg.object_id === newValue)[0].name
        this.internalApp.region_name = newRegName
        this.changeAppAttribute(
            'region_id',
            newValue
        )
        this.changeAppAttribute(
            'region_name',
          newRegName
        )
        if (newRegName !== 'Иркутская область') {
          this.changeAppAttribute(
              'mo_id',
              null
          )
          this.changeAppAttribute(
              'mo_name',
              ''
          )
        }
      }
    },
    'internalApp.work_less': function(newValue, oldValue) {
      if (oldValue !== null) {
        this.changeAppAttribute('work_less', newValue)
        if (newValue === true) {
          this.changeAppAttribute(
              'oo_id',
              null
          )
          this.changeAppAttribute(
              'oo_name',
              ''
          )
          this.changeAppAttribute(
              'oo_new',
              ''
          )
          this.changeAppAttribute(
              'position_category_id',
              null
          )
          this.changeAppAttribute(
              'position_category_name',
              ''
          )
          this.changeAppAttribute(
              'position_id',
              null
          )
          this.changeAppAttribute(
              'position_name',
              ''
          )
        }
      }
    },
    'oo': function(newValue, oldValue) {
      if (this.oo === this.internalApp.oo_name) {
        this.changeAppAttribute('oo_id', this.internalApp.oo_id)
        this.changeAppAttribute('oo_name', this.internalApp.oo_name)
        this.changeAppAttribute('oo_new', '')
      } else {
        this.changeAppAttribute('oo_id', null)
        this.changeAppAttribute('oo_name', '')
        this.changeAppAttribute('oo_new', newValue)
      }
    },
    'internalApp.position_category_id': function(newValue, oldValue) {
      if (newValue !== null) {
        let name = this.positionCategories.filter((pc) => pc.object_id === newValue)[0].name
        this.internalApp.position_category_name = name
        this.changeAppAttribute('position_category_id', newValue)
        this.changeAppAttribute('position_category_name', name)
      } else {
        this.changeAppAttribute('position_category_id', null)
        this.changeAppAttribute('position_category_name', '')
      }
    },
    'internalApp.position_id': function(newValue, oldValue) {
      if (newValue !== null) {
        let name = this.positions.filter((pc) => pc.object_id === newValue)[0].name
        this.internalApp.position_name = name
        this.changeAppAttribute('position_id', newValue)
        this.changeAppAttribute('position_name', name)
      } else {
        this.changeAppAttribute('position_id', null)
        this.changeAppAttribute('position_name', '')
      }

    },
    'internalApp.education_level': function(newValue, oldValue) {
      try {
        this.changeAppAttribute('education_level', newValue)
      } catch (e) {console.log('internalApp.education_level error: ', e)}
    },
    'internalApp.education_category': function(newValue, oldValue) {
      try {
        this.changeAppAttribute('education_category', newValue)
      } catch (e) {console.log('internalApp.education_category error: ', e)}
    },
    'internalApp.education_doc_id': function (newValue, oldValue) {
      try {
        this.changeAppAttribute('education_doc_id', newValue)
        this.changeAppAttribute('education_doc_name', this.internalApp.education_doc_name)
        this.changeAppAttribute('education_doc_file', this.internalApp.education_doc_file)
      } catch (e) {console.log('internalApp.education_doc_id error: ', e)}
    },
    'internalApp.diploma_surname': function (newValue, oldValue) {
      try {
        this.changeAppAttribute('diploma_surname', newValue)
      } catch (e) {console.log('internalApp.diploma_surname error: ', e)}
    },
    'internalApp.surname_doc_id': function (newValue, oldValue) {
      try {
        this.changeAppAttribute('surname_doc_id', newValue)
        this.changeAppAttribute('surname_doc_name', this.internalApp.surname_doc_name)
        this.changeAppAttribute('surname_doc_file', this.internalApp.surname_doc_file)
      } catch (e) {console.log('internalApp.surname_doc_id error: ', e)}
    },
    'internalApp.education_serial': function (newValue, oldValue) {
      try {
        this.changeAppAttribute('education_serial', newValue)
      } catch (e) {console.log('internalApp.education_serial error: ', e)}
    },
    'internalApp.education_number': function (newValue, oldValue) {
      try {
        this.changeAppAttribute('education_number', newValue)
      } catch(e) {console.log('internalApp.education_number error: ', e)}
    },
    'internalApp.education_date': function (newValue, oldValue) {
      try {
        if (!(newValue instanceof Date)) {
          this.changeAppAttribute('education_date', convertDateToBackend(newValue))
        }
      } catch(e) {console.log('internalApp.education_date error: ', e)}

    },
    'internalApp.certificate_mail': function (newValue, oldValue) {
      try {
        this.changeAppAttribute('certificate_mail', newValue)
      } catch(e) {console.log('internalApp.certificate_mail error: ', e)}
    },
    'internalApp.mail_address': function(newValue, oldValue) {
      try {
        this.changeAppAttribute('mail_address', newValue)
      } catch(e) {console.log('internalApp.mail_address error: ', e)}
    }
  },
  mounted() {
    this.setInternalApp()
    this.getOoTypes()
  }
}

</script>

<style scoped>

</style>
<script setup>
import DocViewer from "@/components/DocViewer.vue";
</script>
