<template>
  <LkPage ref="lkPage" :usePreLoader="usePreLoader">
    <slot>
      <v-row dense>
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
                  <template v-for="app in lastActivePass">
                    <v-list-item
                       :title="app.event_name"
                    >
                      <template v-slot:subtitle>
                        {{app.status}}
                      </template>

                      <template v-slot:append>
                        <v-btn
                          icon="mdi-chevron-right"
                          variant="text"
                        ></v-btn>
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
    </slot>
  </LkPage>

</template>

<script>

import LkPage from "@/components/LkPage.vue";
import {apiRequest} from "@/commons/api_request";
import {showAlert} from "@/commons/alerts";

export default {
  name: 'Main',
  components: {LkPage},
  props: {
    usePreLoader: Function,
  },
  data() {
    return {
      lastActivePass: [
        {
          'object_id': 1,
          'event_name': 'Первое мероприятие',
          'status': 'На проверке'
        },
        {
          'object_id': 2,
          'event_name': 'Второй курс',
          'status': 'Подтверждена'
        }
      ],
      profileInfo: {}
    }
  },
  methods: {
    getProfileInfo() {
      apiRequest(
        '/backend/api/v1/auth/main_page_info',
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
          }
        })
    }
  },
  mounted() {
    this.getProfileInfo()
    this.usePreLoader(true)
  }
}

</script>

<style scoped>

</style>
