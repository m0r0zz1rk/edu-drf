<template>

  <LkPage :usePreLoader="usePreLoader">
    <slot>
      <v-card
          color="coko-blue"
          class="lk-full-page-card"
          title="Курсы (ОУ)"
      >
        <v-card-text>

            <template
                style="text-align: center"
                v-if="!courses"
            >
              <b>Пожалуйста подождите...</b>
            </template>

            <template
              v-if="courses"
            >

              <v-expansion-panels
                  style="padding-top: 5px"
                  v-model="departmentsPanels"
                  color="coko-blue"
                  multiple
              >

                <v-expansion-panel
                  v-for="dep in courses"
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
                          v-for="course in dep.services"
                          cols="12"
                          md="3"
                          sm="6"
                      >

                        <v-card
                            color="coko-blue"
                            @click="openCourseDetailDialog(course, dep.department)"
                            variant="tonal"
                        >
                          <v-card-title>
                            <div style="text-align: center">
                              {{course.code}}
                            </div>

                          </v-card-title>

                          <v-card-text
                            class="internal-card-text"
                          >
                            <div
                              style="color: black; text-align: center;"
                            >

                              <b>{{course.title}}</b>
                              <br/><br/>
                              Сроки обучения:<br/>
                              <b>{{course.date_start}}-{{course.date_end}}</b>
                              <br/>
                              Куратор:<br/>
                              <b>{{course.curator_fio}}</b>

                            </div>

                          </v-card-text>
                        </v-card>

                      </v-col>
                    </v-row>

                  </v-expansion-panel-text>

                </v-expansion-panel>

              </v-expansion-panels>

            </template>

        </v-card-text>

        <v-spacer></v-spacer>

      </v-card>
    </slot>
  </LkPage>

  <ServiceDetail
    ref="courseDetail"
    serviceType="course"
    :serviceInfo="selectedCourse"
    :department="courseDep"
  />

</template>

<script>

// Компонент для просмотра доступных курсов для регистрации
import LkPage from "@/components/LkPage.vue";
import {apiRequest} from "@/commons/api_request";
import {showAlert} from "@/commons/alerts";
import ServiceDetail from "@/components/dialogs/students/service/ServiceDetail.vue";

export default {
  name: 'Courses',
  components: {ServiceDetail, LkPage},
  props: {
    // Функция для отображения/скрытия анимации загрузки на странице
    usePreLoader: Function,
  },
  data() {
    return {
      // Параметр отображения загрузки на элементах формы
      loading: true,
      // Список курсов, сгруппированных по подразделениям
      courses: null,
      // Список открытых панелей с курсами департаментов
      departmentsPanels: [],
      // Выбранный курс
      selectedCourse: null,
      // Подразделение выбранного курса
      courseDep: ''
    }
  },
  methods: {
    // Открыть диалоговое окно с детальной инфомрацией по курсу
    openCourseDetailDialog(course, dep) {
      this.selectedCourse = course
      this.courseDep = dep
      this.$refs.courseDetail.openDialog()

    },
    // Получение курсов, сгруппированных по подразделениям
    async getCourses() {
      let coursesRequest = await apiRequest(
          '/backend/api/v1/users/courses/',
          'GET',
          true,
          null
      )
      if (coursesRequest.error) {
        showAlert(
            'error',
            'Курсы',
            coursesRequest.error
        )
      } else {
        this.courses = coursesRequest.success
        for (let i=0;i<this.courses.length;i++) {
          this.departmentsPanels.push(i)
        }
        coursesRequest.success.map((dep) => {
          this.departmentsPanels.push(dep.department)
        })
      }
      this.loading = false
    }
  },
  mounted() {
    this.getCourses()
  }
}

</script>

<style scoped>

</style>