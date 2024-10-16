<template>

  <LkPage :usePreLoader="usePreLoader">
    <slot>
      <v-card
          color="coko-blue"
          class="lk-full-page-card"
      >
        <v-card-title>
          Архивные заявки
          <v-tabs
              v-model="archiveAppTab"
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

        </v-card-text>
      </v-card>
    </slot>
  </LkPage>

</template>

<script>

// Страница для просмотра архивных заявок
import LkPage from "@/components/LkPage.vue";

export default {
  name: 'ArchiveApps',
  components: {LkPage},
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