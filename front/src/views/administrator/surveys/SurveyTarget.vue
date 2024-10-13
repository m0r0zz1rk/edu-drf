<template>

  <PaginationTable
      ref="surveyTargetTable"
      tableTitle="Таргетирования опросов"
      tableWidth="98"
      :noTab="false"
      :addButton="true"
      :xlsxButton="false"
      getRecsURL="/backend/api/v1/surveys/survey_target/"
      addRecURL="/backend/api/v1/surveys/survey_target/"
      :tableHeaders="tableHeaders"
      :fieldsArray="fieldsArray"
      :itemSelectEvent="selectTarget"
      :addSpecialFunction="newTarget"
  />

  <SurveyTargetDetail
    ref="surveyTargetDetail"
    :getTargets="getTargets"
  />

</template>

<script>

// Страница для работы с таргетированием опросов
import PaginationTable from "@/components/tables/pagination_table/PaginationTable.vue";
import SurveyTargetDetail from "@/components/forms/surveys/SurveyTargetDetail.vue";
import surveyTargetTypes from "@/commons/consts/survey/surveyTargetTypes";

export default {
  name: 'SurveyTarget',
  components: {SurveyTargetDetail, PaginationTable},
  data() {
    return {
      // Заголовки таблицы
      tableHeaders: [
        {
          'title': 'Опрос',
          'key': 'survey_description'
        },
        {
          'title': 'Тип назначения',
          'key': 'type'
        },
      ],
      // Описание полей таблицы
      fieldsArray: []
    }
  },
  methods: {
    // Формирование списка названий типов таргетирования и списка описаний столбцов таблицы
    startFunc() {
      let types = []
      surveyTargetTypes.map((t) => {
        types.push(t.title)
      })
      this.fieldsArray = [
        {
          ui: 'input',
          type: 'text',
          key: 'survey_description',
          addRequired: false
        },
        {
          ui: 'select',
          items: types,
          key: 'type',
          addRequired: true,
        },
      ]
    },
    // Получение списка записей назначений
    getTargets() {
      this.$refs.surveyTargetTable.getRecs()
    },
    // Открыть форму Detail для добавления нового таргетирования
    newTarget() {
      this.$refs.surveyTargetDetail.surveyTarget = {
        'survey_id': null,
        'survey_description': '(Не выбран)',
        'type': '',
        'group_id': null,
        'group_code': '(Не выбрана)'
      }
      this.$refs.surveyTargetDetail.newTarget = true
      this.$refs.surveyTargetDetail.dialog = true
    },
    // Выбор таргетирования
    selectTarget(target) {
      this.$refs.surveyTargetDetail.surveyTarget = target
      this.$refs.surveyTargetDetail.newTarget = false
      this.$refs.surveyTargetDetail.dialog = true
    }
  },
  mounted() {
    this.startFunc()
  }
}

</script>

<style scoped>

</style>