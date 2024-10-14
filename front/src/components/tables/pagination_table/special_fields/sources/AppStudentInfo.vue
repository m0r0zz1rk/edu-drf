<template>

  <div>

    {{studentInfo.display_name}}<br/>
    {{studentInfo.email}}<br/>
    {{studentInfo.phone}}

  </div>

</template>

<script>

// Компонент для отображения информации об обучающемся в заявке учебной группы
export default {
  name: 'AppStudentInfo',
  props: {
    // Объект с информацией о студенте
    studentInfo: Object,
  }
}

</script>

<style scoped>

</style>