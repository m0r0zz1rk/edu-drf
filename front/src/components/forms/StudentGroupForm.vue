<template>

    <v-card
      variant="outlined"
      class="lk-full-page-card"
    >

      <v-card-title class="d-flex justify-space-between align-center">

          Управление учебной группой {{code}}

      </v-card-title>

      <v-card-text class="adaptive-tab-table-card-text" style="padding: 0;">

        <v-tabs
          style="width: 100%; top: 0; z-index: 10; position: sticky"
          v-model="groupTab"
          bg-color="coko-blue"
          show-arrows
        >

          <v-tab
            class="coko-tab"
            value="info"
          >
            Информация
          </v-tab>

          <v-tab
            class="coko-tab"
            value="manage"
          >
            Управление
          </v-tab>

          <v-tab
            class="coko-tab"
            value="docs"
          >
            Документы
          </v-tab>

          <v-tab
            class="coko-tab"
            value="apps"
          >
            Участники
          </v-tab>

          <v-tab
            class="coko-tab"
            value="schedule"
          >
            Расписание
          </v-tab>

          <v-tab
            v-if="serviceType === 'ou'"
            class="coko-tab"
            value="cert"
          >
            Удостоверения
          </v-tab>

        </v-tabs>

        <StudentGroupInfo
          v-if="groupTab === 'info'"
          :setCode="setCode"
          :groupId="groupId"
        />

        <StudentGroupManage
          ref="groupManage"
          v-if="groupTab === 'manage'"
          :groupId="groupId"
        />

        <StudentGroupDocs
          v-if="groupTab === 'docs'"
          :groupId="groupId"
          :serviceType="serviceType"
        />

        <StudentGroupSchedule
            v-if="groupTab === 'schedule'"
            :groupId="groupId"
        />

      </v-card-text>

      <v-card-actions

        style="background-color: white"
      >

        <v-spacer></v-spacer>

        <v-btn
          v-if="groupTab === 'manage'"
          color="coko-blue"
          text="Сохранить"
          :loading="loading"
          @click="saveGroup()"
        ></v-btn>
      </v-card-actions>

    </v-card>

</template>

<script>
import LkPage from "@/components/LkPage.vue";
import StudentGroupInfo from "@/components/forms/student_group/StudentGroupInfo.vue";
import StudentGroupManage from "@/components/forms/student_group/StudentGroupManage.vue";
import {apiRequest} from "@/commons/api_request";
import {hideAlert, showAlert} from "@/commons/alerts";
import studentGroupStatuses from "@/commons/consts/studentGroupStatuses";
import StudentGroupDocs from "@/components/forms/student_group/StudentGroupDocs.vue";
import studyForms from "@/commons/consts/studyForms";
import StudentGroupSchedule from "@/components/forms/student_group/StudentGroupSchedule.vue";

export default {
  name: "StudentGroupForm",
  components: {StudentGroupSchedule, StudentGroupDocs, StudentGroupManage, StudentGroupInfo, LkPage},
  props: {
    groupId: String, // object_id учебной группы
  },
  data() {
    return {
      groupTab: 'info', // Выбранная вкладка на форме
      loading: false, // Параметр отображения анимации загрузки на элементах формы
      code: '', // Код учебной группы
      serviceType: '', // Тип услуги учебной группы
    }
  },
  methods: {
    // Сохранить информацию по учебной группе
    async saveGroup() {
      hideAlert('error')
      let groupInfo = this.$refs.groupManage.studentGroup
      if ((groupInfo.code === null) || (groupInfo.code.length === 0)) {
        showAlert(
          'error',
          'Изменение информации',
          'Некорректный шифр учебной группы'
        )
        return false
      }
      if (studentGroupStatuses.filter((status) => status.key === groupInfo['status']).length === 0) {
        groupInfo['status'] = studentGroupStatuses.filter((status) => status.title === groupInfo['status'])[0].key
      }
      if (studyForms.filter((form) => form.key === groupInfo['form']).length === 0) {
        groupInfo['form'] = studyForms.filter((form) => form.title === groupInfo['form'])[0].key
      }
      console.log(groupInfo)
      this.loading = true
      let updateRequest = await apiRequest(
        '/backend/api/v1/edu/student_group/'+this.groupId+'/',
        'PATCH',
        true,
        groupInfo
      )
      if (updateRequest.error) {
        showAlert('error', 'Обновление информации', updateRequest.error)
        return false
      } else {
        showAlert('success', 'Обновление информации', updateRequest.success)
        this.groupTab = 'info'
      }
      this.loading = false
    },
    // Получить тип услуги учебной группы
    async getServiceType() {
      let serviceTypeRequest = await apiRequest(
        '/backend/api/v1/edu/student_group_service_type/'+this.groupId+'/',
        'GET',
        true,
        null
      )
      if (serviceTypeRequest.error) {
        showAlert('error', 'Получение типа услуги учебной группе', serviceTypeRequest.error)
        return false
      } else {
        this.serviceType = serviceTypeRequest.service_type
      }
    },
    // Установить код учебной группы для отображения в шапке формы
    setCode(code) {
      this.code = code
    }
  },
  mounted() {
    this.getServiceType()
  }
}
</script>

<style scoped>

</style>
