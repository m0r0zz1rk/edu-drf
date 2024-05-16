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
</template>

<script>
import JournalRecStatusBadge from "@/components/badges/journal/JournalRecStatusBadge.vue";
import JournalModuleBadge from "@/components/badges/journal/JournalModuleBadge.vue";
import JournalDetailInfoDialog from "@/components/dialogs/JournalDetailInfoDialog.vue";
import CuratorGroupsField from "@/components/pagination_table/special_fields/sources/CuratorGroupsField.vue";

export default {
  name: "SpecialField",
  components: {CuratorGroupsField, JournalDetailInfoDialog, JournalModuleBadge, JournalRecStatusBadge},
  props: {
    ui: String, // Тип поля,
    header: Object, // Заголовок пагинационной таблицы
    item: Object, // Запись таблицы,
    mobileDisplay: Boolean, // Отображение на экране мобильного устройства
  }
}
</script>



<style scoped>

</style>
