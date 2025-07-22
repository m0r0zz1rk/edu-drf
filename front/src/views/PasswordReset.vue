<template>

  <div class="login-background-img adaptive-login-background-img"></div>
  <v-card class="login-card adaptive-login-card" variant="outlined">

    <v-card-title class="login-card-title">АИС "Учебный центр". Восстановление пароля</v-card-title>

    <v-card-text class="login-card-text adaptive-login-card-text">

      <div v-if="tokenValid === null">
        <b>Подождите, проверяем валидность токена для сброса пароля...</b>
      </div>

      <div v-else-if="tokenValid === false">
        <b>
          Полученный токен не валиден, возможно истек срок действия токена. Перейдите на форму входа и
          сформируйте запрос на смену пароля еще раз
        </b>
      </div>

      <div v-else class="login-form adaptive-login-form">
        <br/>
        <v-text-field
          v-model="password1"
          :append-inner-icon="passVisible1 ? 'mdi-eye-off' : 'mdi-eye'"
          :type="passVisible1 ? 'text' : 'password'"
          bg-color="white"
          label="Пароль"
          :rules="[rules.required, rules.password]"
          variant="solo"
          :loading="loading"
          @click:append-inner="passVisible1 = !passVisible1"
          clearable
        />
        <v-text-field
          v-model="password2"
          :append-inner-icon="passVisible2 ? 'mdi-eye-off' : 'mdi-eye'"
          :type="passVisible2 ? 'text' : 'password'"
          bg-color="white"
          label="Подтверждение"
          :rules="[rules.required, rules.password]"
          variant="solo"
          :loading="loading"
          @click:append-inner="passVisible2 = !passVisible2"
          clearable
        />
        <v-btn
          class="login-button adaptive-login-button"
          color="coko-blue"
          :loading="loading"
          type="submit"
          @click="passwordReset()"
          text="Изменить"
        />
      </div>
    </v-card-text>

  </v-card>
</template>

<script>
import {showAlert} from "@/commons/alerts";
import {apiRequest} from "@/commons/apiRequest";

export default {
  name: "PasswordReset",
  props: {
    usePreLoader: Function,
  },
  data() {
    return {
      // Первое поле для ввода нового пароля
      password1: '',
      // Отображение пароля в первом поле
      passVisible1: false,
      // Второе поле для ввода подтверждения пароля
      password2: '',
      // Отображение пароля во втором поле
      passVisible2: false,
      // Правила обработки полей
      rules: {
        required: value => !!value || 'Обязательно для заполнения.',
        password: value => value.length >= 8 || 'Минимальная длина пароля - 8 символов'
      },
      // Индикатор загрузки на элементах формы
      loading: false,
      // Индикатор валидности токена
      tokenValid: null
    }
  },
  methods: {
    // Выполнение проверки токена сброса пароля
    async tokenValidation() {
      const tokenValidationRequest = await apiRequest(
        `/backend/api/v1/password_reset/validate_token/`,
        'POST',
        false,
        {token: this.$route.query.token},
        true
      )
      this.tokenValid = tokenValidationRequest.status === 200
    },
    // Выполнение запроса на сброс пароля
    async passwordReset() {
      if (this.password1.length < 8 || this.password2.length < 8) {
        showAlert('error', 'Сброс пароля', 'Минимальная длина пароля - 8 символов')
        return
      }
      if (this.password1 !== this.password2) {
        showAlert('error', 'Сброс пароля', 'Введенные пароли не совпадают')
        return
      }
      if (confirm('Вы уверены, что хотите установить указанный пароль?')) {
        this.loading = true
        const passwordResetRequest = await apiRequest(
          `/backend/api/v1/password_reset/confirm/`,
          'POST',
          false,
          {token: this.$route.query.token, password: this.password1},
          true
        )
        if (passwordResetRequest.status === 200) {
          showAlert('success', 'Сброс пароля', 'Пароль успешно изменен')
          this.usePreLoader()
          this.$router.push('/login')
        } else {
          showAlert('error', 'Сброс пароля', 'Ошибка при смене пароля. Обратитесь к администратору')
        }
        this.loading = false
      }
    }
  },
  mounted() {
    this.usePreLoader(true)
    this.tokenValidation()
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

  .login-button {
    margin: 0 auto;
  }

  .login-form {
    width: 95%;
    padding-top: 10px;
    margin: 0 auto;
    text-align: center;
  }

</style>
