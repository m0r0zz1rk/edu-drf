<template>
  <div>
    <v-app class="my-app">
      <keep-alive>
        <PreLoader ref="preLoader" />
      </keep-alive>
      <router-view :usePreLoader="usePreLoader"/>
      <div class="alerts adaptive-alerts">
        <v-alert
          id="error-alert"
          class="alert-hidden adaptive-alert"
          type="error"
        >
        </v-alert>
        <v-alert
          id="warning-alert"
          class="alert-hidden adaptive-alert"
          type="warning"
        ></v-alert>
        <v-alert
          id="info-alert"
          class="alert-hidden adaptive-alert"
          type="info"
        ></v-alert>
        <v-alert
          id="success-alert"
          class="alert-hidden adaptive-alert"
          type="success"
        ></v-alert>
      </div>
    </v-app>
  </div>
</template>

<script>

import PreLoader from "@/components/Preloader.vue";

export default {
  name: 'App',
  data() {
    return {
      firstRender: true
    }
  },
  components: {PreLoader},
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

.alerts {
  position: absolute;
  z-index: 100;
  right: 5px;
  bottom: 5px;
}

.alert-visible {
  z-index: 100;
}

.alert-hidden {
  display: none;
  z-index: 0;
}
</style>
