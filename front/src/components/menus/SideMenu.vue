<template>
  <v-list
    density="compact"
    v-model="menuList"
    nav
  >
    <v-list-item
      prepend-icon="mdi-home"
      class="adaptive-nav-list-item"
      title="Главная"
      :active="$route.path === '/'"
      value="main"
      @click="$route.path !== '/' ? navigate('/') : false"
    ></v-list-item>
    <v-list-item v-for="item in menuItems"
      :prepend-icon="item.icon"
      class="adaptive-nav-list-item"
      :title="item.title"
      :active="$route.path === item.link"
      :value="item.value"
      @click="$route.path !== item.link ? navigate(item.link) : false"
    ></v-list-item>
  </v-list>
</template>

<script>
import {apiRequest} from "@/commons/api_request";
import {getCookie, setCookie} from "@/commons/cookie";
import studentMenuItems from "@/components/menus/menu_items/student_menu_items";
import centreMenuItems from "@/components/menus/menu_items/centre_menu_items";
import depMenuItems from "@/components/menus/menu_items/dep_menu_items";

export default {
  name: "SideMenu",
  data() {
    return {
      menuList: 'main',
      menuItems: []
    }
  },
  methods: {
    async getMenuItems() {
      if (getCookie('cokoRole')) {
        switch (getCookie('cokoRole')) {
          case 'centre':
            this.menuItems = centreMenuItems
            break;

          case 'dep':
            this.menuItems = depMenuItems
            break;

          default:
            this.menuItems = studentMenuItems
        }
      } else {
        apiRequest(
          '/backend/api/v1/auth/get_user_role/',
          'GET',
          true,
          null,
          false
        )
          .then(data => {
            setCookie('cokoRole', data.role)
            switch (data.role) {
              case 'centre':
                this.menuItems = centreMenuItems
                break;

              case 'dep':
                this.menuItems = depMenuItems
                break;

              default:
                this.menuItems = studentMenuItems
            }
          })
      }
    },
    navigate(path) {
      this.$router.push(path)
    }
  },
  mounted() {
    this.getMenuItems()
  }
}
</script>


<style scoped>

</style>
