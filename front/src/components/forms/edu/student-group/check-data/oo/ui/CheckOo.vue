<template>

  <template
    v-if="internalOoData === null"
  >
    Пожалуйста, подождите..
  </template>

  <template
    v-else
  >

    <v-alert
      v-if="internalOoData.length === 0"
      color="success"
      icon="$success"
      title="Проверка ОО"
      text="Все данные были проверены"
    />

    <template
      v-if="internalOoData.length > 0 & ooApp !== null"
    >

      <v-text-field
        readonly
        label="ФИО обучающегося"
        v-model="ooApp.student"
        :loading="loading"
      />

      <v-text-field
        readonly
        label="МО в заявке"
        v-model="ooApp.mo"
        :loading="loading"
      />

      <v-text-field
        readonly
        label="ОО в заявке"
        v-model="ooApp.oo_new"
        :loading="loading"
      />

      <v-text-field
        readonly
        label="Выбранное ОО из базы"
        v-model="correctOoName"
        :loading="loading"
        @click="e => $refs.selectOoDialog.dialog = true"
      />

      <v-card
        v-if="internalOoData.length > 0 & ooApp !== null"
      >

        <v-card-actions>

          <v-spacer />

          <v-btn
            color="coko-blue"
            text="Пропустить"
            :loading="loading"
            @click="getNext()"
          />

          <v-btn
            :disabled="correctOoId === null"
            color="coko-blue"
            text="Сохранить"
            :loading="loading"
            @click="saveData()"
          />


        </v-card-actions>

      </v-card>

      <CokoDialog
        ref="selectOoDialog"
        v-if="checkData !== null"
      >

        <template v-slot:title>
          База данных ОО
        </template>

        <template v-slot:text>

          <template v-if="fieldsArray === null">
            <b>Подгружаем данные, подождите...</b>
          </template>

          <PaginationTable
            v-if="fieldsArray !== null"
            tableTitle="Выберите ОО"
            tableWidth="98"
            :noTab="false"
            :addButton="true"
            :xlsxButton="false"
            :getRecsURL="`/backend/api/v1/guides/oo/?mo=${ooApp.mo}`"
            addRecURL="/backend/api/v1/guides/oo/"
            :tableHeaders="tableHeaders"
            :fieldsArray="fieldsArray"
            :itemSelectEvent="ooSelect"
            :defaultBody="{'mo': ooApp.mo}"
          />

        </template>

      </CokoDialog>

    </template>

  </template>

</template>

<script>
// Проверка образовательных организаций в заявках учебных групп
import {tableColumns} from "@/commons/table-data/tableColumns";
import PaginationTable from "@/components/tables/pagination_table/PaginationTable.vue";
import {endpoints} from "@/commons/endpoints";
import {apiRequest} from "@/commons/apiRequest";
import {showAlert} from "@/commons/alerts";
import {getOoFieldsArray} from "@/commons/table-data/get-data-for-fields-array/getOoFieldsArray";
import CokoDialog from "@/components/dialogs/CokoDialog.vue";

export default {
  name: "CheckOo",
  components: {CokoDialog, PaginationTable},
  props: {
    // object_id учебной группы
    groupId: String,
    // Тип услуги (ou или iku)
    serviceType: String,
    // Список данных для проверки
    ooData: Array,
    // Функция изменения объекта со списками заявок на проверку данных
    changeCheckData: Function
  },
  data() {
    return {
      // Индекс для массива данных
      index: 0,
      // Текущая заявка на редактирование
      ooApp: null,
      // Индикатор лоадера
      loading: false,
      // Столбцы таблицы для выбора ОО
      tableHeaders: tableColumns['oo'].tableHeaders.filter((th) => !(['actions', 'mo'].includes(th.key))),
      // Описание столбцов таблицы для выбора ОО
      fieldsArray: null,
      // object_id выбранной ОО
      correctOoId: null,
      // Наименование выбранной ОО
      correctOoName: '',
      // Внутренний список с заявками для проверки ОО
      internalOoData: null
    }
  },
  methods: {
    // Установка первой заявки при рендере компонента и списка заявок
    setFirstAppAndInternalOoData() {
      this.internalOoData = this.ooData
      this.ooApp = this.ooData[0]
    },
    // Получить описания столбцов для таблицы
    async getFieldsArray() {
      const ooFA = await getOoFieldsArray()
      this.fieldsArray = ooFA.filter((fa) => !(['actions', 'mo'].includes(fa.key)))
    },
    // Получить следующую заявку из списка
    getNext(afterSave = false) {
      this.ooApp = null
      if (!afterSave) {
        if (this.internalOoData.length === 0) { return }
        if (this.index >= this.internalOoData.length - 1) { this.index = -1 }
        this.index++
      }
      this.ooApp = this.internalOoData[this.index]
    },
    // Хэндлер при выборе корректной ОО из таблицы
    ooSelect(oo) {
      this.correctOoId = oo.object_id
      this.correctOoName = oo.short_name
      this.$refs.selectOoDialog.dialog = false
    },
    // Зафиксировать данные и перейти к следующей заявке
    async saveData() {
      if (this.correctOoId === null) {
        showAlert('error', 'Проверка ОО', 'Выберите ОО')
        return
      }
      this.loading = true
      let url = endpoints['courseApplicationAdmin']
      if (this.serviceType === 'iku') { url = endpoints['eventApplicationAdmin'] }
      const ooSaveRequest = await apiRequest(
        `${url}${this.ooApp.app_id}/`,
        'PATCH',
        true,
        {
          'oo_new': '',
          'oo_id': this.correctOoId
        },
        true
      )
      if (ooSaveRequest.status === 200) {
        showAlert('success', 'Проверка ОО', 'Информация успешно сохранена')
        this.internalOoData = this.internalOoData.filter((rec) => rec.app_id !== this.ooApp.app_id)
        this.correctOoId = null
        this.correctOoName = ''
        this.loading = false
        this.getNext(true)
      } else {
        showAlert('error', 'Проверка ОО', 'Ошибка при обновлении информации в заявке')
      }
    }
  },
  mounted() {
    this.getFieldsArray()
    this.setFirstAppAndInternalOoData()
  },
  watch: {
    internalOoData: function(newValue, oldValue) {
      if (!([newValue, oldValue].includes(null)) && newValue !== this.ooData) {
        this.changeCheckData('oo', newValue)
      }
    }
  }
}
</script>

<style scoped>

</style>
<script setup>
</script>
