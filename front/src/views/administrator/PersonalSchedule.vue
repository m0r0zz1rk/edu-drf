<template>

  <LkPage :usePreLoader="usePreLoader">
    <slot>

      <v-card
          variant="outlined"
      >
        <v-card-text>

          <div
              style="background-color: white; overflow: auto;"
              class="adaptive-no-tab-table-card-text"
          >

            <b
                style="text-align: center"
            >
              Личное расписание
            </b>

            <b
                v-if="schedule === null"
            >
              Подождите, получаем расписание...
            </b>

            <v-expansion-panels
                v-if="schedule !== null"
                v-model="scheduleOpenedPanel"
                multiple
            >

              <v-expansion-panel
                  v-for="studyDay in schedule"
                  color="coko-blue"
              >

                <v-expansion-panel-title color="coko-blue">

                  <v-row
                      no-gutters
                  >

                    <v-col
                        cols="10"
                    >
                      {{studyDay.date}} ({{getDayOfWeek(studyDay.date)}})
                    </v-col>

                  </v-row>

                </v-expansion-panel-title>

                <v-expansion-panel-text>

                  <div
                      v-if="studyDay.lessons.length === 0"
                      style="text-align: center"
                  >
                    <b>Нет занятий</b>
                  </div>

                  <div
                      v-if="studyDay.lessons.length > 0"
                  >
                    <v-data-table
                        sticky
                        class="adaptive-schedule-table"
                        style="overflow: auto;"
                        :headers="headers"
                        :mobile-breakpoint="960"
                        :items="studyDay.lessons.sort((a, b) => convertTimeStrToSeconds(a.time_start_str) - convertTimeStrToSeconds(b.time_start_str))"
                        :loading="loading"
                        loading-text="Подождите, идет загрузка данных..."
                        hide-default-footer
                        :disable-pagination="true"
                    >

                      <template v-slot:headers="{ columns, isSorted, getSortIcon, toggleSort }">
                        <tr v-if="!(mobileDisplay)" style="position: sticky; top: 0; z-index: 5">
                          <template v-for="column in columns">
                            <td
                                style="
                                  text-align: center;
                                  background-color: #373c59;
                                  color: white;
                                "
                            >
                              <b>
                                {{column.title}}
                              </b>

                            </td>

                          </template>

                        </tr>

                        <tr v-if="mobileDisplay" style="position: sticky; top: 0; z-index: 5">

                        </tr>

                      </template>

                      <template v-slot:item="{ item, index }">

                        <tr
                            v-bind:class="{'v-data-table__tr v-data-table__tr--mobile': mobileDisplay}"
                        >

                          <template v-for="header in headers">

                            <td
                                style="text-align: center;"
                            >

                              <div v-if="mobileDisplay" class="v-data-table__td-title">

                                {{header.title}}

                              </div>

                              <template
                                  v-if="header.key === 'distance'"
                              >

                                <BooleanBadge
                                    v-if="header.key === 'distance'"
                                    :bool="item[header.key]"
                                />

                              </template>


                              <div
                                  v-if="header.key !== 'distance'"
                              >

                                {{item[header.key]}}

                              </div>

                            </td>

                          </template>

                        </tr>

                      </template>

                      <template v-slot:loading>
                        <v-skeleton-loader :type="'table-row@10'"></v-skeleton-loader>
                      </template>

                      <template v-slot:bottom></template>

                    </v-data-table>
                  </div>

                </v-expansion-panel-text>

              </v-expansion-panel>

            </v-expansion-panels>

          </div>

        </v-card-text>

      </v-card>

    </slot>
  </LkPage>

</template>

<script>

// Страница для просмотра личного расписания
import BooleanBadge from "@/components/badges/BooleanBadge.vue";
import ScheduleDayManage from "@/components/dialogs/edu/student_group/schedule/ScheduleDayManage.vue";
import {apiRequest} from "@/commons/api_request";
import {showAlert} from "@/commons/alerts";
import LkPage from "@/components/LkPage.vue";
import {getDayOfWeek} from "@/commons/date";
import {convertTimeStrToSeconds} from "@/commons/time";
import lessonTypes from "@/commons/consts/edu/lessonTypes";

export default {
  name: 'PersonalSchedule',
  components: {LkPage, ScheduleDayManage, BooleanBadge},
  props: {
    // Функция для показа или сокрытия анимации загрузки
    usePreLoader: Function,
  },
  data() {
    return {
      // Объект личного расписания
      schedule: null,
      // Открытые раскрывающиеся панели
      scheduleOpenedPanel: [],
      // URL адрес эндпоинта для получения личного расписания
      personalScheduleURL: '/backend/api/v1/admins/personal_schedule/',
      // Список заголовков таблицы для отображения учебных занятий
      headers: [
        {
          'title': 'Начало',
          'key': 'time_start_str'
        },
        {
          'title': 'Окончание',
          'key': 'time_end_str'
        },
        {
          'title': 'Учебная группа',
          'key': 'group_code'
        },
        {
          'title': 'Тип занятия',
          'key': 'type'
        },
        {
          'title': 'Тема',
          'key': 'lesson_theme'
        },
        {
          'title': 'Дистант',
          'key': 'distance'
        },
        {
          'title': 'Форма контроля',
          'key': 'control'
        },
      ]
    }
  },
  methods: {
    convertTimeStrToSeconds,
    getDayOfWeek,
    // Получение личного расписания
    async getPersonalSchedule() {
      let personalScheduleResponse = await apiRequest(
          this.personalScheduleURL,
          'GET',
          true,
          null
      )
      if (personalScheduleResponse.error) {
        showAlert('error', 'Личное расписание', personalScheduleResponse.error)
        return false
      } else {
        this.schedule = personalScheduleResponse
      }
    }
  },
  mounted() {
    this.getPersonalSchedule()
  }
}

</script>

<style scoped>

</style>