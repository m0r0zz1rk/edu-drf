<template>
  <v-row>
    <v-col
      cols="12"
      md="6"
      sm="12"
    >
      <v-card
        variant="outlined"
      >
        <v-card-title
          class="login-card-title"
        >
          Личные данные
        </v-card-title>
        <v-card-text style="background-color: white">
          <div style="background-color: white"
               class="adaptive-main-card-text-height">
            <div v-if="Object.keys(profileInfo).length > 0">
              <b>ФИО:</b><br/>
              {{ profileInfo.fio }}<br/><br/>
              <b>Телефон:</b><br/>
              {{ profileInfo.phone }}<br/><br/>
              <b>Email:</b><br/>
              {{ profileInfo.email }}<br/><br/>
              <b>СНИЛС:</b><br/>
              {{ profileInfo.snils }}<br/><br/>
            </div>

            <div style="width: 100%; text-align: center">
              <v-btn
                style="margin: 0 auto"
                color="coko-blue"
                prepend-icon="mdi-account-box-outline"
                @click="$router.push('/profile')"
              >Перейти в профиль</v-btn>
            </div>
          </div>
        </v-card-text>
      </v-card>

    </v-col>

    <v-col
      cols="12"
      md="6"
      sm="12"
    >
      <v-card
        variant="outlined"
        class="adaptive-main-card-height"
      >
        <v-card-title
          class="login-card-title"
        >
          Активные заявки
        </v-card-title>
        <v-card-text
          style="background-color: white"
        >
          <div style="background-color: white"
               class="adaptive-main-card-text-height">
            <v-list >
              <template v-for="app in lastActiveApps">
                <v-list-item :title="app.name">
                  <template v-slot:subtitle>
                    <AppTypeBadge :appType="app.app_type" />
                    <AppStatusBadge :appStatus="app.status" />
                  </template>

                  <template v-slot:append>
                    <v-btn
                      icon="mdi-chevron-right"
                      variant="text"
                      @click="goToApp(app.app_type, app.object_id)"
                    />
                  </template>
                </v-list-item>
                <v-divider inset></v-divider>
              </template>

            </v-list>
          </div>

        </v-card-text>
      </v-card>
    </v-col>
  </v-row>

  <MailingDialog
    ref="mailingDialog"
    :phoneMailing="phoneMailing"
    :emailMailing="emailMailing"
    :showMainButton="false"
    :setMailingByEmail="(val) => {console.log(val); emailMailing = val}"
    :setMailingByPhone="(val) => {console.log(val); phoneMailing = val}"
    :onMailingClose="mailingSave"
  />

</template>

<script>
import {apiRequest} from "@/commons/apiRequest";
import {showAlert} from "@/commons/alerts";
import AppStatusBadge from "@/components/badges/students/AppStatusBadge.vue";
import AppTypeBadge from "@/components/badges/students/AppTypeBadge.vue";
import MailingDialog from "@/components/dialogs/authen/MailingDialog.vue";

export default {
  name: "StudentMainPage",
  components: {MailingDialog, AppTypeBadge, AppStatusBadge},
  data() {
    return {
      lastActiveApps: [],
      profileInfo: {},
      // Рассылка по Email
      emailMailing: true,
      // Рассылка по телефону
      phoneMailing: true,
    }
  },
  methods: {
    getProfileInfo() {
      apiRequest(
        '/backend/api/v1/auth/student_main_page_info',
        'GET',
        true,
        false
      )
        .then((data) => {
          if (data.error) {
            showAlert(
              'error',
              'Получение данных профиля',
              data.error
            )
          } else {
            this.profileInfo = data
            this.lastActiveApps = data.active_apps
            if (data.need_mailing) {
              this.$refs.mailingDialog.openMailingDialog()
            }
          }
        })
    },
    // Переход к заявке
    goToApp(type, object_id) {
      this.$router.push(`/student/app/${type}/${object_id}`)
    },
    // Сохранение информации о рассылке
    mailingSave() {
      apiRequest(
          '/backend/api/v1/auth/mailing/',
          'POST',
          true,
          {'email_mailing': this.emailMailing, 'phone_mailing': this.phoneMailing}
      )
          .then((data) => {
            if (data.success) {
              showAlert('success', 'Согласие на рассылку', data.success)
            } else {
              showAlert('error', 'Согласие на рассылку', data.error)
            }
          })
    }
  },
  mounted() {
    this.getProfileInfo()
  }
}
</script>

<style scoped>

</style>
