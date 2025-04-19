<template>

  <v-icon
    color="coko-blue"
    icon="mdi-file-move"
    @click="appMoveFunction(application)"
  />



</template>

<script>

// Ячейка для переноса заявки из одной учебной группы в другую
export default {
  name: 'AppMove',
  props: {
    // Функция для выбора заявки и подготовки к ее переносу
    appMoveFunction: Function,
    // Заявка
    application: Object
  }
}

</script>


<style scoped>

</style>
