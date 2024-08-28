<template>

  <v-badge v-if="studentGroupStatus === 'REGISTRATION'"
           color="purple"
           content="Регистрация"
           inline
  />

  <v-badge v-if="studentGroupStatus === 'PROCESS'"
           color="blue"
           content="В процессе"
           inline
  />

  <v-badge v-if="studentGroupStatus === 'COMPLETE'"
           color="green"
           content="Заврешено"
           inline
  />

  <v-badge v-if="studentGroupStatus === 'OFFER'"
           color="indigo"
           content="Скан договора оферты"
           inline
  />

  <v-badge v-if="studentGroupStatus === 'URL'"
           color="blue-grey"
           content="Ссылка на обучение"
           inline
  />

  <v-badge v-if="studentGroupStatus === 'STATEMENT'"
           color="deep-orange"
           content="Утверждение состава"
           inline
  />

</template>

<script>

// Компонент для отображения статуса учебной группы
export default {
  name: "StudentGroupStatusBadge",
  props: {
    studentGroupStatus: String, //Статус учебной группы от бэкенда,
  }
}
</script>

<style scoped>

</style>
