<template>
  <v-card
    class="lk-full-page-card"
    color="coko-blue"
  >
    <v-card-title class="d-flex justify-space-between align-center">

      <v-tabs
        v-model="userInfoTab"
        bg-color="coko-blue"
        show-arrows
      >
        <v-tab
            class="coko-tab"
            value="profile"
        >
          Профиль
        </v-tab>

        <v-tab
            class="coko-tab"
            value="docs"
        >
          Документы
        </v-tab>

        <v-tab
            v-if="profileUuid"
            class="coko-tab"
            value="course_apps"
        >
          ОУ
        </v-tab>

        <v-tab
            v-if="profileUuid"
            class="coko-tab"
            value="event_apps"
        >
          ИКУ
        </v-tab>

      </v-tabs>

      <v-btn
        v-if="profileUuid"
        icon="mdi-close"
        color="coko-blue"
        @click="closeDialogEvent"
      ></v-btn>

    </v-card-title>

    <v-card-text>

      <DialogContentWithError ref="content-error">

        <slot>

          <div v-if="userInfoTab === 'profile'">
            <v-row
                style="margin-top: 15px"
                dense
            >
              <v-col
                cols="12"
                md="4"
                sm="6"
              >
                <v-text-field
                  bg-color="white"
                  label="Фамилия*"
                  v-model="profileData['surname']"
                  :rules="[rules.required,]"
                  variant="solo"
                  :loading="formLoading"
                  @change="e => profileData['surname'] = e.target.value"
                  clearable
                ></v-text-field>
              </v-col>

              <v-col
                cols="12"
                md="4"
                sm="6"
              >
                <v-text-field
                  bg-color="white"
                  label="Имя*"
                  v-model="profileData['name']"
                  :rules="[rules.required,]"
                  variant="solo"
                  :loading="formLoading"
                  @change="e => profileData['name'] = e.target.value"
                  clearable
                ></v-text-field>
              </v-col>

              <v-col
                cols="12"
                md="4"
                sm="6"
              >
                <v-text-field
                  bg-color="white"
                  label="Отчество"
                  v-model="profileData['patronymic']"
                  variant="solo"
                  :loading="formLoading"
                  @change="e => profileData['patronymic'] = e.target.value"
                  clearable
                ></v-text-field>
              </v-col>

              <v-col
                cols="12"
                md="4"
                sm="6"
              >
                <v-text-field
                  bg-color="white"
                  v-mask="'+7 (###) ###-##-##'"
                  :rules="[rules.required, rules.phone]"
                  label="Номер телефона*"
                  v-model="profileData['phone']"
                  variant="solo"
                  :loading="formLoading"
                  @change="e => profileData['phone'] = e.target.value"
                  clearable
                ></v-text-field>
              </v-col>

              <v-col
                cols="12"
                md="4"
                sm="6"
              >
                <v-text-field
                  bg-color="white"
                  :rules="[rules.required, rules.email]"
                  label="Электронная почта*"
                  v-model="profileData['email']"
                  variant="solo"
                  :loading="formLoading"
                  @change="e => profileData['email'] = e.target.value"
                  clearable
                ></v-text-field>
              </v-col>

              <v-col
                cols="12"
                md="4"
                sm="6"
              >
                <v-text-field
                  bg-color="white"
                  v-mask="'###-###-### ##'"
                  :rules="[rules.required, rules.snils]"
                  label="СНИЛС*"
                  v-model="profileData['snils']"
                  variant="solo"
                  :loading="formLoading"
                  @change="e => profileData['snils'] = e.target.value"
                  clearable
                ></v-text-field>
              </v-col>

              <v-col
                cols="12"
                md="4"
                sm="6"
              >
                <v-select
                  :items="states"
                  bg-color="white"
                  label="Государство*"
                  v-model="profileData['state']"
                  variant="solo"
                  :loading="formLoading"
                  @update:modelValue="e => profileData['state'] = e"
                  :rules="[rules.required,]"
                ></v-select>
              </v-col>

              <v-col
                cols="12"
                md="4"
                sm="6"
              >
                <v-date-input
                  bg-color="white"
                  label="Дата рождения*"
                  v-model="profileData['birthday']"
                  v-mask="'##.##.####'"
                  prepend-icon=""
                  prepend-inner-icon="$calendar"
                  variant="solo"
                  :loading="formLoading"
                  clearable
                ></v-date-input>
              </v-col>

              <v-col
                cols="12"
                md="4"
                sm="6"
              >
                <v-select
                  :items="sex"
                  bg-color="white"
                  label="Пол*"
                  v-model="profileData['sex']"
                  :loading="formLoading"
                  :rules="[rules.required,]"
                  @update:modelValue="e => profileData['sex'] = e"
                  variant="solo"
                ></v-select>
              </v-col>

              <v-col
                cols="12"
                md="4"
                sm="6"
              >
                <v-select
                  :items="health"
                  bg-color="white"
                  label="Ограничения по здоровью*"
                  v-model="profileData['health']"
                  :loading="formLoading"
                  :rules="[rules.required,]"
                  @update:modelValue="e => profileData['health'] = e"
                  variant="solo"
                ></v-select>
              </v-col>

              <v-col
                cols="12"
                md="4"
                sm="6"
              >
                <v-select
                  v-if="profileUuid"
                  :items="teacher"
                  bg-color="white"
                  label="Является преподавателем"
                  v-model="profileData['teacher']"
                  :loading="formLoading"
                  @update:modelValue="e => profileData['teacher'] = e"
                  variant="solo"
                ></v-select>
              </v-col>

            </v-row>
            <small class="text-caption text-medium-emphasis">* - обязательные для заполнения поля</small>

          </div>

          <div v-if="userInfoTab === 'docs'">
            <br/>
            <PaginationTable
                tableTitle="Документы обучающегося"
                tableWidth="100"
                :noTab="false"
                :addButton="true"
                :xlsxButton="false"
                :getRecsURL="
                  profileUuid ?
                    '/backend/api/v1/docs/student_docs/?profile_id='+profileUuid
                    :
                    '/backend/api/v1/docs/student_docs/'
                "
                :addRecURL="
                  profileUuid ?
                    '/backend/api/v1/docs/student_docs/?profile_id='+profileUuid
                    :
                    //'/backend/api/v1/docs/student_docs/'
                    '/backend/api/v1/docs/upload_student_doc/'
                "
                :tableHeaders="tableHeaders"
                :fieldsArray="fieldsArray"
                :openDocViewerFunction="openDocViewer"
            />
          </div>

          <CourseApps
            v-if="userInfoTab === 'course_apps'"
            :profileUuid="profileUuid"
          />

          <EventApps
            v-if="userInfoTab === 'event_apps'"
            :profileUuid="profileUuid"
          />

        </slot>

      </DialogContentWithError>

    </v-card-text>

    <v-divider></v-divider>

    <v-card-actions
        style="background-color: white"
    >

      <v-spacer></v-spacer>

      <PasswordChange
          v-if="userInfoTab === 'profile'"
          :profileUuid="profileUuid"
          :closeDialog="() => {passwordDialog = false}"
      />

      <v-btn
        v-if="userInfoTab === 'profile'"
        color="coko-blue"
        text="Сохранить"
        :loading="formLoading"
        @click="saveProfile()"
      ></v-btn>
    </v-card-actions>

  </v-card>

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
          fileType="student"
      />
    </template>

  </CokoDialog>

</template>

<script>
import {apiRequest} from "@/commons/apiRequest";
import {showAlert} from "@/commons/alerts";
import {convertBackendDate, convertDateToBackend} from "@/commons/date";
import emailPattern from "@/commons/emailPattern";
import PasswordChange from "@/components/PasswordChange.vue";
import DialogContentWithError from "@/components/dialogs/DialogContentWithError.vue";
import CokoDialog from "@/components/dialogs/CokoDialog.vue";
import PaginationTable from "@/components/tables/pagination_table/PaginationTable.vue";
import studentDocTypes from "@/commons/consts/docs/studentDocTypes";
import CourseApps from "@/components/forms/profile/CourseApps.vue";
import DocViewer from "@/components/DocViewer.vue";
import {useDisplay} from "vuetify";
import EventApps from "@/components/forms/profile/EventApps.vue";

export default {
  name: "ProfileForm",
  components: {EventApps, DocViewer, CourseApps, PaginationTable, CokoDialog, DialogContentWithError, PasswordChange},
  props: {
    profileUuid: String, // Вариативный параметр, object_id профиля пользователя,
    closeDialogEvent: Function, // Событие для закрытия диалогового окна (для просмотра профиля из справочников)
  },
  data() {
    return {
      // Параметр проверки мобильного устройства
      mobileDisplay: useDisplay().smAndDown,
      // Информация о профиле пользователя
      profileData: {
        'surname': '',
        'name': '',
        'patronymic': '',
        'phone': '',
        'email': '',
        'snils': '',
        'state': '',
        'birthday': '',
        'sex': '',
        'health': '',
        'teacher': ''
      },
      // Список доступных государств
      states: [],
      // Список полов
      sex: [
        'Мужской',
        'Женский'
      ],
      // Список возможных значений поля "Ограничение по здоровью"
      health: [
        'Да',
        'Нет'
      ],
      // Список возможных значений поля "Является преподавателем"
      teacher: [
        'Да',
        'Нет'
      ],
      // Параметр оторбражения анимации загрузки на элеметнах формы
      formLoading: true,
      // Параметр отображения пароля в первом поле
      pass1Visible: false,
      // Параметр отображения пароль в поле подтверждения
      pass2Visible: false,
      // Текст ошибки, возникщей при регистрации
      registrationError: '',
      // Правила обработки значений полей формы
      rules: {
        required: value => !!value || 'Обязательно для заполнения.',
        phone: value => value.length === 18 || 'Некорректный номер телефона',
        snils: value => value.length === 14 || 'Некорректный СНИЛС',
        email: value => emailPattern.test(value) || 'Некорректный e-mail.'
      },
      // Параметр валидности полученных данных
      dataValid: false,
      // Параметр отображения диалогового окна для смены пароля
      passwordDialog: false,
      // Выбранная вкладка
      userInfoTab: 'profile',
      // Список возожных типов документов
      studentDocTypes: studentDocTypes,
      // Список столбцов таблицы документов обучающегося
      tableHeaders: [
        {
          'title': 'Дата добавления',
          'key': 'date_create'
        },
        {
          'title': 'Тип документа',
          'key': 'doc_type'
        },
        {
          'title': 'Документ',
          'key': 'file'
        }
      ],
      fieldsArray: [
        {
          ui: 'date',
          key: 'date_create',
          readOnly: true,
          addRequired: false,
        },
        {
          ui: 'select',
          items:studentDocTypes,
          key: 'doc_type',
          addRequired: true,
        },
        {
          ui: 'file',
          key: 'file',
          addRequired: true
        }
      ],
      // Выбранный ID документа
      docId: null
    }
  },
  methods: {
    // Открыть окно для просмотра документа
    openDocViewer(fio, docId, docName, docType) {
      this.docId = docId
      this.$refs.docViewerDialog.dialog = true
    },
    async setData() {
      let statesRequest = await apiRequest(
        '/backend/api/v1/guides/state/',
        'GET',
        false,
        null,
      )
      this.states = []
      statesRequest.map((state) => {
        this.states.push(state.name)
      })
      let profileInfoURLRequest = '/backend/api/v1/auth/get_profile/'
      if (this.profileUuid) {
        profileInfoURLRequest = '/backend/api/v1/guides/student_profile/'+this.profileUuid+'/'
      }
      let profileRequest = await apiRequest(
        profileInfoURLRequest,
        'GET',
        true,
        null,
      )
      if (profileRequest.error) {
        this.$refs["content-error"].showContentError(profileRequest.error)
      } else {
        this.profileData = profileRequest
      }
      this.formLoading = false
    },
    checkValidData() {
      Object.keys(this.profileData).map((key) => {
        if (key === 'phone') {
          if ([undefined, null].includes(this.profileData[key]) || this.profileData[key].length < 18) {
            this.$refs["content-error"].showContentError('Введите корректный номер телефона')
            this.dataValid = false
            return false
          }
        }
        if (key === 'email') {
          if ([undefined, null].includes(this.profileData[key]) || !(emailPattern.test(this.profileData[key]))) {
            this.$refs["content-error"].showContentError('Введите корректный email')
            this.dataValid = false
            return false
          }
        }
        if (key === 'snils') {
          if ([undefined, null].includes(this.profileData[key]) || this.profileData[key].length < 14) {
            this.$refs["content-error"].showContentError('Введите корректный СНИЛС')
            this.dataValid = false
            return false
          }
        }
        if ([undefined, null].includes(this.profileData[key]) || this.profileData[key].length === 0) {
          this.$refs["content-error"].showContentError('Заполните все обязательные поля формы')
          this.dataValid = false
          return false
        }
      })
    },
    async saveProfile() {
      this.dataValid = true
      this.checkValidData()
      if (this.dataValid) {
        this.formLoading = true
        let checkURL = '/backend/api/v1/auth/check_profile_phone/'
        let body = {'phone': this.profileData['phone']}
        if (this.profileUuid) {
          checkURL = '/backend/api/v1/guides/student_profile/check_phone/'
          body['profile_id'] = this.profileUuid
        }
        let checkPhone = await apiRequest(
          checkURL,
          'POST',
          true,
          body,
          true
        )
        if (checkPhone.status !== 200) {
          let json = await checkPhone.json()
          this.$refs["content-error"].showContentError(json.error)
          this.formLoading = false
          return false
        }
        checkURL = '/backend/api/v1/auth/check_profile_email/'
        body = {'email': this.profileData['email']}
        if (this.profileUuid) {
          checkURL = '/backend/api/v1/guides/student_profile/check_email/'
          body['profile_id'] = this.profileUuid
        }
        let checkEmail = await apiRequest(
          checkURL,
          'POST',
          true,
          body,
          true
        )
        if (checkEmail.status !== 200) {
          let json = await checkEmail.json()
          this.$refs["content-error"].showContentError(json.error)
          this.formLoading = false
          return false
        }
        checkURL = '/backend/api/v1/auth/check_profile_snils/'
        body = {'snils': this.profileData['snils']}
        if (this.profileUuid) {
          checkURL = '/backend/api/v1/guides/student_profile/check_snils/'
          body['profile_id'] = this.profileUuid
        }
        let checkSnils = await apiRequest(
          checkURL,
          'POST',
          true,
          body,
          true
        )
        if (checkSnils.status !== 200) {
          let json = await checkSnils.json()
          this.$refs["content-error"].showContentError(json.error)
          this.formLoading = false
          return false
        }
        body = {}
        Object.keys(this.profileData).map((key) => {
          if (key === 'sex') {
            body[key] = this.profileData[key] === 'Мужской'
          } else if (key === 'health') {
            body[key] = this.profileData[key] === 'Да'
          } else if (key === 'teacher') {
            if (this.profileUuid) {
              body[key] = this.profileData[key] === 'Да'
            }
          } else if (key === 'birthday') {
            body[key] = convertDateToBackend(this.profileData[key])
          } else {
            body[key] = this.profileData[key]
          }
        })
        if (this.profileUuid) {
          body['object_id'] = this.profileUuid
        }
        let saveProfileURL = '/backend/api/v1/auth/save_profile/'
        if (this.profileUuid) {
          saveProfileURL = '/backend/api/v1/guides/student_profile/update/'
        }
        let dataSaveRequest = await apiRequest(
          saveProfileURL,
          'PATCH',
          true,
          body
        )
        if (dataSaveRequest.success) {
          showAlert(
            'success',
            'Изменение профиля',
            dataSaveRequest.success
          )
          this.formLoading = false
          this.closeDialogEvent()
        }
        if (dataSaveRequest.error) {
          this.$refs["content-error"].showContentError(dataSaveRequest.error)
          this.formLoading = false
        }
      }
    }
  },
  watch: {
    profileData: function() {
      if (this.profileData['sex']) {
        this.profileData['sex'] = 'Мужской'
      } else {
        this.profileData['sex'] = 'Женский'
      }
      if (this.profileData['health']) {
        this.profileData['health'] = 'Да'
      } else {
        this.profileData['health'] = 'Нет'
      }
      if (this.profileUuid) {
        if (this.profileData['teacher']) {
          this.profileData['teacher'] = 'Да'
        } else {
          this.profileData['teacher'] = 'Нет'
        }
      }
      this.profileData['birthday'] = convertBackendDate(this.profileData['birthday'])
    }
  },
  mounted() {
    this.setData()
  }
}
</script>


<style scoped>

</style>
