<template>

  <v-alert
    id="content-error-alert"
    class="alert-hidden"
    style="width: 100%"
    :text="errorText"
    type="error"
  ></v-alert>

  <v-container>

    <slot></slot>

  </v-container>

</template>

<script>
//Содержимое, проходящее проверку на ошибки в диалоговом окне
export default {
  name: "DialogContentWithError",
  data() {
    return {
      errorText: '' // Текст ошибки
    }
  },
  methods: {
    // Скрыть ошибку
    hideContentError() {
      this.errorText = ''
      document.querySelector('#content-error-alert').classList.remove('alert-visible')
      document.querySelector('#content-error-alert').classList.add('alert-hidden')
    },
    // Показать ошибку
    showContentError(message) {
      this.errorText = message
      document.querySelector('#content-error-alert').classList.add('alert-visible')
      document.querySelector('#content-error-alert').classList.remove('alert-hidden')
    },
  }
}
</script>



<style scoped>
  @import '../../assets/css/alerts.css';
</style>
