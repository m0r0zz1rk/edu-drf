<template>
  <div>
    <v-app class="my-app">
      <router-view/>
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

export default {
  name: 'App',
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
