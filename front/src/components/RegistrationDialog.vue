<template>
  <v-dialog
    v-model="dialog"
    class="adaptive-registration-dialog"
    persistent
  >
    <template v-slot:activator="{ props: activatorProps }">
      <v-btn
        style="margin-top: 5px;"
        class="login-button adaptive-login-button"
        color="coko-blue"
        text="Регистрация"
        v-bind="activatorProps"
        :loading="formLoading"
      ></v-btn>
    </template>

    <v-card>
      <v-card-title class="registration-card-title">
        Регистрация обучающегося
      </v-card-title>
      <v-card-text>
        <v-row dense>
          <v-col
            cols="12"
            md="4"
            sm="6"
          >
            <v-text-field
              id="registrationSurname"
              bg-color="white"
              label="Фамилия*"
              :rules="[rules.required,]"
              variant="solo"
              :loading="formLoading"
              clearable
            ></v-text-field>
          </v-col>

          <v-col
            cols="12"
            md="4"
            sm="6"
          >
            <v-text-field
              id="registrationName"
              bg-color="white"
              label="Имя*"
              :rules="[rules.required,]"
              variant="solo"
              :loading="formLoading"
              clearable
            ></v-text-field>
          </v-col>

          <v-col
            cols="12"
            md="4"
            sm="6"
          >
            <v-text-field
              id="registrationPatronymic"
              bg-color="white"
              label="Отчество"
              variant="solo"
              :loading="formLoading"
              clearable
            ></v-text-field>
          </v-col>

          <v-col
            cols="12"
            md="4"
            sm="6"
          >
            <v-text-field
              id="registrationPhone"
              bg-color="white"
              v-mask="'+7 (###) ###-##-##'"
              :rules="[rules.required, rules.phone]"
              label="Номер телефона*"
              variant="solo"
              :loading="formLoading"
              clearable
            ></v-text-field>
          </v-col>

          <v-col
            cols="12"
            md="4"
            sm="6"
          >
            <v-text-field
              id="registrationEmail"
              bg-color="white"
              :rules="[rules.required, rules.email]"
              label="Электронная почта*"
              variant="solo"
              :loading="formLoading"
              clearable
            ></v-text-field>
          </v-col>

          <v-col
            cols="12"
            md="4"
            sm="6"
          >
            <v-text-field
              id="registrationSnils"
              bg-color="white"
              v-mask="'###-###-### ##'"
              :rules="[rules.required, rules.snils]"
              label="СНИЛС*"
              variant="solo"
              :loading="formLoading"
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
              id="registrationState"
              bg-color="white"
              label="Государство*"
              :loading="formLoading"
              :rules="[rules.required,]"
            ></v-select>
          </v-col>

          <v-col
            cols="12"
            md="4"
            sm="6"
          >
            <v-date-input
              id="registrationBirthday"
              bg-color="white"
              :rules="[rules.required,]"
              label="Дата рождения*"
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
              id="registrationSex"
              bg-color="white"
              label="Пол*"
              :loading="formLoading"
              :rules="[rules.required,]"
            ></v-select>
          </v-col>

          <v-col
            cols="12"
            md="4"
            sm="6"
          >
            <v-select
              :items="health"
              id="registrationHealth"
              bg-color="white"
              label="Ограничения по здоровью*"
              :loading="formLoading"
              :rules="[rules.required,]"
            ></v-select>
          </v-col>

          <v-col
            cols="12"
            md="4"
            sm="6"
          >
            <v-text-field
              id="registrationPass1"
              :append-inner-icon="pass1Visible ? 'mdi-eye-off' : 'mdi-eye'"
              :type="pass1Visible ? 'text' : 'password'"
              bg-color="white"
              label="Пароль*"
              :rules="[rules.required,]"
              variant="solo"
              @click:append-inner="pass1Visible = !pass1Visible"
              :loading="formLoading"
              clearable
            ></v-text-field>
          </v-col>

          <v-col
            cols="12"
            md="4"
            sm="6"
          >
            <v-text-field
              id="registrationPass2"
              :append-inner-icon="pass2Visible ? 'mdi-eye-off' : 'mdi-eye'"
              :type="pass2Visible ? 'text' : 'password'"
              bg-color="white"
              label="Подтверждение пароля*"
              :rules="[rules.required,]"
              variant="solo"
              @click:append-inner="pass2Visible = !pass2Visible"
              :loading="formLoading"
              clearable
            ></v-text-field>
          </v-col>
        </v-row>

        <v-btn
          color="coko-blue"
          @click="agreementDialog = true"
        >Согласие на обработку ПДн</v-btn><br/>
        <v-dialog v-model="agreementDialog">
          <v-card>
            <template v-slot:text>
              <p style="text-align: justify">
                Нажимая кнопку «Регистрация» я даю свое согласие Государственному автономному учреждению
                Иркутской области «Центр оценки профессионального мастерства, квалификаций педагогов и мониторинга
                качества образования» (далее - ГАУ ИО «ЦОПМКиМКО»), адрес местонахождения: 664023, Иркутская область,
                город Иркутск, улица Лыткина, дом 75 «а» , на обработку моих персональных данных в автоматизированной
                информационной системе "Учебный центр" (далее - АИС) в целях регистрации и использования АИС
                в образовательных целях.<br/>
                Перечень обрабатываемых персональных данных, передаваемых в АИС:<br/>
                - Фамилия, имя, отчество;<br/>
                - Телефон;<br/>
                - Адрес электронной почты;<br/>
                - СНИЛС.<br/>
                Настоящее согласие, выданное мной ГАУ ИО "ЦОПМКиМКО", действует до момента удаления моей учетной записи
                в АИС, либо до момента прекращения ГАУ ИО "ЦОПМКиМКО" эксплуатации АИС, если иное не предусмотрено
                законодательством Российской Федерации.<br/>
                Я уведомлен(а), что вправе отозвать настоящее согласие, выданное мной ГАУ ИО "ЦОПМКиМКО" путем
                направления мною либо моим представителем соответствующего письменного запроса (заявления) в ГАУ ИО
                «ЦОПМКиМКО» по адресу: 664023, Иркутская область, город Иркутск, улица Лыткина, дом 75 «а».<br/>
                Под обработкой персональных данных в целях выдачи настоящего согласия ГАУ ИО "ЦОПМКиМКО" понимается
                любое действие (операция) или совокупность действий (операций), совершаемых с использованием средств
                автоматизации или без использования таких средств с персональными данными, включая сбор, запись,
                систематизацию, накопление, хранение, уточнение (обновление, изменение), извлечение, использование,
                обезличивание, блокирование, удаление, уничтожение персональных данных.
              </p>
              <v-checkbox v-model="agreementCheckbox">
                <template v-slot:label>
                  <div>
                    Я даю свое согласие на обработку персональных данных*
                  </div>
                </template>
              </v-checkbox>
            </template>
          </v-card>

        </v-dialog>
        <small class="text-caption text-medium-emphasis">* - обязательные для заполнения поля</small>
        <v-alert
          id="error-registration-alert"
          class="alert-hidden"
          style="width: 100%"
          :text="registrationError"
          type="error"
        ></v-alert>
      </v-card-text>

      <v-divider></v-divider>

      <v-card-actions>
        <v-spacer></v-spacer>

        <v-btn
          text="Отмена"
          @click="dialog = false"
        ></v-btn>

        <v-btn
          color="coko-blue"
          text="Регистрация"
          @click="registration()"
        ></v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<script>

import {apiRequest} from "@/commons/api_request";

export default {
  name: 'RegistrationDialog',
  data() {
    return {
      agreementDialog: false,
      dialog: false,
      formLoading: false,
      pass1Visible: false,
      pass2Visible: false,
      registrationError: '',
      rules: {
        required: value => !!value || 'Обязательно для заполнения.',
        phone: value => value.length === 18 || 'Некорректный номер телефона',
        snils: value => value.length === 14 || 'Некорректный СНИЛС',
        email: value => {
          const pattern = /^(([^<>()[\]\\.,;:\s@"]+(\.[^<>()[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/
          return pattern.test(value) || 'Некорректный e-mail.'
        },
      },
      states: ['Россия', 'Украина', 'Беларусь', 'Казахстан'],
      sex: ['Мужской', 'Женский'],
      health: ['Да', 'Нет'],
      agreementCheckbox: false
    }
  },
  methods: {
    async getStates() {
      apiRequest(
        '/backend/api/v1/guides/states',
        'GET',
        false,
        null,
      )
        .then((data) => {
          this.states = []
          data.map((state) => {
            this.states.push(state.name)
          })
        })
    },
    hideRegError() {
      document.querySelector('#error-registration-alert').classList.remove('alert-visible')
      document.querySelector('#error-registration-alert').classList.add('alert-hidden')
    },
    showRegError(message) {
      this.registrationError = message
      document.querySelector('#error-registration-alert').classList.add('alert-visible')
      document.querySelector('#error-registration-alert').classList.remove('alert-hidden')
    },
    verifyData() {
      let surname = document.querySelector('#registrationSurname').value
      if (surname.length === 0) {
        this.showRegError('Заполните поле "Фамилия"')
        return null
      }
      let name = document.querySelector('#registrationName').value
      if (name.length === 0) {
        this.showRegError('Заполните поле "Имя"')
        return null
      }
      let patronymic = document.querySelector('#registrationPatronymic').value
      let phone = document.querySelector('#registrationPhone').value
      if (phone.length !== 18) {
        this.showRegError('Задан некорректный номер телефона')
        return null
      }
      let email = document.querySelector('#registrationEmail').value
      if (email.value === 0) {
        this.showRegError('Задан некорректный номер телефона')
        return null
      }
      const pattern = /^(([^<>()[\]\\.,;:\s@"]+(\.[^<>()[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/
      if (!(pattern.test(email))) {
        this.showRegError('Задан некорректный email')
        return null
      }
      let snils = document.querySelector('#registrationSnils').value
      if (snils.length !== 14) {
        this.showRegError('Задан некорректный СНИЛС')
        return null
      }
      let state = document.querySelector('#registrationState')._value
      if (state.length === 0) {
        this.showRegError('Выберите государство')
        return null
      }
      let birthday = document.querySelector('#registrationBirthday').value
      if (birthday.length === 0) {
        this.showRegError('Выберите дату рождения')
        return null
      }
      let sex = document.querySelector('#registrationSex')._value
      if (sex.length === 0) {
        this.showRegError('Выберите пол')
        return null
      }
      let health = document.querySelector('#registrationHealth')._value
      if (health.length === 0) {
        this.showRegError('Укажите, есть ли у Вас ограничения по здоровью')
        return null
      }
      let password = document.querySelector('#registrationPass1').value
      let confirm = document.querySelector('#registrationPass2').value
      if ((password.length < 8) || (confirm.length < 8)) {
        this.showRegError('Минимальная длина пароля - 8 символов')
        return null
      }
      if (password !== confirm) {
        this.showRegError('Введенные пароли не совпадают')
        return null
      }
      if (!(this.agreementCheckbox)) {
        this.showRegError('Дайте согласие на обработку ПДн')
        return null
      }
      return {
        'surname': surname,
        'name': name,
        'patronymic': patronymic,
        'phone': phone,
        'email': email,
        'snils': snils,
        'state': state,
        'birthday': birthday,
        'sex': sex === 'Мужской',
        'health': health === 'Да',
        'password': password
      }
    },
    registration() {
      this.hideRegError()
      let regData = this.verifyData()
      if (regData !== null) {
        return true
      }
    }
  },
  mounted() {
    this.getStates()
  }
}

</script>

<style scoped>
  .registration-card-title {
    background-color: #373c59;
    color: white;
  }

  .alert-visible {
    z-index: 100;
  }

  .alert-hidden {
    display: none;
    z-index: 0;
  }

</style>
