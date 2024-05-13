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
              <v-tab class="coko-tab" value="user">Обучающиеся</v-tab>
              <v-tab class="coko-tab" value="coko">Сотрудники</v-tab>
              <v-tab class="coko-tab" value="state">Государства</v-tab>
              <v-tab class="coko-tab" value="mo">МО</v-tab>
              <v-tab class="coko-tab" value="oo_type">Типы ОО</v-tab>
              <v-tab class="coko-tab" value="oo">ОО</v-tab>
              <v-tab class="coko-tab" value="audience_category">Категории слушателей</v-tab>
              <v-tab class="coko-tab" value="event_type">Типы мероприятий</v-tab>
              <v-tab class="coko-tab" value="position_category">Категории должностей</v-tab>
              <v-tab class="coko-tab" value="position">Должности</v-tab>

            </v-tabs>

            <GuideUser v-if="guidesTab === 'user'" />

            <GuideCoko v-if="guidesTab === 'coko'" />
          </div>
        </v-card-text>
      </v-card>
    </slot>
  </LkPage>
</template>

<script>
import LkPage from "@/components/LkPage.vue";
import GuideUser from "@/views/administrator/guides/GuideUser.vue";
import GuideCoko from "@/views/administrator/guides/GuideCoko.vue";

export default {
  name: "Guides",
  components: {GuideCoko, GuideUser, LkPage},
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

</style>
