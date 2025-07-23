<template>

  <CokoDialog
    ref="courseDetailDialog"
    :cardActions="true"
  >

    <template v-slot:title>
      Информация
    </template>

    <template v-slot:text>
      Наименование услуги:<br/>
      <b>{{serviceInfo.title}}</b>
      <br/><br/>
      Шифр группы:<br/>
      <b>{{serviceInfo.code}}</b>
      <br/><br/>
      Сроки обучения:<br/>
      <b>{{serviceInfo.date_start}}-{{serviceInfo.date_end}}</b>
      <br/><br/>
      Тип:<br/>
      <b>{{serviceInfo.type}}</b>
      <br/><br/>
      Объем (часов):<br/>
      <b>{{serviceInfo.duration}}</b>
      <br/><br/>
      Структурное подразделение:<br/>
      <b>{{department}}</b>
      <br/><br/>
      Куратор:<br/>
      <template v-if="serviceInfo.curator_fio === '-'">
        <b>(Куратор не назначен)</b>
      </template>
      <template v-if="serviceInfo.curator_fio !== '-'">
        <b>{{serviceInfo.curator_fio}}</b>
        <br/><br/>
        Контактный телефон куратора: <br/>
        <b>+7 3952 500-287 (вн. {{serviceInfo.curator_phone}})</b>
        <br/><br/>
        Email куратора:<br/>
        <b>{{serviceInfo.curator_email}}</b>
      </template>
    </template>

    <template v-slot:actions>
      <v-btn
        variant="flat"
          color="coko-blue"
          text="Подать заявку"
          :loading="loading"
          @click="createApp()"
      ></v-btn>
    </template>

  </CokoDialog>

</template>

<script>

// Диалоговое окно для просмотра детальной информации по услуге и подачи заявки
import CokoDialog from "@/components/dialogs/CokoDialog.vue";
import {apiRequest} from "@/commons/apiRequest";
import {showAlert} from "@/commons/alerts";

export default {
  name: 'ServiceDetail',
  components: {CokoDialog},
  props: {
    // Подразделение ЦОКО, проводящее курс
    department: String,
    // Тип услуги (course или event)
    serviceType: String,
    // Информация по выбранному курсу
    serviceInfo: Object
  },
  data() {
    return {
      // Параметр отображения загрузки на кнопке "Подать заявку"
      loading: false
    }
  },
  methods: {
    // Открыть диалоговое окно
    openDialog() {
      this.$refs.courseDetailDialog.dialog = true
    },
    // Подать заявку на курсу
    async createApp() {
      this.loading = true
      let url = '/backend/api/v1/applications/'
      if (this.serviceType === 'course') {
        url += 'course_application_user/'
      } else {
        url += 'event_application_user/'
      }
      try {
        const createAppRequest = await apiRequest(
          url,
          'POST',
          true,
          {
            group_id: this.serviceInfo.object_id
          }
        )
        if (createAppRequest.error) {
          showAlert(
            'error',
            'Подача заявки',
            createAppRequest.error
          )
          this.$refs.courseDetailDialog.dialog = false
        } else {
          showAlert(
            'success',
            'Подача заявки',
            'Заявка успешно создана'
          )
          this.$router.push({
            path: '/student/app/'+this.serviceType+'/'+createAppRequest.app_id
          })
        }
      } catch(e) {
        console.log('ou_service save error: ', e)
        showAlert(
          'error',
          'Подача заявки',
          'Произошла ошибка в процессе выполнения запроса'
        )
      }

      this.loading = false
    }
  }
}

</script>

<style scoped>

</style>
