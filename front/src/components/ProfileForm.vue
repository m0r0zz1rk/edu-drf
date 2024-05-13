<template>
  <v-card
    class="lk-full-page-card"
    color="coko-blue"
  >
    <v-card-title class="d-flex justify-space-between align-center">

      <span v-if="!(profileUuid)">
        Профиль пользователя
      </span>

      <v-tabs
        v-if="profileUuid"
        class="guides-tabs"
        v-model="userInfoTab"
        bg-color="coko-blue"
        show-arrows
      >
        <v-tab class="coko-tab" value="profile">Профиль</v-tab>
        <v-tab class="coko-tab" value="apps">Заявки</v-tab>

      </v-tabs>

      <v-btn
        v-if="profileUuid"
        icon="mdi-close"
        color="coko-blue"
        @click="closeDialogEvent"
      ></v-btn>

    </v-card-title>

    <v-card-text>

      <div style="margin-top: 5px;">

        <div v-if="userInfoTab === 'profile'">
          <v-row dense>
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
          <v-alert
            id="error-profile-form-alert"
            class="alert-hidden"
            style="width: 100%"
            :text="profileFormError"
            type="error"
          ></v-alert>
        </div>

      </div>

    </v-card-text>

    <v-divider></v-divider>

    <v-card-actions style="background-color: white">

      <v-spacer></v-spacer>

      <v-btn
        color="coko-blue"
        text="Смена пароля"
        :loading="formLoading"
        @click="passwordDialog = true"
      ></v-btn>

      <v-btn
        color="coko-blue"
        text="Сохранить"
        :loading="formLoading"
        @click="saveProfile()"
      ></v-btn>
    </v-card-actions>

  </v-card>

  <v-dialog
    persistent
    class="adaptive-change-pass-dialog"
    v-model="passwordDialog"
  >

    <PasswordChange
      :profileUuid="profileUuid"
      :closeDialog="() => {passwordDialog = false}"
    />

  </v-dialog>
</template>

<script>
import {apiRequest} from "@/commons/api_request";
import {showAlert} from "@/commons/alerts";
import {convertBackendDate, convertDateToBackend} from "@/commons/date";
import email_pattern from "@/commons/email_pattern";
import PasswordChange from "@/components/PasswordChange.vue";

export default {
  name: "ProfileForm",
  components: {PasswordChange},
  props: {
    profileUuid: String, // Вариативный параметр, object_id профиля пользователя,
    closeDialogEvent: Function, // Событие для закрытия диалогового окна (для просмотра профиля из справочников)
  },
  data() {
    return {
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
      states: [],
      sex: [
        'Мужской',
        'Женский'
      ],
      health: [
        'Да',
        'Нет'
      ],
      teacher: [
        'Да',
        'Нет'
      ],
      formLoading: true,
      pass1Visible: false,
      pass2Visible: false,
      registrationError: '',
      rules: {
        required: value => !!value || 'Обязательно для заполнения.',
        phone: value => value.length === 18 || 'Некорректный номер телефона',
        snils: value => value.length === 14 || 'Некорректный СНИЛС',
        email: value => email_pattern.test(value) || 'Некорректный e-mail.'
      },
      dataValid: false,
      passwordDialog: false,
      userInfoTab: 'profile',
      profileFormError: ''
    }
  },
  methods: {
    showProfileFormError(message) {
      this.profileFormError = message
      document.querySelector('#error-profile-form-alert').classList.add('alert-visible')
      document.querySelector('#error-profile-form-alert').classList.remove('alert-hidden')
    },
    async setData() {
      let statesRequest = await apiRequest(
        '/backend/api/v1/guides/states/',
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
        profileInfoURLRequest = '/backend/api/v1/guides/user/'+this.profileUuid+'/'
      }
      let profileRequest = await apiRequest(
        profileInfoURLRequest,
        'GET',
        true,
        null,
      )
      if (profileRequest.error) {
        this.showProfileFormError(profileRequest.error)
      } else {
        this.profileData = profileRequest
      }
      this.formLoading = false
    },
    checkValidData() {
      Object.keys(this.profileData).map((key) => {
        if (key === 'phone') {
          if (this.profileData[key] === null || this.profileData[key].length < 18) {
            this.showProfileFormError('Введите корректный номер телефона')
            this.dataValid = false
            return false
          }
        }
        if (key === 'email') {
          if (this.profileData[key] === null || !(email_pattern.test(this.profileData[key]))) {
            this.showProfileFormError('Введите корректный email')
            this.dataValid = false
            return false
          }
        }
        if (key === 'snils') {
          if (this.profileData[key] === null || this.profileData[key].length < 14) {
            this.showProfileFormError('Введите корректный СНИЛС')
            this.dataValid = false
            return false
          }
        }
        if (this.profileData[key] === null || this.profileData[key].length === 0) {
          this.showProfileFormError('Заполните все обязательные поля формы')
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
          checkURL = '/backend/api/v1/guides/user/check_phone/'
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
          this.showProfileFormError(json.error)
          this.formLoading = false
          return false
        }
        checkURL = '/backend/api/v1/auth/check_profile_email/'
        body = {'email': this.profileData['email']}
        if (this.profileUuid) {
          checkURL = '/backend/api/v1/guides/user/check_email/'
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
          this.showProfileFormError(json.error)
          this.formLoading = false
          return false
        }
        checkURL = '/backend/api/v1/auth/check_profile_snils/'
        body = {'snils': this.profileData['snils']}
        if (this.profileUuid) {
          checkURL = '/backend/api/v1/guides/user/check_snils/'
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
          this.showProfileFormError(json.error)
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
        console.log(body)
        let saveProfileURL = '/backend/api/v1/auth/save_profile/'
        if (this.profileUuid) {
          saveProfileURL = '/backend/api/v1/guides/user/update/'
        }
        let dataSaveRequest = await apiRequest(
          saveProfileURL,
          'POST',
          true,
          body
        )
        if (dataSaveRequest.success) {
          showAlert(
            'success',
            'Изменение профиля',
            dataSaveRequest.success
          )
          this.closeDialogEvent()
        }
        if (dataSaveRequest.error) {
          this.showProfileFormError(dataSaveRequest.error)
        }
        this.formLoading = false
      }
    }
  },
  watch: {
    profileData: function() {
      // Your function here, for example:
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
.alert-visible {
  z-index: 100;
}

.alert-hidden {
  display: none;
  z-index: 0;
}
</style>
