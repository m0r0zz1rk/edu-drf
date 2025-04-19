<template>
  <div>
    <v-app class="my-app">
      <keep-alive>
        <PreLoader ref="preLoader" />
      </keep-alive>
      <router-view :usePreLoader="usePreLoader"/>
      <notifications
        position="top right"
      />
    </v-app>
  </div>
</template>

<script>

import PreLoader from "@/components/Preloader.vue";
import {Notifications} from "@kyvg/vue3-notification";

export default {
  name: 'App',
  data() {
    return {
      firstRender: true
    }
  },
  components: {Notifications, PreLoader},
  methods: {
    usePreLoader(onlyClose = false) {
      this.$refs.preLoader.usePreloader(onlyClose)
    }
  },
  mounted() {
    if (!(this.$refs.preLoader.preLoader)) {
      this.usePreLoader()
    }
  }
}
</script>

<style scoped>

@import "./assets/css/alerts.css";

</style>
