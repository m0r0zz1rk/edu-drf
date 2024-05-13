<template>
  <div class="login-background-img adaptive-login-background-img"></div>
  <v-card
    class="login-card adaptive-login-card"
    variant="outlined"
  >
    <v-card-title class="login-card-title">
      АИС "Учебный центр". Вход
    </v-card-title>
    <v-card-text class="login-card-text adaptive-login-card-text">
      <v-tabs class="login-tabs"
              v-model="loginTab"
              align-tabs="center"
              bg-color="coko-blue"
      >
        <v-tab class="coko-tab" value="student">Обучающийся</v-tab>
        <v-tab class="coko-tab" value="coko">Сотрудник центра</v-tab>
      </v-tabs>
      <v-tabs-window v-model="loginTab">
        <v-tabs-window-item value="student">
          <div class="login-form adaptive-login-form">
            <v-radio-group v-model="loginStudentType" inline>
              <v-radio color="coko-red" value="phone">
                <template v-slot:label>
                  <b class="login-radio-label">Телефон</b>
                </template>
              </v-radio>
              <v-radio class="login-student-radio-button" color="coko-red" value="email">
                <template v-slot:label>
                  <b class="login-radio-label">Почта</b>
                </template>
              </v-radio>
              <v-radio class="login-student-radio-button" color="coko-red" value="snils">
                <template v-slot:label>
                  <b class="login-radio-label">СНИЛС</b>
                </template>
              </v-radio>
            </v-radio-group>
            <v-form @submit.prevent="userLogin(false)">
              <v-text-field v-if="loginStudentType === 'phone'"
                            id="phoneTextField"
                            bg-color="white"
                            v-mask="'+7 (###) ###-##-##'"
                            :rules="[rules.required, rules.phone]"
                            label="Номер телефона"
                            variant="solo"
                            :loading="formLoading"
                            clearable>
              </v-text-field>
              <v-text-field v-if="loginStudentType === 'email'"
                            id="emailTextField"
                            bg-color="white"
                            label="Email"
                            :rules="[rules.required, rules.email]"
                            variant="solo"
                            :loading="formLoading"
                            clearable>
              </v-text-field>
              <v-text-field v-if="loginStudentType === 'snils'"
                            id="snilsTextField"
                            bg-color="white"
                            v-mask="'###-###-### ##'"
                            label="СНИЛС"
                            :rules="[rules.required, rules.snils]"
                            variant="solo"
                            :loading="formLoading"
                            clearable>
              </v-text-field>
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
              ></v-text-field>
              <v-btn
                class="login-button adaptive-login-button"
                color="coko-blue"
                :loading="formLoading"
                type="submit"
              >Войти</v-btn>
            </v-form>
            <RegistrationDialog ref="regDialog" :usePreLoader="usePreLoader" />
            <v-btn
              style="margin-top: 5px;"
              class="login-button adaptive-login-button"
              color="coko-blue"
              :loading="formLoading"
            >Инструкция</v-btn><br/>
            <v-btn
              style="margin-top: 5px;"
              class="login-button adaptive-login-button"
              color="coko-blue"
              :loading="formLoading"
            >Восстановить пароль</v-btn>
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
</template>

<script>
import {showAlert} from "@/commons/alerts";
import RegistrationDialog from "@/components/dialogs/RegistrationDialog.vue";
import {getUrlParameter} from "@/commons/get_url_parameter";

export default {
  name: 'Login',
  components: {RegistrationDialog},
  props: {
    usePreLoader: Function,
  },
  data() {
    return {
      loginTab: 'student',
      loginStudentType: 'email',
      passVisible: false,
      formLoading: false,
      rules: {
        required: value => !!value || 'Обязательно для заполнения.',
        phone: value => value.length === 18 || 'Некорректный номер телефона',
        snils: value => value.length === 14 || 'Некорректный СНИЛС',
        email: value => {
          const pattern = /^(([^<>()[\]\\.,;:\s@"]+(\.[^<>()[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/
          return pattern.test(value) || 'Некорректный e-mail.'
        },
      },
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
    }
  },
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
