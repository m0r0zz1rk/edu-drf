<template>

  <v-badge
      :color="appStatuses.filter((st) => st.key === appStatus)[0].color"
      :content="appStatuses.filter((st) => st.key === appStatus)[0].title"
      inline
  />

</template>

<script>

// Бэйдж для отображения статуса заявки обучающегося
import appStatuses from "@/commons/consts/apps/appStatuses";

export default {
  name: 'AppStatusBadge',
  props: {
    // Статус заявки
    appStatus: String
  },
  data() {
    return {
      // Список статусов заявок
      appStatuses: appStatuses
    }
  }
}

</script>

<style scoped>

</style>