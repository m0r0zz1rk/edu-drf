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
          Информация о пользователе
        </v-card-title>
        <v-card-text>
          <v-skeleton-loader
            v-if="loading"
            type="paragraph"
          />
          <div
              v-if="!(loading)"
              style="background-color: white"
              class="adaptive-main-card-text-height"
          >
            <b>Пользователь:</b><br/>
            {{ mainPageInfo['user_info']['display_name'] }}<br/><br/>
            <b>Роль:</b><br/>
            {{ userRole }}<br/><br/>
            <b>Подразделение:</b><br/>
            {{ mainPageInfo['user_info']['dep'] }}<br/><br/>
            <b>Дата регистрации в АИС:</b><br/>
            {{ mainPageInfo['user_info']['first_login'] }}<br/><br/>
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
        v-if="userRole === 'Администратор'"
        variant="outlined"
        class="adaptive-main-card-height"
      >
        <v-card-title
          class="login-card-title"
        >
          Учебный процесс
        </v-card-title>
        <v-card-text>
          <v-skeleton-loader
              v-if="loading"
              type="paragraph"
          />
          <div
              v-if="!(loading)"
              style="background-color: white"
              class="adaptive-main-card-text-height"
          >
            <b>Пользователей в АИС:</b><br/>
            {{ mainPageInfo['study_info']['user_count'] }}<br/><br/>
            <b>Заявок в АИС:</b><br/>
            {{ mainPageInfo['study_info']['app_count'] }}<br/><br/>
            <b>Курсов (ОУ) в АИС:</b><br/>
            {{ mainPageInfo['study_info']['course_count'] }}<br/><br/>
            <b>Мероприятий (ИКУ) в АИС:</b><br/>
            {{ mainPageInfo['study_info']['event_count'] }}<br/><br/>
          </div>
        </v-card-text>
      </v-card>
    </v-col>

<!--    <v-col-->
<!--      cols="12"-->
<!--      md="6"-->
<!--      sm="12"-->
<!--    >-->
<!--      <v-card-->
<!--        v-if="userRole === 'Администратор'"-->
<!--        variant="outlined"-->
<!--        class="adaptive-main-card-height"-->
<!--      >-->
<!--        <v-card-title-->
<!--          class="login-card-title"-->
<!--        >-->
<!--          Последние заявки (Тест)-->
<!--        </v-card-title>-->
<!--        <v-card-text>-->
<!--          <v-skeleton-loader-->
<!--              v-if="loading"-->
<!--              type="paragraph"-->
<!--          />-->
<!--          <div-->
<!--              v-if="!(loading)"-->
<!--              style="background-color: white"-->
<!--              class="adaptive-main-card-text-height"-->
<!--          >-->
<!--            <v-list >-->
<!--              <template v-for="app in mainPageInfo['last_apps']">-->
<!--                <v-list-item-->
<!--                >-->
<!--                  <v-list-item-title>-->
<!--                    {{app.user}}<br/>-->
<!--                    {{app.event_name}}-->
<!--                  </v-list-item-title>-->
<!--                  <template v-slot:subtitle>-->
<!--                    {{app.status}}-->
<!--                  </template>-->

<!--                  <template v-slot:append>-->
<!--                    <v-btn-->
<!--                      icon="mdi-chevron-right"-->
<!--                      variant="text"-->
<!--                    ></v-btn>-->
<!--                  </template>-->
<!--                </v-list-item>-->
<!--                <v-divider inset></v-divider>-->
<!--              </template>-->

<!--            </v-list>-->
<!--          </div>-->
<!--        </v-card-text>-->
<!--      </v-card>-->
<!--    </v-col>-->

  </v-row>
</template>

<script>
import {apiRequest} from "@/commons/apiRequest";
import {showAlert} from "@/commons/alerts";
import {getCookie} from "@/commons/cookie";

export default {
  name: "CentreMainPage",
  data() {
    return {
      // Роль пользователя
      userRole: getCookie('cokoRole') === 'centre' ? 'Администратор' : 'Сотрудник центра',
      mainPageInfo: {
        'user_info': {
          'display_name': 'Фамилия Имя Отчество',
          'dep': '-',
          'first_login': new Date(2000, 1, 1)
        },
        'study_info': {
          'user_count': 0,
          'app_count': 0,
          'course_count': 0,
          'event_count': 0
        },
        'last_apps': [
          {
            'user': 'Фамилия Имя Отчетство',
            'event_name': 'Мероприятие',
            'status': 'Статус'
          }
        ]
      },
      // Параметр отображения загрузки данных для формы
      loading: true
    }
  },
  methods: {
    async getMainPageInfo() {
      let mainPageRequest = await apiRequest(
        '/backend/api/v1/admins/main_page_info',
        'GET',
        true,
        false
      )
      if (mainPageRequest.error) {
        showAlert(
          'error',
          'Получение данных для главной страницы',
          mainPageRequest.error
        )
      } else {
        this.mainPageInfo = mainPageRequest
        this.loading = false
      }
    }
  },
  mounted() {
    this.getMainPageInfo()
  },
}
</script>

<style scoped>

</style>
