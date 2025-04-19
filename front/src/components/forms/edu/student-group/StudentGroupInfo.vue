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
        :studentGroupStatus="groupInfo.status"
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
        v-model="groupInfo.code"
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
        v-model="groupInfo.service_name"
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
        v-model="groupInfo.date_start"
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
        v-model="groupInfo.date_end"
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
        v-model="groupInfo.curator"
        label="Куратор"
        readonly
      />
    </v-col>

    <v-col
      v-if="!([null, undefined, 0].includes(groupInfo.plan_seats_number))"
      cols="12"
      md="12"
      sm="12"
    >
      <v-text-field
        bg-color="white"
        variant="underlined"
        v-model="groupInfo.plan_seats_number"
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
        v-model="groupInfo.apps_count"
        label="Количество участников"
        readonly
      />
    </v-col>

  </v-row>

</template>

<script>
import {apiRequest} from "@/commons/apiRequest";
import {showAlert} from "@/commons/alerts";
import StudentGroupStatusBadge from "@/components/badges/edu/StudentGroupStatusBadge.vue";

// Компонент для отображения основной информации по учебной группе
export default {
  name: "StudentGroupInfo",
  components: {StudentGroupStatusBadge},
  props: {
    // Информация об учебной группе
    groupInfo: Object
  },
}
</script>

<style scoped>

</style>
