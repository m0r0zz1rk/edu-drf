<template>
  <LkPage ref="lkPage" :usePreLoader="usePreLoader">
    <slot>
      <h1>Главная страница</h1>
    </slot>
  </LkPage>

</template>

<script>

import LkPage from "@/components/LkPage.vue";

export default {
  name: 'Main',
  components: {LkPage},
  props: {
    usePreLoader: Function,
  },
  mounted() {
    this.usePreLoader(true)
  }
}

</script>

<style scoped>

</style>
