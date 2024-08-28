<template>
  <v-badge v-if="recStatus === 'WARNING'"
    color="info"
    content="Предупреждение"
    inline
  />
  <v-badge v-if="recStatus === 'ERROR'"
           color="error"
           content="Ошибка"
           inline
  />
  <v-badge v-if="recStatus === 'SUCCESS'"
           color="success"
           content="Успешно"
           inline
  />
</template>

<script>
export default {
  name: "JournalRecStatusBadge",
  props: {
    recStatus: String, //Статус сообщения от бэкенда
  }
}
</script>


<style scoped>

</style>
