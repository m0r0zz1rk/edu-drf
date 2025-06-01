<template>
  <LkPage :usePreLoader="usePreLoader">
    <slot>
      <v-card
        variant="outlined"
      >
        <v-card-text>
          <div style="background-color: white; overflow: auto;" class="adaptive-no-tab-table-card-text">
            <PaginationTable
              tableTitle="Журнал событий"
              :noTab="true"
              tableWidth="98"
              :addButton="false"
              :xlsxButton="false"
              getRecsURL="/backend/api/v1/journal/journal/"
              :tableHeaders="tableHeaders"
              :fieldsArray="fieldsArray"
            />
          </div>
        </v-card-text>
      </v-card>
    </slot>
  </LkPage>
</template>

<script>
import LkPage from "@/components/LkPage.vue";
import PaginationTable from "@/components/tables/pagination_table/PaginationTable.vue";
import systemModules from "@/commons/consts/systemModules";
import journalRecStatuses from "@/commons/consts/journalRecStatuses";

export default {
  name: "Journal",
  components: {PaginationTable, LkPage},
  props: {
    usePreLoader: Function,
  },
  data() {
    return {
      tableHeaders: [
        {
          'title': 'Дата создания',
          'key': 'date_create'
        },
        {
          'title': 'Источник',
          'key': 'source'
        },
        {
          'title': 'Модуль',
          'key': 'module'
        },
        {
          'title': 'Статус',
          'key': 'status'
        },
        {
          'title': 'Описание',
          'key': 'description'
        },
        {
          'title': 'Подробно',
          'key': 'journalDetailInfo',
        },
      ],
      fieldsArray: [
        {
          ui: 'date',
          key: 'date_create',
          addRequired: false,
        },
        {
          ui: 'input',
          type: 'text',
          key: 'source',
          addRequired: false,
        },
        {
          ui: 'journalModule',
          items: systemModules,
          key: 'module',
          addRequired: false,
        },
        {
          ui: 'journalRecStatus',
          items: journalRecStatuses,
          key: 'status',
          addRequired: false,
        },
        {
          ui: 'input',
          key: 'description',
          addRequired: false,
        },
        {
          ui: 'journalDetailInfo',
          key: 'journalDetailInfo',
          addRequired: false,
        }
      ]
    }
  },
  mounted() {
    this.usePreLoader(true)
  }
}
</script>

<style scoped>

</style>
