<template>
  <div v-if="paymentData === null"><b>Пожалуйста, подождите...</b></div>

  <div v-else>
    <table>
      <tr>
        <td style="text-align: right;">Договор оферты:</td>
        <td style="text-align: center;"><v-btn color="coko-blue" text="Просмотр" :loading="loading" @click="openDocViewerDialog()"/></td>
        <td style="text-align: center;"></td>
      </tr>
      <tr>
        <td style="text-align: right;">Документ об оплате:</td>
        <td style="text-align: center;">
          <v-btn
            v-if="paymentData.pay_doc_id !== null"
            color="coko-blue"
            text="Просмотр"
            :loading="loading"
            @click="openDocViewerDialog('pay')"
          />
          <p v-else><b>-</b></p>
        </td>
        <td style="text-align: center;">
          <v-btn
            v-if="app.status === 'wait_pay'"
            color="coko-blue"
            text="Загрузить"
            :loading="loading"
            @click="$refs.uploadPayDocDialog.dialog = true"
          />
        </td>
      </tr>
    </table>
    <div v-if="paymentData.message !== null">
      <br/>
      <b>Комментарий об отклоненной оплате: </b> {{paymentData.message}}
    </div>
  </div>

  <CokoDialog ref="docViewerDialog" v-if="paymentData !== null">
    <template v-slot:title>{{docViewerTitle}}</template>
    <template v-slot:text><DocViewer :fileType="docViewerType" :fileId="docViewerId"/></template>
  </CokoDialog>

  <CokoDialog ref="uploadPayDocDialog" :cardActions="true">
    <template v-slot:title>Загрузка документа об оплате</template>
    <template v-slot:text>
      <v-file-input :loading="loading" v-model="payDocFile"/>
    </template>
    <template v-slot:actions>
      <v-btn color="coko-blue" text="Загрузить" :loading="loading" @click="savePayDoc()"/>
    </template>
  </CokoDialog>

</template>

<script>
import DocViewer from "@/components/DocViewer.vue";
import CokoDialog from "@/components/dialogs/CokoDialog.vue";
import {apiRequest} from "@/commons/apiRequest";
import {showAlert} from "@/commons/alerts";
import {getBase64} from "@/commons/files";

export default {
  name: "AppPayment",
  props: {
    // Объект заявки
    app: Object,
    // Тип заявки (course, event)
    appType: String,
    // Функция для обновления формы с заявкой
    updateAppForm: Function
  },
  components: {CokoDialog, DocViewer},
  data() {
    return {
      // Данные по оплате
      paymentData: null,
      // Заголовок диалогового окна для просмотра документа
      docViewerTitle: 'Договор офферы',
      // Тип файла для просмотра
      docViewerType: 'offer',
      // ID файла для просмотра
      docViewerId: null,
      // Параметр блокировки элементов формы
      loading: false,
      // Документ об оплате для загрузки
      payDocFile: null
    }
  },
  methods: {
    // Открыть диалоговое окно для просмотра документа
    openDocViewerDialog(type = 'offer') {
      this.docViewerType = type
      if (type === 'offer') {
        this.docViewerTitle = 'Догофор оферты'
        this.docViewerId = this.paymentData.offer_id
      } else {
        this.docViewerTitle = 'Документ об оплате'
        this.docViewerId = this.paymentData.pay_doc_id
      }
      this.$refs.docViewerDialog.dialog = true
    },
    // Функция для получения данных об оплате по заявке
    async getPaymentData() {
      this.paymentData = await apiRequest(
        `/backend/api/v1/applications/${this.appType}_application_user/payment/${this.app.object_id}/`,
        'GET',
        true,
        null
      )
    },
    // Загрузка документа об оплате
    async savePayDoc() {
      if (this.payDocFile === null) {
        showAlert('error', 'Документ об оплате', 'Выберите документ')
        return
      }
      this.loading = true
      let formData = new FormData()
      const base64file = await getBase64(this.payDocFile)
      formData.append('file', base64file)
      formData.append('profile_id', this.app.profile_id)
      formData.append('app_id', this.app.object_id)
      const savePayDocRequest = await apiRequest(
        '/backend/api/v1/docs/pay_doc/create/',
        'POST',
        true,
        formData,
        false,
        true
      )
      if (savePayDocRequest.success) {
        showAlert('success', 'Документ об оплате', 'Документ успешно сохранен')
        this.$refs.uploadPayDocDialog.close()
        await this.updateAppForm()
      } else {
        showAlert('error', 'Документ об оплате', savePayDocRequest.error)
      }
      this.loading = false
    }
  },
  mounted() {
    this.getPaymentData()
  }
}
</script>


<style scoped>

</style>
