<template>

  <LkPage :usePreLoader="usePreLoader">
    <slot>
      <v-card color="coko-blue">
        <v-card-text class="adaptive-no-tab-table-card-text">

          <v-tabs v-model="activeAppTab" bg-color="coko-blue" show-arrows>
            <v-tab class="coko-tab" value="course">Заявки на курсы</v-tab>
            <v-tab class="coko-tab" value="event">Заявки на мероприятия</v-tab>
          </v-tabs>

          <CourseApp v-if="activeAppTab === 'course'" :usePreLoader="usePreLoader"/>
          <EventApp v-if="activeAppTab === 'event'" :usePreLoader="usePreLoader"/>

        </v-card-text>
      </v-card>
    </slot>
  </LkPage>

</template>

<script>

// Страница просмотра активных заявок обучающегося
import LkPage from "@/components/LkPage.vue";
import CourseApp from "@/views/users/apps/CourseApp.vue";
import EventApp from "@/views/users/apps/EventApp.vue";

export default {
  name: 'ActiveApps',
  components: {EventApp, CourseApp, LkPage},
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
