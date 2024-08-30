<template>

  <div
    style="padding: 10px; width: 98%"
  >

    <v-progress-circular
        v-if="schedule === null"
        color="coko-blue"
        indeterminate
    />

    <v-expansion-panels
        v-if="schedule !== null"
        v-model="scheduleOpenedPanel"
        multiple
    >

      <v-expansion-panel
          v-for="studyDay in schedule"
          color="coko-blue"
          :title="studyDay.day"
      >

      </v-expansion-panel>

    </v-expansion-panels>

  </div>

</template>

<script>

import {apiRequest} from "@/commons/api_request";
import {showAlert} from "@/commons/alerts";
import {convertBackendDate, convertDateToBackend} from "@/commons/date";

export default {
  name: 'StudentGroupSchedule',
  props: {
    groupId: String, // object_id учбеной группы
  },
  data() {
    return {
      loading: false, // Параметр отображения анимации загрузки
      studentGroup: {
        date_start: null,
        date_end: null,
      }, // Объект с редактируемыми параметрами учебной группы
      schedule: [], // Расписание занятий по дням
      scheduleOpenedPanel: [], // Массив, содержащий параметры раскрытия панелей по дням
    }
  },
  methods: {
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
        for (let i=0;i<scheduleRequest.length;i++) {
          panel.push(i)
        }
        this.scheduleOpenedPanel = panel
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