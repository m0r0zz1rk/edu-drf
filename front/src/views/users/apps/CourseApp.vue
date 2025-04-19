<template>

  <div
      style="text-align: center"
      v-if="apps === null"
  >
    <b>Пожалуйста подождите...</b>
  </div>

  <div
      v-if="apps"
  >

    <v-expansion-panels
        style="padding-top: 5px"
        v-model="departmentsPanels"
        color="coko-blue"
        multiple
    >

      <v-expansion-panel
          v-for="dep in apps"
      >

        <v-expansion-panel-title
            color="coko-blue"
        >
          <div style="font-size: 18px">
            {{dep.department}}
          </div>
        </v-expansion-panel-title>

        <v-expansion-panel-text>

          <v-row
              dense
          >

            <v-col
                v-for="app in dep.apps"
                cols="12"
                md="3"
                sm="6"
            >

              <v-card
                  color="coko-blue"
                  @click="openApp(app.object_id)"
                  variant="tonal"
              >
                <v-card-title>

                  <div style="text-align: center">
                    {{app.group_code}}<br/>
                    <AppStatusBadge
                        :appStatus="app.status"
                    />
                  </div>

                </v-card-title>

                <v-card-text
                    class="internal-card-text"
                >
                  <div
                      style="color: black; text-align: center;"
                  >
                    <b>{{app.service_title}}</b>
                    <br/><br/>
                    Сроки обучения:<br/>
                    <b>{{app.service_date_range}}</b>
                    <br/>
                    Тип программы:<br/>
                    <b>{{app.service_type}}</b>

                  </div>

                </v-card-text>
              </v-card>

            </v-col>
          </v-row>

        </v-expansion-panel-text>

      </v-expansion-panel>

    </v-expansion-panels>

  </div>

</template>

<script>

// Форма для просмотра активных заявок на курсы
import {apiRequest} from "@/commons/apiRequest";
import {showAlert} from "@/commons/alerts";
import AppStatusBadge from "@/components/badges/students/AppStatusBadge.vue";

export default {
  name: 'CourseApp',
  props: {
    // Функция для показа анимации загрузки
    usePreLoader: Function,
  },
  components: {AppStatusBadge},
  data() {
    return {
      // Список подразделений с заявками
      apps: null,
      // Массив для открытых раскрывающихся панелей с заявками
      departmentsPanels: []
    }
  },
  methods: {
    // Получение списка заявок на курсы, сгруппированных по поздразделениям
    async getCourseApps() {
      let courseAppsRequest = await apiRequest(
          '/backend/api/v1/applications/course_application_user/',
          'GET',
          true,
          null
      )
      if (courseAppsRequest.error) {
        showAlert(
            'error',
            'Получение заявок',
            courseAppsRequest.error
        )
      } else {
        this.apps = courseAppsRequest
        for (let i=0;i<this.apps.length;i++) {
          this.departmentsPanels.push(i)
        }
      }
    },
    // Перейти на страницу заявки
    openApp(app_id) {
      this.usePreLoader()
      this.$router.push({
        path: '/student/app/course/'+app_id
      })
    }
  },
  mounted() {
    this.getCourseApps()
  }
}

</script>

<style scoped>

</style>
