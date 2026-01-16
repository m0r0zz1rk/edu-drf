<template>
  <div
      v-if="ui === 'journalModule'"
      v-bind:class="{'v-data-table__td-value': mobileDisplay}"
  >
    <JournalModuleBadge :moduleName="item[header.key]" />
  </div>

  <div
      v-if="ui === 'journalRecStatus'"
      v-bind:class="{'v-data-table__td-value': mobileDisplay}"
  >
    <JournalRecStatusBadge :recStatus="item[header.key]" />
  </div>

  <div
      v-if="ui === 'journalDetailInfo'"
      v-bind:class="{'v-data-table__td-value': mobileDisplay}"
  >
    <JournalDetailInfoDialog :item="item" />
  </div>

  <div
    v-if="ui === 'cokoCuratorGroups'"
    v-bind:class="{'v-data-table__td-value': mobileDisplay}"
  >
    <CuratorGroupsField :item="item" />
  </div>

  <div
    v-if="ui === 'dppOrder'"
    v-bind:class="{'v-data-table__td-value': mobileDisplay}"
  >
    <ProgramOrderField :item="item" />
  </div>

  <div
    v-if="ui === 'studentGroupStatus'"
    v-bind:class="{'v-data-table__td-value': mobileDisplay}"
  >
    <StudentGroupStatusBadge :studentGroupStatus="item.status" />
  </div>

  <div
    v-if="ui === 'file'"
  >
    <v-icon
      v-if="item.pay_doc_id !== null"
      color="coko-blue"
      icon="mdi-file-document-outline"
      @click="openDocViewerFunction(
        'Просмотр документа',
        item.object_id,
        'Документ',
        'student'
      )"
    />
  </div>

  <AppStudentInfo
    v-if="ui === 'appStudentInfo'"
    :studentInfo="item[header.key]"
  />

  <AppMove
    v-if="ui === 'appMove'"
    :application="item"
    :appMoveFunction="appMoveFunction"
  />

  <AppStatusBadge
    v-if="ui === 'appStatus'"
    :appStatus="item[header.key]"
  />

  <BooleanBadge
    v-if="ui === 'appOoCheck'"
    :bool="item.oo_new === ''"
  />

  <div
    v-if="ui === 'appEducationCheck'"
  >
    <BooleanBadge
        :bool="item.education_check"
    />&nbsp;
    <v-icon
      v-if="item.education_doc_id !== null"
      color="coko-blue"
      icon="mdi-file-document-outline"
      @click="openDocViewerFunction(
          item.student.display_name,
          item.education_doc_id,
          item.education_doc_name,
          'student'
      )"
    />

  </div>

  <div
    v-if="ui === 'appCertificateScan'"
  >
    <BooleanBadge :bool="item.scan !== null" />&nbsp;
    <v-icon
      v-if="item.scan !== null"
      color="coko-blue"
      icon="mdi-file-document-outline"
      @click="openDocViewerFunction(
          item.student.display_name,
          item.scan,
          'Скан удостоверения',
          'student'
      )"
    />

  </div>

  <div
      v-if="ui === 'appPayCheck'"
  >
    <v-icon
      v-if="item.pay_doc_id === null || item.status === 'wait_pay'"
      color="coko-blue"
      icon="mdi-upload"
      @click="$refs[`payUpload_${item.student.profile_id}`].dialog = true"
    />
    <CokoDialog :ref="`payUpload_${item.student.profile_id}`" :cardActions="true">
      <template v-slot:title>
        Загрузить документ об оплате обучающегося "{{item.student.display_name}}"
      </template>

      <template v-slot:text>
        <VFileInput v-model="payFiles[item.student.profile_id]" label="Выберите документ об оплате" />
      </template>

      <template v-slot:actions>
        <v-btn
          variant="flat"
          :loading="loading"
          color="coko-blue"
          text="Сохранить"
          @click="savePayDoc(item)"
        />
      </template>

    </CokoDialog>
    <BooleanBadge
        :bool="['pay', 'study', 'study_complete', 'archive'].includes(item.status)"
    />
    <v-icon
        v-if="item.pay_doc_id !== null"
        color="coko-blue"
        icon="mdi-file-document-outline"
        @click="openDocViewerFunction(
          item.student.display_name,
          item.pay_doc_id,
          item.pay_doc_name,
          'pay'
      )"
    />

  </div>

  <v-icon
    v-if="ui === 'appFormView'"
    icon="mdi-list-box-outline"
    @click="item.student ?
      selectGroupAppFunction(
          item.student.display_name,
          item.object_id
      )
      :
      selectGroupAppFunction(
          item.group_code,
          item.object_id
      )
    "
  />

  <BooleanBadge
    v-if="ui === 'appSurveyCheck'"
    :bool="item[header.key]"
  />

</template>

<script>
import JournalRecStatusBadge from "@/components/badges/journal/JournalRecStatusBadge.vue";
import JournalModuleBadge from "@/components/badges/journal/JournalModuleBadge.vue";
import JournalDetailInfoDialog from "@/components/dialogs/journal/JournalDetailInfoDialog.vue";
import CuratorGroupsField from "@/components/tables/pagination_table/special_fields/sources/CuratorGroupsField.vue";
import ProgramOrderField from "@/components/tables/pagination_table/special_fields/sources/ProgramOrderField.vue";
import StudentGroupStatusBadge from "@/components/badges/edu/StudentGroupStatusBadge.vue";
import fileContentTypes from "@/commons/consts/fileContentTypes";
import FileField from "@/components/tables/pagination_table/special_fields/sources/FileField.vue";
import AppStudentInfo from "@/components/tables/pagination_table/special_fields/sources/AppStudentInfo.vue";
import AppStatusBadge from "@/components/badges/students/AppStatusBadge.vue";
import BooleanBadge from "@/components/badges/BooleanBadge.vue";
import AppMove from "@/components/tables/pagination_table/special_fields/sources/AppMove.vue";
import CokoDialog from "@/components/dialogs/CokoDialog.vue";
import {showAlert} from "@/commons/alerts";
import {apiRequest} from "@/commons/apiRequest";
import {getBase64} from "@/commons/files";

export default {
  name: "SpecialField",
  components: {
    CokoDialog,
    AppMove,
    BooleanBadge,
    AppStatusBadge,
    AppStudentInfo,
    FileField,
    StudentGroupStatusBadge,
    ProgramOrderField, CuratorGroupsField, JournalDetailInfoDialog, JournalModuleBadge, JournalRecStatusBadge},
  props: {
    ui: String, // Тип поля,
    header: Object, // Заголовок пагинационной таблицы
    item: Object, // Запись таблицы,
    mobileDisplay: Boolean, // Отображение на экране мобильного устройства
    // Функция для просмотра документов
    openDocViewerFunction: Function,
    // Функция для получения полной заявки и просмотра анкеты в группе
    selectGroupAppFunction: Function,
    // Функция получения записей в таблице
    getRecs: Function,
    // Функция для выбора заявки и подготовки к ее переносу
    appMoveFunction: Function
  },
  data() {
    return {
      // Список соответствий расширения файла и MIME типа
      fileContentTypes: fileContentTypes,
      // Объект с документами об оплате
      payFiles: {},
      // Параметр лоадера на форме
      loading: false
    }
  },
  methods: {
    // Подгрузка документа об оплате
    async savePayDoc(item) {
      const profile_id = item.student.profile_id
      const files = this.payFiles[profile_id]
      if (!files) {
        showAlert('error', 'Загрузка файла', 'Выберите документ об оплате')
        return
      }
      let formData = new FormData()
      const base64file = await getBase64(files)
      formData.append("profile_id", profile_id)
      formData.append("app_id", item.object_id)
      formData.append("file",base64file)
      this.loading = true
      const saveAppRequest = await apiRequest(
        '/backend/api/v1/docs/pay_doc/create/',
        'POST',
        true,
        formData,
        false,
        true
      )
      if (saveAppRequest.error) {
        showAlert(
          'error',
          'Сохранение заявки',
          saveAppRequest.error
        )
      } else {
        showAlert(
          'success',
          'Сохранение заявки',
          saveAppRequest.success
        )
        this.getRecs()
      }
      this.loading = false
    }
  }
}
</script>



<style scoped>

</style>
