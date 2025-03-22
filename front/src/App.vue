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
      <div class="alerts adaptive-alerts">
        <v-alert
          id="error-alert"
          class="alert-hidden adaptive-alert"
          type="error"
          @click="hideAlert('error')"
        >
        </v-alert>
        <v-alert
          id="warning-alert"
          class="alert-hidden adaptive-alert"
          type="warning"
          @click="hideAlert('warning')"
        ></v-alert>
        <v-alert
          id="info-alert"
          class="alert-hidden adaptive-alert"
          type="info"
          @click="hideAlert('info')"
        ></v-alert>
        <v-alert
          id="success-alert"
          class="alert-hidden adaptive-alert"
          type="success"
          @click="hideAlert('success')"
        ></v-alert>
      </div>
    </v-app>
  </div>
</template>

<script>

import PreLoader from "@/components/Preloader.vue";
import {hideAlert} from "@/commons/alerts";
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
    hideAlert,
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
