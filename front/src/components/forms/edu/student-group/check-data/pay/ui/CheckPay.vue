<template>
  <template v-if="internalPayData === null">Пожалуйста, подождите..</template>
  <template v-else>
    <v-alert
      v-if="internalPayData.length === 0"
      color="success"
      icon="$success"
      title="Проверка ОО"
      text="Все документы были проверены"
    />
    <template v-if="internalPayData.length > 0 & payApp !== null">
      <table style="width: 100%">
        <tr>
          <td style="width: 50%; align-content: flex-start">
            <v-text-field readonly label="ФИО обучающегося" v-model="payApp.student" :loading="loading"/>
            <v-text-field
              v-if="mobileDisplay"
              readonly
              label="Документ об оплате"
              v-model="docText"
              :loading="loading"
              @click="e => openDocViewerDialog()"
            />
            <v-text-field label="Причина отказа" v-model="rejectReason" :loading="loading"/>
            <v-card v-if="internalPayData.length > 0 & payApp !== null">
              <v-card-actions>
                <v-spacer />
                <v-btn color="coko-blue" text="Пропустить" :loading="loading" @click="getNext()" />
                <v-btn color="coko-blue" text="Отклонить" :loading="loading" @click="payReject()" />
                <v-btn color="coko-blue" text="Подтвердить" :loading="loading" @click="saveData()" />
              </v-card-actions>
            </v-card>
            <CokoDialog ref="docViewerDialog" v-if="mobileDisplay && payApp !== null">
              <template v-slot:title>Документ об оплате {{payApp.student}}</template>
              <template v-slot:text>
                <DocViewer fileType="pay" :fileId="payApp.pay_doc_id"/>
              </template>
            </CokoDialog>
          </td>
          <td style="width: 50%; align-content: flex-start" v-if="!mobileDisplay">
            <b style="top: 0">Документ об оплате</b><br/>
            <b v-if="payApp.pay_doc_id === null">Нет документа</b>
            <div v-else :key="key" style="width: 100%; height: 60vh; overflow: auto">
              <DocViewer fileType="pay" :fileId="payApp.pay_doc_id"/>
            </div>
          </td>
        </tr>
      </table>

    </template>

  </template>

</template>

<script>
// Проверка оплаты в заявках учебных групп
import {endpoints} from "@/commons/endpoints";
import {apiRequest} from "@/commons/apiRequest";
import {showAlert} from "@/commons/alerts";
import DocViewer from "@/components/DocViewer.vue";
import CokoDialog from "@/components/dialogs/CokoDialog.vue";
import {useDisplay} from "vuetify";

export default {
  name: "CheckPay",
  components: {CokoDialog, DocViewer},
  props: {
    // object_id учебной группы
    groupId: String,
    // Тип услуги (ou или iku)
    serviceType: String,
    // Список данных для проверки
    payData: Array,
    // Функция изменения объекта со списками заявок на проверку данных
    changeCheckData: Function,
    // Функция обновления таблицы на вкладке "Заявки"
    updateApps: Function
  },
  data() {
    return {
      // Параметр проверки мобильного устройства
      mobileDisplay: useDisplay().smAndDown,
      // Индекс для массива данных
      index: 0,
      // Текущая заявка на редактирование
      payApp: null,
      // Индикатор лоадера
      loading: false,
      // Внутренний список с заявками для проверки ОО
      internalPayData: null,
      // Текст поля для просмотра документа об оплате
      docText: 'Нажмите для просмотра',
      // Текст с причиной отказа, отправляемый пользователю по email
      rejectReason: '',
      key: 0
    }
  },
  methods: {
    // Установка первой заявки при рендере компонента и списка заявок
    setFirstAppAndInternalPayData() {
      this.internalPayData = this.payData
      this.payApp = this.payData[0]
    },
    // Получить следующую заявку из списка
    getNext(afterSave = false) {
      this.payApp = null
      if (!afterSave) {
        if (this.internalPayData.length === 0) { return }
        if (this.index >= this.internalPayData.length - 1) { this.index = -1 }
        this.index++
      }
      this.payApp = this.internalPayData[this.index]
    },
    // Открыть диалоговое окно для просмотра документа
    openDocViewerDialog() {
      this.$refs.docViewerDialog.dialog = true
    },
    // Запрос на отклонение оплаты
    async payReject() {
      if (this.rejectReason === '') {
        showAlert('error', 'Проверка оплаты', 'Заполните причину отказа'); return
      }
      if (confirm(`Вы уверены, что хотите отколнить оплату ${this.payApp.student} ?`)) {
        this.loading = true
        let url = endpoints['coursePayDenied']
        if (this.serviceType === 'iku') { url = endpoints['eventPayDenied'] }
        const payDeniedRequest = await apiRequest(
          `${url}${this.payApp.app_id}/`,
          'POST',
          true,
          {
            'message': this.rejectReason
          },
          true
        )
        if (payDeniedRequest.status === 200) {
          showAlert('success', 'Проверка оплаты', 'Оплата успешно отклонена')
          this.updateApps()
          this.internalPayData = this.internalPayData.filter((rec) => rec.app_id !== this.payApp.app_id)
          this.loading = false
          this.getNext(true)
        } else {
          showAlert('error', 'Проверка оплаты', 'Ошибка при обновлении информации в заявке')
        }
      }
    },
    // Зафиксировать данные и перейти к следующей заявке
    async saveData() {
      this.loading = true
      let url = endpoints['courseApplicationAdmin']
      if (this.serviceType === 'iku') { url = endpoints['eventApplicationAdmin'] }
      const paySaveRequest = await apiRequest(
        `${url}${this.payApp.app_id}/`,
        'PATCH',
        true,
        {
          'status': 'pay'
        },
        true
      )
      if (paySaveRequest.status === 200) {
        this.updateApps()
        showAlert('success', 'Проверка оплаты', 'Информация успешно сохранена')
        this.internalPayData = this.internalPayData.filter((rec) => rec.app_id !== this.payApp.app_id)
        this.loading = false
        this.getNext(true)
      } else {
        showAlert('error', 'Проверка оплаты', 'Ошибка при обновлении информации в заявке')
      }
    },
  },
  mounted() {
    this.setFirstAppAndInternalPayData()
  },
  watch: {
    payApp: function() {this.key += 1},
    internalPayData: function(newValue, oldValue) {
      if (!([newValue, oldValue].includes(null)) && newValue !== this.payData) {
        this.changeCheckData('pay', newValue)
      }
    }
  }
}
</script>

<style scoped>

</style>
