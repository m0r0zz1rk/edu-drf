<template>

  <CokoDialog
    ref="registrationDialog"
    :cardActions="true"
  >

    <template v-slot:title>
      Регистрация обучающегося
    </template>

    <template v-slot:text>

      <DialogContentWithError ref="content-error">

        <slot>

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
                  variant="solo"
              ></v-select>
            </v-col>

            <v-col
                cols="12"
                md="4"
                sm="6"
            >
              <v-date-input
                  id="registrationBirthday"
                  v-mask="'##.##.####'"
                  bg-color="white"
                  :rules="[rules.required,]"
                  label="Дата рождения*"
                  prepend-icon=""
                  prepend-inner-icon="$calendar"
                  variant="solo"
                  :loading="formLoading"
                  clearable
              />
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
                  id="registrationHealth"
                  bg-color="white"
                  label="Ограничения по здоровью*"
                  :loading="formLoading"
                  :rules="[rules.required,]"
                  variant="solo"
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
                  :rules="[rules.required, rules.password]"
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
                  :rules="[rules.required, rules.password]"
                  variant="solo"
                  @click:append-inner="pass2Visible = !pass2Visible"
                  :loading="formLoading"
                  clearable
              ></v-text-field>
            </v-col>
          </v-row>

          <v-btn
              color="coko-blue"
              @click="$refs.agreementDialog.dialog = true"
          >Согласие на обработку ПДн</v-btn><br/>

          <CokoDialog
            ref="agreementDialog"
          >

            <template v-slot:title>
              Согласие на обработку ПДН
            </template>

            <template v-slot:text>
              <p>
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

          </CokoDialog>

        </slot>

      </DialogContentWithError>

      <small class="text-caption text-medium-emphasis">* - обязательные для заполнения поля</small>

    </template>

    <template v-slot:actions>

      <v-btn
          color="coko-blue"
          text="Регистрация"
          @click="registration()"
      ></v-btn>

    </template>

  </CokoDialog>
</template>

<script>

import {apiRequest} from "@/commons/apiRequest";
import {showAlert} from "@/commons/alerts";
import emailPattern from "@/commons/emailPattern";
import DialogContentWithError from "@/components/dialogs/DialogContentWithError.vue";
import {useDisplay} from "vuetify";
import CokoDialog from "@/components/dialogs/CokoDialog.vue";

export default {
  name: 'RegistrationDialog',
  components: {CokoDialog, DialogContentWithError},
  props: {
    usePreLoader: Function
  },
  data() {
    return {
      // Проверка на мобильное устройство
      mobileDisplay: useDisplay().smAndDown,
      dialog: false,
      uniqFailed: false,
      uniqueData: [
        {
          attr: 'phone',
          alias: 'номером телефона',
        },
        {
          attr: 'email',
          alias: 'email',
        },
        {
          attr: 'snils',
          alias: 'СНИЛС',
        },
      ],
      formLoading: false,
      pass1Visible: false,
      pass2Visible: false,
      rules: {
        required: value => !!value || 'Обязательно для заполнения.',
        phone: value => value.length === 18 || 'Некорректный номер телефона',
        snils: value => value.length === 14 || 'Некорректный СНИЛС',
        email: value => emailPattern.test(value) || 'Некорректный e-mail.',
        password: value => value.length >= 8 || 'Минимальная длина пароля - 8 символов'
      },
      states: ['Россия', 'Украина', 'Беларусь', 'Казахстан'],
      sex: ['Мужской', 'Женский'],
      health: ['Да', 'Нет'],
      agreementCheckbox: false
    }
  },
  methods: {
    // Отркыть диалоговое окно
    openDialog() {
      this.$refs.registrationDialog.dialog = true
    },
    async getStates() {
      apiRequest(
        '/backend/api/v1/guides/state/',
        'GET',
        false,
        null,
      )
        .then((data) => {
          this.states = []
          data.map((state) => {
            this.states.push(state.name)
          })
          this.usePreLoader()
        })
    },
    verifyData() {
      let surname = document.querySelector('#registrationSurname').value
      if (surname.length === 0) {
        this.$refs["content-error"].showContentError('Заполните поле "Фамилия"')
        return null
      }
      let name = document.querySelector('#registrationName').value
      if (name.length === 0) {
        this.$refs["content-error"].showContentError('Заполните поле "Имя"')
        return null
      }
      let patronymic = document.querySelector('#registrationPatronymic').value
      let phone = document.querySelector('#registrationPhone').value
      if (phone.length !== 18) {
        this.$refs["content-error"].showContentError('Задан некорректный номер телефона')
        return null
      }
      let email = document.querySelector('#registrationEmail').value
      if (email.value === 0) {
        this.$refs["content-error"].showContentError('Задан некорректный номер телефона')
        return null
      }
      if (!(emailPattern.test(email))) {
        this.$refs["content-error"].showContentError('Задан некорректный email')
        return null
      }
      let snils = document.querySelector('#registrationSnils').value
      if (snils.length !== 14) {
        this.$refs["content-error"].showContentError('Задан некорректный СНИЛС')
        return null
      }
      let state = document.querySelector('#registrationState')._value
      if (state.length === 0) {
        this.$refs["content-error"].showContentError('Выберите государство')
        return null
      }
      let birthday = document.querySelector('#registrationBirthday').value
      if (birthday.length === 0) {
        this.$refs["content-error"].showContentError('Выберите дату рождения')
        return null
      }
      let sex = document.querySelector('#registrationSex')._value
      if (sex.length === 0) {
        this.$refs["content-error"].showContentError('Выберите пол')
        return null
      }
      let health = document.querySelector('#registrationHealth')._value
      if (health.length === 0) {
        this.$refs["content-error"].showContentError('Укажите, есть ли у Вас ограничения по здоровью')
        return null
      }
      let password = document.querySelector('#registrationPass1').value
      let confirm = document.querySelector('#registrationPass2').value
      if ((password.length < 8) || (confirm.length < 8)) {
        this.$refs["content-error"].showContentError('Минимальная длина пароля - 8 символов')
        return null
      }
      if (password !== confirm) {
        this.$refs["content-error"].showContentError('Введенные пароли не совпадают')
        return null
      }
      if (!(this.agreementCheckbox)) {
        this.$refs["content-error"].showContentError('Дайте согласие на обработку ПДн')
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
    async registration() {
      this.formLoading = true
      this.$refs["content-error"].hideContentError()
      this.uniqFailed = false
      let regData = this.verifyData()
      if (regData !== null) {
        for (let i=0;i<this.uniqueData.length;i++) {
          let obj = this.uniqueData[i]
          if (!(this.uniqFailed)) {
            let body = {}
            body[obj.attr] = regData[obj.attr]
            let uniqResp = await apiRequest(
              '/backend/api/v1/auth/check_'+obj.attr+'/',
              'POST',
              false,
              body,
              true
            )
            if (uniqResp.status === 406) {
              this.uniqFailed = true
              this.$refs["content-error"].showContentError('Пользователь с указанным '+obj.alias+' уже существует')
            }
          }
        }
        if (!(this.uniqFailed)) {
          apiRequest(
            '/backend/api/v1/auth/registration/',
            'POST',
            false,
            regData
          )
            .then((data) => {
              if (data.success) {
                this.dialog = false
                showAlert(
                  'success',
                  'Регистрация обучающегося',
                  data.success
                )
                this.$refs.registrationDialog.dialog = false
              } else {
                showAlert(
                  'error',
                  'Регистрация обучающегося',
                  data.error
                )
              }
              this.formLoading = false
              return false
            })
        } else {
          this.formLoading = false
        }
      }
      else {
        // Прокрутить блок страницы вверх
        this.$refs.registrationDialog.scrollTextToTop()
        this.formLoading = false
      }
    }
  },
  mounted() {
    this.getStates()
  },
  watch: {
    agreementCheckbox: function(newValue) {
      if (newValue)  { this.$refs.agreementDialog.close() }
    }
  }
}

</script>

<style scoped>

</style>
