<template>
  <LkPage :usePreLoader="usePreLoader">
    <slot>
      <v-card
          variant="outlined"
      >
        <v-card-text>
          <div style="background-color: white; overflow: auto;" class="adaptive-no-tab-table-card-text">
            <v-tabs class="guides-tabs"
                    v-model="guidesTab"
                    bg-color="coko-blue"
                    show-arrows
            >
              <v-tab class="guides-tab" value="user">Пользователи</v-tab>
              <v-tab class="guides-tab" value="state">Государства</v-tab>
              <v-tab class="guides-tab" value="mo">МО</v-tab>
              <v-tab class="guides-tab" value="oo_type">Типы ОО</v-tab>
              <v-tab class="guides-tab" value="oo">ОО</v-tab>
              <v-tab class="guides-tab" value="audience_category">Категории слушателей</v-tab>
              <v-tab class="guides-tab" value="event_type">Типы мероприятий</v-tab>
              <v-tab class="guides-tab" value="position_category">Категории должностей</v-tab>
              <v-tab class="guides-tab" value="position">Должности</v-tab>

            </v-tabs>
          </div>
        </v-card-text>
      </v-card>
    </slot>
  </LkPage>
</template>

<script>
import LkPage from "@/components/LkPage.vue";

export default {
  name: "Guides",
  components: {LkPage},
  props: {
    usePreLoader: Function,
  },
  data() {
    return {
      guidesTab: 'user'
    }
  },
  mounted() {
    this.usePreLoader(true)
  }
}
</script>

<style scoped>
.guides-tab {
  color: white;
}

.guides-tab:hover {
  background-color: #FF5722;
}
</style>
