<template>

  <v-badge
    :color="appTypes.filter((st) => st.key === appType)[0].color"
    :content="appTypes.filter((st) => st.key === appType)[0].title"
    inline
  />

</template>


<script>
// Бэйдж для отоюражения типа мероприятия заявки обучающегося
import {appTypes} from "@/commons/consts/apps/appTypes";

export default {
  name: "AppTypeBadge",
  props: {
    // Тип заявки
    appType: String
  },
  data() {
    return {
      // Список типов мероприятий
      appTypes: appTypes
    }
  }
}
</script>

<style scoped>

</style>
