<template>
  <LkPage :usePreLoader="usePreLoader">
    <slot>
      <v-card
        variant="outlined"
      >
        <v-card-text>

          <div style="background-color: white; overflow: auto;" class="adaptive-no-tab-table-card-text">

            <v-tabs class="guides-tabs"
                    v-model="eduTab"
                    bg-color="coko-blue"
                    show-arrows
            >

              <v-tab class="coko-tab" value="dpp">ДПП</v-tab>
              <v-tab class="coko-tab" value="planning">Планирование</v-tab>
              <v-tab class="coko-tab" value="ou">Курсы (ОУ)</v-tab>
              <v-tab class="coko-tab" value="iku">Мероприятия (ИКУ)</v-tab>
              <v-tab class="coko-tab" value="group">Учебные группы</v-tab>
              <v-tab class="coko-tab" value="schedule">Расписания</v-tab>

            </v-tabs>

            <EduDpp v-if="eduTab === 'dpp'" />

            <EduPlanningParameter v-if="eduTab === 'planning'" />

            <EducationService v-if="eduTab === 'ou'" />

          </div>
        </v-card-text>
      </v-card>
    </slot>
  </LkPage>
</template>

<script>
import LkPage from "@/components/LkPage.vue";
import EduDpp from "@/views/administrator/edu/EduDpp.vue";
import EduPlanningParameter from "@/views/administrator/edu/EduPlanningParameter.vue";
import EducationService from "@/views/administrator/edu/EducationService.vue";

export default {
  name: "Edu",
  components: {EducationService, EduPlanningParameter, EduDpp, LkPage},
  props: {
    usePreLoader: Function,
  },
  data() {
    return {
      eduTab: 'dpp'
    }
  },
  mounted() {
    this.usePreLoader(true)
  }
}
</script>

<style scoped>

</style>
