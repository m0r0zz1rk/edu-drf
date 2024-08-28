<template>

  <v-progress-circular
    v-if="studyDates === null"
    color="coko-blue"
    indeterminate
  />

  <v-expansion-panels
    v-if="studyDates !== null"
    v-model="schedule"
    multiple
  >

  </v-expansion-panels>

</template>

<script>
// Компонент для работы с расписанием занятий учебной группы
import {apiRequest} from "@/commons/api_request";
import {showAlert} from "@/commons/alerts";
import {convertBackendDate} from "@/commons/date";

export default {
  name: "ScheduleForm",
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
      studyDates: null, // Список дат обучения учебной группы
      schedule: [], // Список открытых дней с расписанием занятий
    }
  },
  methods: {
    async getInfo() {
      let infoRequest = await apiRequest(
        '/backend/api/v1/edu/student_group/'+this.groupId+'/',
        'GET',
        true,
        null
      )
      if (infoRequest.error) {
        showAlert('error', 'Информация по учебной группе', infoRequest.error)
        return false
      } else {
        Object.keys(this.studentGroup).map((key) => {
          this.studentGroup[key] = infoRequest[key]
        })
      }
      let checkDate = convertBackendDate(this.studentGroup.date_start)
      let datesArr = []
      while (checkDate <= convertBackendDate(this.studentGroup.date_end)) {
        datesArr.push
      }
      this.loading = false
    },
  },
  mounted() {
    this.getInfo()
  }
}
</script>

<style scoped>

</style>
