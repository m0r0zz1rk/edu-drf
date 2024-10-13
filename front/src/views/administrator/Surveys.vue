<template>

  <LkPage :usePreLoader="usePreLoader">
    <slot>
      <v-card
          variant="outlined"
      >
        <v-card-text>
          <div
              style="background-color: white; overflow: auto;"
              class="adaptive-no-tab-table-card-text"
          >
            <v-tabs
                v-model="surveyTab"
                bg-color="coko-blue"
                show-arrows
            >
              <v-tab class="coko-tab" value="base">База опросов</v-tab>
              <v-tab class="coko-tab" value="target">Таргетирование</v-tab>
              <v-tab class="coko-tab" value="report">Отчеты</v-tab>
            </v-tabs>

            <SurveyBase
              v-if="surveyTab === 'base'"
            />

            <SurveyTarget
              v-if="surveyTab === 'target'"
            />

            <SurveyReport
              v-if="surveyTab === 'report'"
            />

          </div>
        </v-card-text>
      </v-card>
    </slot>
  </LkPage>

</template>

<script>

// Основной компонент меню опросов
import LkPage from "@/components/LkPage.vue";
import SurveyBase from "@/views/administrator/surveys/SurveyBase.vue";
import SurveyTarget from "@/views/administrator/surveys/SurveyTarget.vue";
import SurveyReport from "@/views/administrator/surveys/SurveyReport.vue";

export default {
  name: 'Surveys',
  components: {SurveyReport, SurveyTarget, SurveyBase, LkPage, },
  props: {
    usePreLoader: Function,
  },
  data() {
    return {
      // Выбранная вкладка опросов
      surveyTab: 'base'
    }
  }
}

</script>

<style scoped>

</style>