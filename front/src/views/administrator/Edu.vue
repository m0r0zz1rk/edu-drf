<template>
  <LkPage :usePreLoader="usePreLoader">
    <slot>
      <v-card
        variant="outlined"
      >
        <v-card-text>

          <div style="background-color: white; overflow: auto;" class="adaptive-no-tab-table-card-text">

            <v-tabs
              v-model="eduTab"
              bg-color="coko-blue"
              show-arrows
            >

              <v-tab class="coko-tab" value="group">Учебные группы</v-tab>
              <v-tab class="coko-tab" value="dpp">ДПП</v-tab>
              <v-tab class="coko-tab" value="ou">Курсы (ОУ)</v-tab>
              <v-tab class="coko-tab" value="iku">Мероприятия (ИКУ)</v-tab>
              <v-tab class="coko-tab" value="planning" v-if="userRole !== 'dep'">Планирование</v-tab>


            </v-tabs>

            <EduDpp
              v-if="eduTab === 'dpp'"
              :userRole="userRole"
              :userDep="userDep"
              :userDepDisplay="userDepDisplay"
            />

            <EduPlanningParameter v-if="eduTab === 'planning' && userRole !== 'dep'" />

            <EducationService
              v-if="eduTab === 'ou'"
              :userRole="userRole"
              :userDep="userDep"
              :userDepDisplay="userDepDisplay"
            />

            <EduInformationService
              v-if="eduTab === 'iku'"
              :userRole="userRole"
              :userDep="userDep"
              :userDepDisplay="userDepDisplay"
            />

            <EduStudentGroup v-if="eduTab === 'group'" :userRole="userRole" />

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
import EduInformationService from "@/views/administrator/edu/EduInformationService.vue";
import EduStudentGroup from "@/views/administrator/edu/EduStudentGroup.vue";
import {getCookie} from "@/commons/cookie";

export default {
  name: "Edu",
  components: {EduStudentGroup, EduInformationService, EducationService, EduPlanningParameter, EduDpp, LkPage},
  props: {
    usePreLoader: Function, // Активация анимации загрузки
  },
  data() {
    return {
      eduTab: 'group',
      // Роль пользователя
      userRole: getCookie('cokoRole'),
      // ObjectGUID подразделения пользователя
      userDep: getCookie('cokoDep'),
      // DisplayName подразделения пользователя
      userDepDisplay: getCookie('cokoDepDisplay')
    }
  },
  mounted() {
    this.usePreLoader(true)
  }
}
</script>

<style scoped>

</style>
