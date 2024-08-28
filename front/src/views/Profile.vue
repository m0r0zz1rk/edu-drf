<template>
  <LkPage ref="lkPage" :usePreLoader="usePreLoader">
    <slot>
      <ProfileForm />
    </slot>
  </LkPage>
</template>

<script>
import ProfileForm from "@/components/forms/ProfileForm.vue";
import LkPage from "@/components/LkPage.vue";

export default {
  name: "Profile",
  props: {
    usePreLoader: Function,
  },
  components: {LkPage, ProfileForm},
  mounted() {
    this.usePreLoader(true)
  }
}
</script>

<style scoped>

</style>
