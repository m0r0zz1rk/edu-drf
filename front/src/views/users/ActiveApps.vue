<template>

  <LkPage :usePreLoader="usePreLoader">
    <slot>
      <v-card
          color="coko-blue"
          class="lk-full-page-card"
      >
        <v-card-title>
          Активные заявки
          <v-tabs
              v-model="activeAppTab"
              bg-color="coko-blue"
              show-arrows
          >
            <v-tab class="coko-tab" value="course">Курсы</v-tab>
            <v-tab class="coko-tab" value="event">Мероприятия</v-tab>
          </v-tabs>
        </v-card-title>
        <v-card-text
          class="adaptive-no-tab-table-card-text"
        >

          <CourseApp
              v-if="activeAppTab === 'course'"
              :usePreLoader="usePreLoader"
          />

        </v-card-text>
      </v-card>
    </slot>
  </LkPage>

</template>

<script>

// Страница просмотра активных заявок обучающегося
import LkPage from "@/components/LkPage.vue";
import CourseApp from "@/views/users/apps/CourseApp.vue";

export default {
  name: 'ActiveApps',
  components: {CourseApp, LkPage},
  props: {
    // Функция отображения/скрытия анимации загрузки
    usePreLoader: Function,
  },
  data() {
    return {
      // Выбранный тип заявок
      activeAppTab: 'course'
    }
  }
}

</script>

<style scoped>

</style>