<template>

  <div
    style="padding: 10px; width: 98%"
  >

    <div v-if="schedule === null">
      <b>Подождите, идет загрузка данных ...</b>
    </div>

    <div v-if="schedule !== null">

      <ScheduleGenerateDialog
        v-if="days !== null"
        :groupId="groupId"
        :days="days"
        :getSchedule="getSchedule"
      />


      <v-btn
          v-if="days !== null"
          prepend-icon="mdi-file-excel"
          :loading="tableLoading"
          style="margin-bottom: 15px;"
          color="coko-blue"
          @click="addChapter()"
          :text="!(mobileDisplay) && 'Скачать'"
      />

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
                {{studyDay.day}} ({{getDayOfWeek(studyDay.day)}})
              </v-col>

              <v-col
                class="d-flex justify-center"
                cols="2"
              >

                <v-btn
                  color="coko-red"
                  prepend-icon="mdi-pencil"
                  @click.native.stop="console.log('KEK')"
                  text="Изменить"
                />

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
                  :items="studyDay.lessons"
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

                        <div v-if="header.key === 'distance'">

                          <BooleanBadge
                            :bool="item[header.key]"
                          />

                        </div>

                        <div v-if="header.key !== 'distance'">

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

  </div>

</template>

<script>

import {apiRequest} from "@/commons/api_request";
import {showAlert} from "@/commons/alerts";
import {convertBackendDate, convertDateToBackend, getDayOfWeek} from "@/commons/date";
import {useDisplay} from "vuetify";
import ScheduleGenerateDialog from "@/components/dialogs/edu/student_group/schedule/ScheduleGenerateDialog.vue";
import BooleanBadge from "@/components/badges/BooleanBadge.vue";

export default {
  name: 'StudentGroupSchedule',
  components: {BooleanBadge, ScheduleGenerateDialog},
  props: {
    groupId: String, // object_id учбеной группы
  },
  data() {
    return {
      mobileDisplay: useDisplay().smAndDown, // Проверка на дисплей мобильного устройства
      showGenerationDialog: false, // Параметр отображения диалогового окна для генерации расписания
      tableLoading: false, // Параметр загрузки таблицы
      loading: false, // Параметр отображения анимации загрузки
      studentGroup: {
        date_start: null,
        date_end: null,
      }, // Объект с редактируемыми параметрами учебной группы
      schedule: [], // Расписание занятий по дням
      scheduleOpenedPanel: [], // Массив, содержащий параметры раскрытия панелей по дням
      days: null, //Массив учебных дней
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
          'title': 'Тема',
          'key': 'theme'
        },
        {
          'title': 'Лекция',
          'key': 'lecture_hours'
        },
        {
          'title': 'Практика',
          'key': 'practice_hours'
        },
        {
          'title': 'Стажировка',
          'key': 'trainee_hours'
        },
        {
          'title': 'Сам. работа',
          'key': 'individual_hours'
        },
        {
          'title': 'Преподаватель',
          'key': 'teacher'
        },
        {
          'title': 'Дистант',
          'key': 'distance'
        },
        {
          'title': 'Форма контроля',
          'key': 'control'
        },
      ], // Список заголовков таблицы для отображения учебных занятий
    }
  },
  methods: {
    getDayOfWeek,
    // Получение расписания учебной группы
    async getSchedule() {
      let scheduleRequest = await apiRequest(
          '/backend/api/v1/edu/schedule/'+this.groupId+'/',
          'GET',
          true,
          null
      )
      if (scheduleRequest.error) {
        showAlert('error', 'Расписание занятий', scheduleRequest.error)
        return false
      } else {
        this.scheduleOpenedPanel = []
        this.schedule = scheduleRequest
        let days = []
        for (let i=0;i<scheduleRequest.length;i++) {
          days.push(scheduleRequest[i].day)
        }
        console.log(days)
        this.days = days
      }
      this.loading = false
    },
  },
  mounted() {
    this.getSchedule()
  }
}

</script>

<style scoped>
  .v-expansion-panel-title__btn{
    pointer-events: none;
  }

</style>