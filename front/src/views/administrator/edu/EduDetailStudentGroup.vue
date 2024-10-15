<template>

  <LkPage :usePreLoader="usePreLoader">

    <slot>

      <div>

        <StudentGroupForm
          :groupId="$route.params.groupId"
        />

      </div>

    </slot>

  </LkPage>

</template>

<script>
import LkPage from "@/components/LkPage.vue";
import StudentGroupForm from "@/components/forms/edu/StudentGroupForm.vue";

// Страница управления учебной группой
export default {
  name: "EduDetailStudentGroup",
  components: {StudentGroupForm, LkPage},
  props: {
    usePreLoader: Function, // Активация анимации загрузки
  },
}
</script>

<style scoped>

</style>
