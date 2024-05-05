<template>
  <v-list bg-color="coko-blue">
    <v-list-item
      v-if="profileItem"
      title="Профиль"
      value="profile"
      @click="navigate('/profile')"
    ></v-list-item>
    <v-list-item
      title="Выход"
      value="logout"
      @click="logout()"
    ></v-list-item>
  </v-list>
</template>

<script>
import {getCookie, setCookie} from "@/commons/cookie";
import {apiRequest} from "@/commons/api_request";

export default {
  name: "UserMenu",
  props: {
    usePreLoader: Function
  },
  data() {
    return {
      profileItem: false
    }
  },
  methods: {
    checkProfileItem() {
      if (getCookie('cokoRole')) {
        this.profileItem = getCookie('cokoRole') === 'student'
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
            this.profileItem = data.role === 'student'
          })
      }
    },
    navigate(path) {
      this.$router.push(path)
    },
    logout() {
      this.$store.dispatch('AUTH_LOGOUT')
        .then(() => {
          this.usePreLoader()
          this.$router.push('/login')
        })
    },
  },
  mounted() {
    this.checkProfileItem()
  }
}
</script>

<style scoped>

</style>
