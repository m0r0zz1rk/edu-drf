<template>
  <v-app-bar :elevation="0" height="20px" color="coko-blue">

    <v-app-bar-nav-icon
      variant="text"
      @click.stop="$vuetify.display.xs ? sideMenu = !sideMenu : sideMenuRail = !sideMenuRail"
    ></v-app-bar-nav-icon>

    <v-app-bar-title >
      <div style="display: flex; align-items:center;">
        <a href="https://coko38.ru" target="_blank">
          <img src="../assets/img/app-bar-logo.png"
               style="vertical-align: center"
               width="30px"
               height="30px"
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
    style="padding-top: 50px"
    class="adaptive-side-menu-permanent"
    :permanent="!($vuetify.display.xs)"
    :prominent="$vuetify.display.xs"
    color="coko-blue"
    :rail="$vuetify.display.xs ? false : sideMenuRail"
    v-model="sideMenu"
  >

    <SideMenu />

  </v-navigation-drawer>

  <v-main
    style="height: calc(100vh - 80px);
            overflow-y: auto;
            overflow-x: hidden;"
  >

      <div class="background-div"></div>

      <div class="content-div adaptive-content-div">
        <slot></slot>
      </div>

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
      sideMenuProminent: false,
      sideMenu: false
    }
  },
  mounted() {
    this.sideMenu = !(this.$vuetify.display.xs)
  }
}

</script>

<style scoped>
  .background-div{
    position: absolute;
    top: 0;
    left: 0;
    width: 100vw;
    height: 100vh;
    background-image: url('../assets/img/lk-background.jpg');
    background-repeat: repeat;
    opacity: 25%;
  }

  .content-div {
    z-index: 15;
  }

</style>
