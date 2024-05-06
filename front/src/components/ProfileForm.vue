<template>
  <v-card
    class="lk-full-page-card"
    color="coko-blue"
    title="Профиль пользователя"
  >
    <v-card-text>
      <div style="margin-top: 5px;">
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
              id="registrationName"
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
              id="registrationPatronymic"
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
              id="registrationPhone"
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
              id="registrationEmail"
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
              id="registrationSnils"
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
              id="registrationState"
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
              id="registrationBirthday"
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
              id="registrationSex"
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
              id="registrationHealth"
              bg-color="white"
              label="Ограничения по здоровью*"
              v-model="profileData['health']"
              :loading="formLoading"
              :rules="[rules.required,]"
              @update:modelValue="e => profileData['health'] = e"
              variant="solo"
            ></v-select>
          </v-col>

        </v-row>
        <small class="text-caption text-medium-emphasis">* - обязательные для заполнения поля</small>
      </div>

    </v-card-text>

    <v-card-actions style="background-color: white">
      <v-divider></v-divider>

      <v-btn
        color="coko-blue"
        text="Смена пароля"
        :loading="formLoading"
        @click="dialog = false"
      ></v-btn>

      <v-btn
        color="coko-blue"
        text="Сохранить"
        :loading="formLoading"
        @click="saveProfile()"
      ></v-btn>
    </v-card-actions>

  </v-card>
</template>

<script>
import {apiRequest} from "@/commons/api_request";
import {showAlert} from "@/commons/alerts";
import {convertBackendDate, convertDateToBackend} from "@/commons/date";
import email_pattern from "@/commons/email_pattern";

export default {
  name: "ProfileForm",
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
        'health': ''
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
      formLoading: false,
      pass1Visible: false,
      pass2Visible: false,
      registrationError: '',
      rules: {
        required: value => !!value || 'Обязательно для заполнения.',
        phone: value => value.length === 18 || 'Некорректный номер телефона',
        snils: value => value.length === 14 || 'Некорректный СНИЛС',
        email: value => email_pattern.test(value) || 'Некорректный e-mail.'
      },
      dataValid: false
    }
  },
  methods: {
    setData() {
      apiRequest(
        '/backend/api/v1/guides/states/',
        'GET',
        false,
        null,
      )
        .then((data) => {
          this.states = []
          data.map((state) => {
            this.states.push(state.name)
          })
          apiRequest(
            '/backend/api/v1/auth/get_profile/',
            'GET',
            true,
            null,
          )
            .then((data) => {
              if (data.error) {
                showAlert(
                  'error',
                  'Получение данных профиля',
                  data.error
                )
              } else {
                console.log(data)
                this.profileData = data
              }
            })
        })
    },
    checkValidData() {
      Object.keys(this.profileData).map((key) => {
        if (key === 'phone') {
          if (this.profileData[key] === null || this.profileData[key].length < 18) {
            showAlert(
              'error',
              'Валидация данных',
              'Введите корректный номер телефона'
            )
            this.dataValid = false
            return false
          }
        }
        if (key === 'email') {
          if (this.profileData[key] === null || !(email_pattern.test(this.profileData[key]))) {
            showAlert(
              'error',
              'Валидация данных',
              'Введите корректный email'
            )
            this.dataValid = false
            return false
          }
        }
        if (key === 'snils') {
          if (this.profileData[key] === null || this.profileData[key].length < 14) {
            showAlert(
              'error',
              'Валидация данных',
              'Введите корректный СНИЛС'
            )
            this.dataValid = false
            return false
          }
        }
        if (this.profileData[key] === null || this.profileData[key].length === 0) {
          showAlert(
            'error',
            'Валидация данных',
            'Заполните все обязательные поля формы'
          )
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
        let checkPhone = await apiRequest(
          '/backend/api/v1/auth/check_profile_phone/',
          'POST',
          true,
          {'phone': this.profileData['phone']},
          true
        )
        if (checkPhone.status !== 200) {
          let json = await checkPhone.json()
            showAlert(
              'error',
              'Проверка номера телефона',
              json.error
            )
            this.formLoading = false
            return false
        }
        let checkEmail = await apiRequest(
          '/backend/api/v1/auth/check_profile_email/',
          'POST',
          true,
          {'email': this.profileData['email']},
          true
        )
        if (checkEmail.status !== 200) {
          let json = await checkEmail.json()
          showAlert(
            'error',
            'Проверка email',
            json.error
          )
          this.formLoading = false
          return false
        }
        let checkSnils = await apiRequest(
          '/backend/api/v1/auth/check_profile_snils/',
          'POST',
          true,
          {'snils': this.profileData['snils']},
          true
        )
        if (checkSnils.status !== 200) {
          let json = await checkSnils.json()
          showAlert(
            'error',
            'Проверка СНИЛС',
            json.error
          )
          this.formLoading = false
          return false
        }
        let body = {}
        Object.keys(this.profileData).map((key) => {
          if (key === 'sex') {
            body[key] = this.profileData[key] === 'Мужской'
          } else if (key === 'health') {
            body[key]= this.profileData[key] === 'Да'
          } else if (key === 'birthday') {
            body[key] = convertDateToBackend(this.profileData[key])
          } else {
            body[key] = this.profileData[key]
          }
        })
        apiRequest(
          '/backend/api/v1/auth/save_profile/',
          'POST',
          true,
          body
        )
          .then((data) => {
            if (data.success) {
              showAlert(
                'success',
                'Изменение профиля',
                data.success
              )
            }
            if (data.error) {
              showAlert(
                'error',
                'Изменение профиля',
                data.error
              )
            }
            this.formLoading = false
          })

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
