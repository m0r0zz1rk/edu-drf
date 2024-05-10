<template>
  <v-badge v-if="recStatus === 'WARNING'"
    color="info"
    content="Предупреждение"
    inline
  ></v-badge>
  <v-badge v-if="recStatus === 'ERROR'"
           color="error"
           content="Ошибка"
           inline
  ></v-badge>
  <v-badge v-if="recStatus === 'SUCCESS'"
           color="success"
           content="Успешно"
           inline
  ></v-badge>
</template>

<script>
export default {
  name: "JournalRecStatusBadge",
  props: {
    recStatus: String, //
  }
}
</script>


<style scoped>

</style>
