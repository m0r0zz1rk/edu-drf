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

export default {
  name: "SpecialField",
  components: {
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
    // Функция для получения полной заяки и просмотра анкеты в группе
    selectGroupAppFunction: Function,
    // Функция получения записей в таблице
    getRecs: Function,
    // Функция для выбора заявки и подготовки к ее переносу
    appMoveFunction: Function
  },
  data() {
    return {
      // Список соответствий расширения файла и MIME типа
      fileContentTypes: fileContentTypes
    }
  }
}
</script>



<style scoped>

</style>
