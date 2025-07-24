<template>
  <div class="login-background-img adaptive-login-background-img"></div>
  <v-card class="login-card adaptive-login-card" variant="outlined">

    <v-card-title class="login-card-title">АИС "Учебный центр". Вход</v-card-title>

    <v-card-text class="login-card-text adaptive-login-card-text">

      <v-tabs class="login-tabs" v-model="loginTab" align-tabs="center" bg-color="coko-blue">
        <v-tab class="coko-tab" value="student">Обучающийся</v-tab>
        <v-tab class="coko-tab" value="coko">Сотрудник центра</v-tab>
      </v-tabs>

      <v-tabs-window v-model="loginTab">
        <v-tabs-window-item value="student">
          <div class="login-form adaptive-login-form">
            <v-radio-group v-model="loginStudentType" inline>
              <v-radio color="coko-red" value="phone">
                <template v-slot:label><b class="login-radio-label">Телефон</b></template>
              </v-radio>
              <v-radio class="login-student-radio-button" color="coko-red" value="email">
                <template v-slot:label><b class="login-radio-label">Почта</b></template>
              </v-radio>
              <v-radio class="login-student-radio-button" color="coko-red" value="snils">
                <template v-slot:label><b class="login-radio-label">СНИЛС</b></template>
              </v-radio>
            </v-radio-group>
            <v-form @submit.prevent="userLogin(false)">
              <v-text-field v-if="loginStudentType === 'phone'"
                            id="phoneTextField"
                            bg-color="white"
                            v-model="phone"
                            v-mask="'+7 (###) ###-##-##'"
                            :rules="[rules.required, rules.phone]"
                            label="Номер телефона"
                            variant="solo"
                            :loading="formLoading"
                            clearable
              />
              <v-text-field v-if="loginStudentType === 'email'"
                            id="emailTextField"
                            bg-color="white"
                            label="Email"
                            :rules="[rules.required, rules.email]"
                            variant="solo"
                            :loading="formLoading"
                            clearable
              />
              <v-text-field v-if="loginStudentType === 'snils'"
                            id="snilsTextField"
                            bg-color="white"
                            v-mask="'###-###-### ##'"
                            label="СНИЛС"
                            :rules="[rules.required, rules.snils]"
                            variant="solo"
                            :loading="formLoading"
                            clearable
              />
              <v-text-field
                id="userPassword"
                :append-inner-icon="passVisible ? 'mdi-eye-off' : 'mdi-eye'"
                :type="passVisible ? 'text' : 'password'"
                bg-color="white"
                label="Пароль"
                :rules="[rules.required,]"
                variant="solo"
                @click:append-inner="passVisible = !passVisible"
                :loading="formLoading"
                clearable
              />
              <v-btn
                class="login-button adaptive-login-button"
                color="coko-blue"
                :loading="formLoading"
                type="submit"
                text="Войти"
              />
            </v-form>
            <v-btn
                style="margin-top: 5px;"
                class="login-button adaptive-login-button"
                color="coko-blue"
                text="Регистрация"
                @click="$refs.regDialog.openDialog()"
                :loading="formLoading"
            />
            <RegistrationDialog ref="regDialog" :usePreLoader="usePreLoader"/>
            <v-btn
              style="margin-top: 5px;"
              class="login-button adaptive-login-button"
              color="coko-blue"
              :loading="formLoading"
              @click="getManual()"
              text="Инструкция"
            /><br/>
            <v-btn
              style="margin-top: 5px;"
              class="login-button adaptive-login-button"
              color="coko-blue"
              :loading="formLoading"
              text="Восстановить пароль"
              @click="$refs.passwordResetDialog.dialog = true"
            />
          </div>
        </v-tabs-window-item>
        <v-tabs-window-item value="coko">
          <div class="login-form">
            <v-form @submit.prevent="userLogin(true)">
              <v-text-field
                id="cokoLogin"
                bg-color="white"
                label="Логин"
                :rules="[rules.required,]"
                variant="solo"
                :loading="formLoading"
                clearable
              ></v-text-field>
              <v-text-field
                id="cokoPassword"
                :append-inner-icon="passVisible ? 'mdi-eye-off' : 'mdi-eye'"
                :type="passVisible ? 'text' : 'password'"
                bg-color="white"
                label="Пароль"
                :rules="[rules.required,]"
                variant="solo"
                :loading="formLoading"
                @click:append-inner="passVisible = !passVisible"
                clearable
              ></v-text-field>
              <v-btn
                class="login-button"
                color="coko-blue"
                :loading="formLoading"
                type="submit"
              >Войти</v-btn>
            </v-form>
          </div>
        </v-tabs-window-item>
      </v-tabs-window>
    </v-card-text>
  </v-card>

  <CokoDialog ref="passwordResetDialog" :cardActions="true">
    <template v-slot:title>Сброс пароля</template>
    <template v-slot:text>
      <v-text-field
        label="Email для сброса пароля"
        v-model="passwordResetEmail"
        :rules="[rules.required, rules.email]"
        variant="solo"
        :loading="formLoading"
        clearable
      />
    </template>
    <template v-slot:actions>
      <v-btn variant="flat" color="coko-blue" text="Сбросить" :loading="formLoading" @click="passwordResetRequest()"/>
    </template>
  </CokoDialog>
</template>

<script>
import {showAlert} from "@/commons/alerts";
import RegistrationDialog from "@/components/dialogs/authen/RegistrationDialog.vue";
import {getUrlParameter} from "@/commons/getUrlParameter";
import DocViewer from "@/components/DocViewer.vue";
import CokoDialog from "@/components/dialogs/CokoDialog.vue";
import {apiRequest} from "@/commons/apiRequest";

export default {
  name: 'Login',
  components: {CokoDialog, DocViewer, RegistrationDialog},
  props: {
    usePreLoader: Function,
  },
  data() {
    return {
      // Выбранная вкладка на форме логина
      loginTab: 'student',
      // Номер телефона на форме
      phone: '',
      // Тип авторизации для обучающегося
      loginStudentType: 'email',
      // Отображение пароля
      passVisible: false,
      // Индикатор активных элементов формы
      formLoading: false,
      // Правила обработки полей
      rules: {
        required: value => !!value || 'Обязательно для заполнения.',
        phone: value => value.length === 18 || 'Некорректный номер телефона',
        snils: value => value.length === 14 || 'Некорректный СНИЛС',
        email: value => {
          const pattern = /^(([^<>()[\]\\.,;:\s@"]+(\.[^<>()[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/
          return pattern.test(value) || 'Некорректный e-mail.'
        },
      },
      // Email для сброса пароля
      passwordResetEmail: ''
    }
  },
  methods: {
    validateLoginForm(cokoLogin) {
      let login = ''
      let password = ''
      if (cokoLogin) {
        login = document.querySelector('#cokoLogin').value
        password = document.querySelector('#cokoPassword').value
      } else {
        switch (this.loginStudentType) {
          case 'phone':
            login = document.querySelector('#phoneTextField').value
            break

          case 'email':
            login = document.querySelector('#emailTextField').value
            break

          default:
            login = document.querySelector('#snilsTextField').value
        }
        password = document.querySelector('#userPassword').value
      }
      if (login.length === 0) {
        showAlert(
          'error',
          'Форма входа',
          cokoLogin ?
                'Введите имя пользователя'
                :
                this.loginStudentType === 'phone' ?
                  'Введите номер телефона'
                  :
                  this.loginStudentType === 'email' ?
                    'Введите адрес электронной почты'
                    :
                    'Введите СНИЛС'
        )
        return false
      }
      if (!(cokoLogin) && (this.loginStudentType === 'phone') && (login.length !== 18)) {
        showAlert(
          'error',
          'Форма входа',
          'Введите корректный номер телефона'
        )
        return false
      }
      if (!(cokoLogin) && (this.loginStudentType === 'snils') && (login.length !== 14)) {
        showAlert(
          'error',
          'Форма входа',
          'Введите корректный СНИЛС'
        )
        return false
      }
      if (password.length === 0) {
        showAlert(
          'error',
          'Форма входа',
          'Введите пароль'
        )
        return false
      }
      return {
        'login': login,
        'password': password
      }
    },
    userLogin(cokoLogin) {
      let validData = this.validateLoginForm(cokoLogin)
      if (validData !== false) {
        let username = validData['login']
        let password = validData['password']
        this.formLoading = true
        this.usePreLoader()
        this.$refs.regDialog.formLoading = true
        this.$store.dispatch('AUTH_REQUEST', { username, password, cokoLogin }).then(() => {
          if (getUrlParameter('nextUrl')) {
            this.$router.push({ path: getUrlParameter('nextUrl') })
          } else {
            this.$router.push('/')
          }})
            .catch((error) => {
              showAlert(
                'error',
                'Авторизация пользователя',
                error
              )
              this.$refs.regDialog.formLoading = false
              this.formLoading = false
              this.usePreLoader()
            })
      }
    },
    // Отправка запроса на смену пароля
    async passwordResetRequest() {
      if (confirm('Вы уверены, что хотите сбросить пароль?')) {
        if (this.passwordResetEmail === null || this.passwordResetEmail.length === 0) {
          showAlert('error', 'Сброс пароля', 'Введите email')
          return
        }
        if (this.rules.email(this.passwordResetEmail) === 'Некорректный e-mail.') {
          showAlert('error', 'Сброс пароля', 'Введите корректный email')
          return
        }
        this.formLoading = true
        const passwordResetReq = await apiRequest(
          `/backend/api/v1/password_reset/`,
          'POST',
          false,
          {email: this.passwordResetEmail},
          true
        )
        if (passwordResetReq.status === 200) {
          showAlert('success', 'Сброс пароля', 'На почту будет отправлено письмо с дальнейшими инструкциями')
          this.$refs.passwordResetDialog.close()
        } else {
          showAlert('error', 'Сброс пароля', 'Ошибка: указан некорректный email')
        }
        this.formLoading = false
      }
    },
    // Получение руководства пользователя
    async getManual() {
      this.formLoading = true
      const manualRequest = await apiRequest(
        `/backend/api/v1/docs/manual/`,
        'GET',
        false,
        null
      )
      if (manualRequest.file) {
        const linkSource = `data:application/vnd.openxmlformats-officedocument.wordprocessingml.document;base64,${manualRequest.file}`;
        const downloadLink = document.createElement('a');
        document.body.appendChild(downloadLink);
        downloadLink.href = linkSource;
        downloadLink.target = '_self';
        downloadLink.download = 'Инструкция.docx';
        downloadLink.click();
      } else {
        showAlert('error', 'Инструкция', 'Ошибка при получении файла инструкции')
      }
      this.formLoading = false
    }
  },
  watch: {
    phone: function(newValue) {
      if (['+7 (8', '+7 (7'].includes(newValue)) {this.phone = '+7 ('}
    },
  }
}
</script>

<style scoped>
  .login-background-img {
    opacity: 50%;
    background-image: url('../assets/img/login.jpg');
    position: absolute;
    left: 0;
    bottom: 0;
    width: 100vw;
    height: 100vh;
    background-position: left bottom;
    background-repeat: no-repeat;
  }

  .login-card {
    position: absolute;
    vertical-align: middle;
  }

  .login-card-text {
    width: 100%;
    background-color: white;
    padding: 0;
  }

  .login-tabs {
    width: 100%;
  }

  .login-radio-label {
    color: #373c59;
  }

  .login-form {
    width: 95%;
    padding-top: 10px;
    margin: 0 auto;
    text-align: center;
  }

  .login-button {
    margin: 0 auto;
  }

</style>
