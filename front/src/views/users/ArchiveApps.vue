<template>

  <LkPage :usePreLoader="usePreLoader">
    <slot>
      <v-card color="coko-blue">
        <v-card-text class="adaptive-no-tab-table-card-text">

          <v-tabs v-model="archiveAppTab" bg-color="coko-blue" show-arrows>
            <v-tab class="coko-tab" value="course">Заявки на курсы</v-tab>
            <v-tab class="coko-tab" value="event">Заявки на мероприятия</v-tab>
          </v-tabs>

          <ArchiveCourseApp v-if="archiveAppTab === 'course'" :usePreLoader="usePreLoader"/>
          <ArchiveEventApp v-if="archiveAppTab === 'event'" :usePreLoader="usePreLoader"/>

        </v-card-text>
      </v-card>
    </slot>
  </LkPage>

</template>

<script>

// Страница для просмотра архивных заявок
import LkPage from "@/components/LkPage.vue";
import CourseApp from "@/views/users/apps/CourseApp.vue";
import EventApp from "@/views/users/apps/EventApp.vue";
import ArchiveCourseApp from "@/views/users/apps/archive/CourseApp.vue";
import ArchiveEventApp from "@/views/users/apps/archive/EventApp.vue";

export default {
  name: 'ArchiveApps',
  components: {ArchiveEventApp, ArchiveCourseApp, EventApp, CourseApp, LkPage},
  props: {
    // Функция отображения/скрытия полноразмерной анимации загрузки страницы
    usePreLoader: Function
  },
  data() {
    return {
      // Выбранная вкладка
      archiveAppTab: 'course'
    }
  }
}

</script>

<style scoped>

</style>
