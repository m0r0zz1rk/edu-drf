<template>

  <div
    style="padding: 10px; width: 98%"
  >

    <div v-if="schedule === null">
      <b>Подождите, идет загрузка данных ...</b>
    </div>

    <div v-if="schedule !== null">

      <v-btn
          v-if="days !== null"
          prepend-icon="mdi-plus"
          :loading="tableLoading"
          style="margin-bottom: 15px; margin-right: 15px"
          color="coko-blue"
          @click="showGenerationDialog=!showGenerationDialog"
          :text="!(mobileDisplay) && 'Добавить'"
      />

      <ScheduleGenerateDialog
        v-if="days !== null"
        :days="days"
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
            :title="studyDay.day+' ('+getDayOfWeek(studyDay.day)+')'"
        >

          <div
              v-if="studyDay.lessons.length === 0"
              style="text-align: center"
          >
            <b>Нет занятий</b>
          </div>

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

export default {
  name: 'StudentGroupSchedule',
  components: {ScheduleGenerateDialog},
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
        this.schedule = scheduleRequest
        let panel = []
        let days = []
        for (let i=0;i<scheduleRequest.length;i++) {
          panel.push(i)
          days.push(scheduleRequest[i].day)
        }
        console.log(days)
        this.scheduleOpenedPanel = panel
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

</style>