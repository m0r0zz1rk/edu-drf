<template>

  <v-btn
      prepend-icon="mdi-creation"
      :loading="loading"
      style="margin-bottom: 15px; margin-right: 15px"
      color="coko-blue"
      @click="dialog=!dialog"
      :text="!(mobileDisplay) && 'Сгенерировать'"
  />

  <v-dialog
      persistent
      v-model="dialog"
  >

    <v-card class="lk-full-page-card">
      <v-card-title class="d-flex justify-space-between align-center">

        Генерация шаблона расписания

        <v-btn
            icon="mdi-close"
            color="coko-blue"
            @click="dialog = !(dialog)"
        />
      </v-card-title>

      <v-card-text>

        <DialogContentWithError ref="content-error">

          <b>
            ВНИМАНИЕ! Все существующие занятия учебных дней, которые будут задействованы
            в процессе генерации, будут удалены
          </b>

          <br/>

          <v-data-table
              sticky
              v-if="template !== null"
              class="adaptive-schedule-table"
              style="overflow: auto;"
              :headers="headers"
              :mobile-breakpoint="960"
              :items="template.sort((a, b) => a.day - b.day)"
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

                    <template v-if="header.key === 'day'">

                      {{item[header.key]}}<br/>({{getDayOfWeek(item[header.key])}})

                    </template>

                    <template v-if="header.key === 'study_day'">

                      <v-checkbox
                        class="d-inline-flex"
                        v-model="item[header.key]"
                      />

                    </template>

                    <template v-if="header.key === 'time_start'">

                      <v-text-field
                        v-model="item[header.key]"
                        :active="timePickerDialogs.filter((rec) => rec.day === item['day'])[0].open"
                        :focused="timePickerDialogs.filter((rec) => rec.day === item['day'])[0].open"
                        append-inner-icon="mdi-clock-time-four-outline"
                        :disabled="!(item['study_day'])"
                        readonly
                      >

                        <v-dialog
                          v-model="timePickerDialogs.filter((rec) => rec.day === item['day'])[0].open"
                          activator="parent"
                          width="auto"
                        >

                          <v-time-picker
                            v-if="timePickerDialogs.filter((rec) => rec.day === item['day'])[0].open"
                            format="24hr"
                            title="Выберите время начала занятия"
                            v-model="item[header.key]"
                          ></v-time-picker>


                        </v-dialog>

                      </v-text-field>

                    </template>

                    <template v-if="header.key === 'hours_count'">

                      <v-number-input
                        :min="1"
                        :max="8"
                        :disabled="!(item['study_day'])"
                        v-model="item[header.key]"
                      />

                    </template>

                  </td>

                </template>

              </tr>

            </template>

            <template v-slot:loading>
              <v-skeleton-loader :type="'table-row@10'"></v-skeleton-loader>
            </template>

            <template v-slot:bottom></template>

          </v-data-table>

        </DialogContentWithError>

      </v-card-text>

      <v-card-actions
          style="background-color: white"
      >

        <v-spacer></v-spacer>

        <v-btn
            color="coko-blue"
            text="Сгенерировать"
            :loading="loading"
            @click="generateSchedule()"
        ></v-btn>
      </v-card-actions>

    </v-card>

  </v-dialog>

</template>

<script>

import DialogContentWithError from "@/components/dialogs/DialogContentWithError.vue";
import {useDisplay} from "vuetify";
import {getDayOfWeek} from "@/commons/date";
import {apiRequest} from "@/commons/api_request";
import {showAlert} from "@/commons/alerts";

export default {
  name: 'ScheduleGenerateDialog',
  components: {DialogContentWithError},
  props: {
    groupId: String, // object_id учебной группы
    days: Array, // Список учебных дней
    getSchedule: Function, // Функция получения расписания в родительском компоненте
  },
  data() {
    return {
      dialog: false, // Параметр отображения диалогового окна
      loading: false, // Параметр выполнения процесса и отключения возможности редактирования формы
      mobileDisplay: useDisplay().smAndDown, // Проверка на дисплей мобильного устройства
      headers: [
        {
          'title': 'День',
          'key': 'day'
        },
        {
          'title': 'Сгенерировать',
          'key': 'study_day'
        },
        {
          'title': 'Начало занятий',
          'key': 'time_start'
        },
        {
          'title': 'Кол-во часов',
          'key': 'hours_count'
        },
      ], // Заголовки таблицы
      template: null, // Шаблон расписания
      timePickerDialog: false, // Параметр отображения диалогового окна с выбором времени начала занятия
      timePickerDialogs: null, // Список параметров отображение компонента для выбора времени
    }
  },
  methods: {
    getDayOfWeek,
    // Формирование базового шалона расписания для формы
    createScheduleTemplate() {
      let temp = []
      let tsd = []
      this.days.map((day) => {
        temp.push({
          'day': day,
          'study_day': true,
          'time_start': '09:00',
          'hours_count': 4
        })
        tsd.push({
          'day': day,
          'open': false
        })
      })
      console.log(temp)
      this.template = temp
      this.timePickerDialogs = tsd
    },
    // Процесс генерации шаблона расписания учебной группы
    async generateSchedule() {
      this.loading = true
      let scheduleGenerateRequest = await apiRequest(
          '/backend/api/v1/edu/schedule/generate/',
          'POST',
          true,
          {
            'group_id': this.groupId,
            'generate': this.template
          }
      )
      if (scheduleGenerateRequest.error) {
        showAlert('error', 'Генерация расписания', scheduleGenerateRequest.error)
      } else {
        this.dialog = false
        showAlert(
            'success',
            'Генерация расписания',
            scheduleGenerateRequest.success
        )
        this.getSchedule()
      }
      this.loading = false
    }
  },
  mounted() {
    this.createScheduleTemplate()
  }
}

</script>

<style scoped>

</style>