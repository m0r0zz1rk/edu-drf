<template>

  Статус заявки:<br/>
  <AppStatusBadge
    :appStatus="app.status"
  />
  <br/><br/>
  Наименование услуги:<br/>
  <b>{{app.service_title}}</b>
  <br/><br/>
  Шифр группы:<br/>
  <b>{{app.group_code}}</b>
  <br/><br/>
  Сроки обучения:<br/>
  <b>{{app.service_date_range}}</b>
  <br/><br/>
  Тип:<br/>
  <b>{{app.service_type}}</b>
  <br/><br/>
  Объем (часов):<br/>
  <b>{{app.service_duration}}</b>
  <br/><br/>
  Структурное подразделение:<br/>
  <b>{{app.department}}</b>
  <br/><br/>
  Куратор:<br/>
  <template
      v-if="app.curator_display_name === '-'">
    <b>(Куратор не назначен)</b>
  </template>
  <template v-if="app.curator_display_name !== '-'">
    <b>{{app.curator_display_name}}</b>
    <br/><br/>
    Контактный телефон куратора: <br/>
    <b>+7 3952 500-287 (вн. {{app.curator_phone}})</b>
    <br/><br/>
    Email куратора:<br/>
    <b>{{app.curator_email}}</b>
  </template>

</template>

<script>

// Просмотр основной информации по заявке
import AppStatusBadge from "@/components/badges/students/AppStatusBadge.vue";

export default {
  name: 'AppInfo',
  components: {AppStatusBadge},
  props: {
    // Объект с информацией о заявке
    app: Object
  }
}
</script>

<style scoped>

</style>