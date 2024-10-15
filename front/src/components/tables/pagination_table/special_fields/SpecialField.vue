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
    <FileField
      :file="item.file"
      :fileName="item.doc_name"
    />
  </div>

  <AppStudentInfo
    v-if="ui === 'appStudentInfo'"
    :studentInfo="item[header.key]"
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
    <v-btn
      v-if="item.education_doc_id !== null"
      color="coko-blue"
      @click="openDocViewerFunction(
          item.student.display_name,
          item.education_doc_id,
          item.education_doc_name,
          'student'
      )"
    >
      <v-icon
        icon="file-document-outline"
      />
    </v-btn>

  </div>

  <div
      v-if="ui === 'appPayCheck'"
  >
    <BooleanBadge
        :bool="item.status in ['pay', 'study', 'study_complete', 'archive']"
    />

  </div>

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

export default {
  name: "SpecialField",
  components: {
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
