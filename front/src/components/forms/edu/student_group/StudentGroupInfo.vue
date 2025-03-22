<template>

  <v-row
    dense
    style="padding: 10px;width: 98%"
  >

    <v-col
      cols="12"
      md="12"
      sm="12"
    >
      <b>Статус:</b>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
      <StudentGroupStatusBadge
        :studentGroupStatus="studentGroup.status"
      />
    </v-col>

    <v-col
      cols="12"
      md="12"
      sm="12"
    >
      <v-text-field
        bg-color="white"
        variant="underlined"
        v-model="studentGroup.code"
        label="Шифр"
        readonly
      />
    </v-col>

    <v-col
      cols="12"
      md="12"
      sm="12"
    >
      <v-textarea
        bg-color="white"
        variant="underlined"
        v-model="studentGroup.service_name"
        label="Наименование услуги"
        readonly
      />
    </v-col>

    <v-col
      cols="12"
      md="12"
      sm="12"
    >
      <v-text-field
        bg-color="white"
        variant="underlined"
        v-model="studentGroup.date_start"
        label="Дата начала обучения"
        readonly
      />
    </v-col>

    <v-col
      cols="12"
      md="12"
      sm="12"
    >
      <v-text-field
        bg-color="white"
        variant="underlined"
        v-model="studentGroup.date_end"
        label="Дата окончания обучения"
        readonly
      />
    </v-col>

    <v-col
      cols="12"
      md="12"
      sm="12"
    >
      <v-text-field
        bg-color="white"
        variant="underlined"
        v-model="studentGroup.curator"
        label="Куратор"
        readonly
      />
    </v-col>

    <v-col
      v-if="!([null, undefined, 0].includes(studentGroup.plan_seats_number))"
      cols="12"
      md="12"
      sm="12"
    >
      <v-text-field
        bg-color="white"
        variant="underlined"
        v-model="studentGroup.plan_seats_number"
        label="Плановое количество мест"
        readonly
      />
    </v-col>

    <v-col
      cols="12"
      md="12"
      sm="12"
    >
      <v-text-field
        bg-color="white"
        variant="underlined"
        v-model="studentGroup.apps_count"
        label="Количество участников"
        readonly
      />
    </v-col>

  </v-row>

</template>

<script>
import {apiRequest} from "@/commons/api_request";
import {showAlert} from "@/commons/alerts";
import StudentGroupStatusBadge from "@/components/badges/edu/StudentGroupStatusBadge.vue";

// Компонент для отображения основной информации по учебной группе
export default {
  name: "StudentGroupInfo",
  components: {StudentGroupStatusBadge},
  props: {
    groupId: String // object_id учебной группы
  },
  data() {
    return {
      studentGroup: {
        code: null,
        service_name: null,
        date_start: null,
        date_end: null,
        curator: null,
        apps_count: null,
        plan_seats_number: null,
        status: null
      } // Объект учебной группы
    }
  },
  methods: {
    // Получение информации по учебной группе
    async getInfo() {
      let infoRequest = await apiRequest(
        '/backend/api/v1/edu/student_group/'+this.groupId+'/',
        'GET',
        true,
        null
      )
      if (infoRequest.error) {
        showAlert('error', 'Информаци по учебной группе', infoRequest.error)
        return false
      } else {
        Object.keys(this.studentGroup).map((key) => {
          this.studentGroup[key] = infoRequest[key]
        })
      }
    }
  },
  mounted() {
    this.getInfo()
  }
}
</script>

<style scoped>

</style>
