<template>

  <div
    style="padding: 10px; width: 98%"
  >

    <div v-if="schedule.length === 0">
      <b>Подождите, идет загрузка данных ...</b>
    </div>

    <div v-else>

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
          @click="downloadExcel()"
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

                <ScheduleDayManage
                  :groupId="groupId"
                  :serviceType="serviceType"
                  :dayInfo="studyDay"
                  :getSchedule="getSchedule"
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
                            v-if="['distance', 'type'].includes(header.key)"
                        >

                          <BooleanBadge
                              v-if="header.key === 'distance'"
                              :bool="item[header.key]"
                          />

                          <p
                            v-if="header.key === 'type'"
                          >
                            {{ lTypes.filter((t) => t.key === item[header.key])[0].name }}
                          </p>

                        </template>


                        <div
                            v-if="!(['distance', 'type'].includes(header.key))"
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

  </div>

</template>

<script>

import {apiRequest} from "@/commons/apiRequest";
import {showAlert} from "@/commons/alerts";
import {getDayOfWeek} from "@/commons/date";
import {useDisplay} from "vuetify";
import ScheduleGenerateDialog from "@/components/dialogs/edu/student_group/schedule/ScheduleGenerateDialog.vue";
import BooleanBadge from "@/components/badges/BooleanBadge.vue";
import ScheduleDayManage from "@/components/dialogs/edu/student_group/schedule/ScheduleDayManage.vue";
import lessonTypes from "../../../../commons/consts/edu/lessonTypes";
import {convertTimeStrToSeconds} from "@/commons/time";

export default {
  name: 'StudentGroupSchedule',
  components: {ScheduleDayManage, BooleanBadge, ScheduleGenerateDialog},
  props: {
    groupId: String, // object_id учбеной группы
    serviceType: String, // Тип услуги учебной группы (ou или iku)
    // Код учебной группы (для наименования файла при выгрузке расписания)
    code: String,
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
      lTypes: lessonTypes, // Типы учебных занятий
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
          'title': 'Тип занятия',
          'key': 'type'
        },
        {
          'title': 'Преподаватель',
          'key': 'teacher_fio'
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
    convertTimeStrToSeconds,
    getDayOfWeek,
    // Получение расписания учебной группы
    async getSchedule() {
      this.schedule = []
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
        this.days = days
      }
      this.loading = false
    },
    // Скачивание Excel файла с расписанием
    async downloadExcel() {
      this.tableLoading = true
      const getDocRequest = await apiRequest(
        '/backend/api/v1/edu/student_group/doc/',
        'POST',
        true,
        {group_id: this.groupId, doc_type: 'schedule'},
        true
      )
      if (getDocRequest.status === 200) {
        const data = await getDocRequest.blob()
        let a = document.createElement('a')
        a.href = window.URL.createObjectURL(data)
        a.download = `Расписание ${this.code}.xlsx`
        a.click()
      } else {
        let message = '\'Произошла ошибка при получении документа'
        let data = await getDocRequest.json()
        if (data.error) {
          message = data.error
        }
        showAlert('error', 'Файл с расписанием', message)
      }
      this.tableLoading = false
    }
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
