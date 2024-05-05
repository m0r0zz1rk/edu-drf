<template>
  <v-app-bar :elevation="0" color="coko-blue">

    <v-app-bar-nav-icon
      variant="text"
      @click.stop="$vuetify.display.xs ? sideMenuProminent = !sideMenuProminent : sideMenuRail = !sideMenuRail"
    ></v-app-bar-nav-icon>

    <v-app-bar-title >
      <div style="display: flex; align-items:center;">
        <a href="https://coko38.ru" target="_blank">
          <img src="../assets/img/app-bar-logo.png"
               style="vertical-align: center"
               width="50px"
               height="50px"
               alt="logo"/>
        </a>&nbsp;&nbsp;
        <span v-if="!($vuetify.display.xs)">АИС "Учебный центр"</span>
      </div>
    </v-app-bar-title>

    <v-spacer></v-spacer>

    <v-menu>
      <template v-slot:activator="{ props }">
        <v-btn
          icon
          v-bind="props"
        >
          <v-icon>mdi-account</v-icon>
        </v-btn>
      </template>

      <UserMenu :usePreLoader="usePreLoader" />
    </v-menu>


  </v-app-bar>

  <v-navigation-drawer
    class="adaptive-side-menu-permanent"
    :permanent="!($vuetify.display.xs)"
    :prominent="$vuetify.display.xs"
    color="coko-blue"
    :rail="$vuetify.display.xs ? false : sideMenuRail"
    v-model="sideMenuProminent"
  >

    <SideMenu />

  </v-navigation-drawer>

  <v-main
    class="v-main"
  >
    <slot></slot>
  </v-main>

</template>

<script>

import SideMenu from "@/components/menus/SideMenu.vue";
import UserMenu from "@/components/menus/UserMenu.vue";

export default {
  name: 'LkPage',
  props: {
    usePreLoader: Function
  },
  components: {UserMenu, SideMenu},
  data() {
    return {
      sideMenuRail: true,
      sideMenuProminent: true,
    }
  },
  mounted() {
    console.log(this.$route.path)
  }
}

</script>

<style scoped>
  .v-main{
    background-image: url('../assets/img/lk-background.jpg');
    background-repeat: repeat;
    opacity: 25%;
  }

</style>
