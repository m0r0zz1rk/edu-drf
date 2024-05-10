<template>
  <LkPage :usePreLoader="usePreLoader">
    <slot>
      <StudentMainPage v-if="userRole === 'student'" />
      <CentreMainPage v-if="userRole === 'centre'" />
    </slot>
  </LkPage>

</template>

<script>

import LkPage from "@/components/LkPage.vue";
import {apiRequest} from "@/commons/api_request";
import {showAlert} from "@/commons/alerts";
import {getCookie, setCookie} from "@/commons/cookie";
import centreMenuItems from "@/components/menus/menu_items/centre_menu_items";
import depMenuItems from "@/components/menus/menu_items/dep_menu_items";
import studentMenuItems from "@/components/menus/menu_items/student_menu_items";
import StudentMainPage from "@/components/main_pages/StudentMainPage.vue";
import CentreMainPage from "@/components/main_pages/CentreMainPage.vue";

export default {
  name: 'Main',
  components: {CentreMainPage, StudentMainPage, LkPage},
  props: {
    usePreLoader: Function,
  },
  data() {
    return {
      userRole: 'student'
    }
  },
  methods: {
    async getUserRole() {
      if (getCookie('cokoRole')) {
        this.userRole = getCookie('cokoRole')
      } else {
        let getRoleRequest = await apiRequest(
          '/backend/api/v1/auth/get_user_role/',
          'GET',
          true,
          null,
          false
        )
        this.userRole = getRoleRequest.role
      }
    }
  },
  mounted() {
    this.getUserRole()
    this.usePreLoader(true)
  }
}

</script>

<style scoped>

</style>
