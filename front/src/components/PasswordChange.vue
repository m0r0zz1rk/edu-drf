<template>
  <v-card>
    <v-card-title class="d-flex justify-space-between align-center">
      Смена пароля

      <v-btn
        icon="mdi-close"
        color="coko-blue"
        @click="closeDialog"
      ></v-btn>
    </v-card-title>

    <v-card-text>
      <v-row dense>
        <v-col
          cols="12"
          md="12"
          sm="12"
        >
          <v-text-field
            v-model="pass1"
            :append-inner-icon="pass1Visible ? 'mdi-eye-off' : 'mdi-eye'"
            :type="pass1Visible ? 'text' : 'password'"
            bg-color="white"
            label="Пароль"
            :rules="[rules.required, rules.password]"
            variant="solo"
            @click:append-inner="pass1Visible = !pass1Visible"
            :loading="formLoading"
            clearable
          ></v-text-field>
        </v-col>

        <v-col
          cols="12"
          md="12"
          sm="12"
        >
          <v-text-field
            v-model="pass2"
            :append-inner-icon="pass2Visible ? 'mdi-eye-off' : 'mdi-eye'"
            :type="pass2Visible ? 'text' : 'password'"
            bg-color="white"
            label="Подтверждение"
            :rules="[rules.required, rules.password]"
            variant="solo"
            @click:append-inner="pass2Visible = !pass2Visible"
            :loading="formLoading"
            clearable
          ></v-text-field>
        </v-col>
      </v-row>
      <v-alert
        id="error-pass-change-alert"
        class="alert-hidden"
        style="width: 100%"
        :text="passChangeError"
        type="error"
      ></v-alert>
    </v-card-text>

    <v-divider></v-divider>

    <v-card-actions>
      <v-btn
        color="coko-blue"
        text="Изменить"
        @click="changePassword()"
      ></v-btn>
    </v-card-actions>
  </v-card>
</template>

<script>
import {showAlert} from "@/commons/alerts";
import {apiRequest} from "@/commons/api_request";

export default {
  name: "PasswordChange",
  props: {
    profileUuid: String, // вариативный параметр UUID профиля
    closeDialog: Function // Функция закрытия диалогового окна в родительском компоненте
  },
  data() {
    return {
      formLoading: false,
      pass1: '',
      pass2: '',
      pass1Visible: false,
      pass2Visible: false,
      rules: {
        required: value => !!value || 'Обязательно для заполнения.',
        password: value => value.length >= 8 || 'Минимальная длина пароля - 8 символов'
      },
      passValid: true,
      passChangeError: ''
    }
  },
  methods: {
    passValidation() {
      if (this.pass1.length < 8 || this.pass2.length < 8) {
        this.showPassChangeError('Минимальная длина пароля - 8 символов')
        this.passValid = false
        return false
      }
      if (this.pass1 !== this.pass2) {
        this.showPassChangeError('Введенные пароли не совпадают')
        this.passValid = false
        return false
      }
    },
    showPassChangeError(message) {
      this.passChangeError = message
      document.querySelector('#error-pass-change-alert').classList.add('alert-visible')
      document.querySelector('#error-pass-change-alert').classList.remove('alert-hidden')
    },
    async changePassword() {
      this.passValid = true
      this.passValidation()
      if (this.passValid) {
        this.formLoading = true
        let changePasswordURL = '/backend/api/v1/auth/change_password/'
        let body = {'password': this.pass1}
        if (this.profileUuid) {
          changePasswordURL = '/backend/api/v1/guides/user/password_change/'
          body['profile_id'] = this.profileUuid
        }
        let changePassRequest = await apiRequest(
          changePasswordURL,
          'POST',
          true,
          body
        )
        if (changePassRequest.error) {
          this.showPassChangeError(changePassRequest.error)
        }
        if (changePassRequest.success) {
          showAlert(
            'success',
            'Смена пароля',
            changePassRequest.success
          )
          this.closeDialog()
        }
        this.formLoading = false
      }
    }
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

