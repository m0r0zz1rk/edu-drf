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
                v-model="reportTab"
                bg-color="coko-blue"
                show-arrows
            >
              <v-tab class="coko-tab" value="dpp">Перечень ДПП</v-tab>
              <v-tab class="coko-tab" value="service">График услуг</v-tab>
              <v-tab class="coko-tab" value="pk-1">1-ПК</v-tab>
              <v-tab class="coko-tab" value="frdo">ФИС ФРДО</v-tab>
              <v-tab class="coko-tab" value="forms">Анкеты</v-tab>
            </v-tabs>

            <DppList
              v-if="reportTab === 'dpp'"
            />

            <ServiceChart
                v-if="reportTab === 'service'"
            />

            <PkOne
              v-if="reportTab === 'pk-1'"
            />

            <FisFrdo
              v-if="reportTab === 'frdo'"
            />

            <ReportForms
              v-if="reportTab === 'forms'"
            />

          </div>
        </v-card-text>
      </v-card>
    </slot>
  </LkPage>

</template>

<script>

// Главая страница меню "Отчеты"
import LkPage from "@/components/LkPage.vue";
import DppList from "@/views/administrator/reports/DppList.vue";
import ServiceChart from "@/views/administrator/reports/ServiceChart.vue";
import PkOne from "@/views/administrator/reports/PkOne.vue";
import FisFrdo from "@/views/administrator/reports/FisFrdo.vue";
import ReportForms from "@/views/administrator/reports/ReportForms.vue";

export default {
  name: 'Reports',
  components: {ReportForms, FisFrdo, PkOne, ServiceChart, DppList, LkPage,},
  data() {
    return {
      // Выбранная вкладка отчетов
      reportTab: 'dpp'
    }
  }
}

</script>

<style scoped>

</style>