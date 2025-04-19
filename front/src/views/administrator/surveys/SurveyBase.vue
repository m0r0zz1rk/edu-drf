<template>

  <PaginationTable
      ref="surveyTable"
      tableTitle="База опросов"
      tableWidth="98"
      :noTab="false"
      :addButton="true"
      :xlsxButton="false"
      getRecsURL="/backend/api/v1/surveys/surveys/"
      addRecURL="/backend/api/v1/surveys/surveys/"
      :tableHeaders="tableHeaders"
      :fieldsArray="fieldsArray"
      :itemSelectEvent="selectSurvey"
  />

  <SurveyDetail
    ref="surveyDetail"
    :getRecs="updateRecs"
  />

</template>

<script>

// Компонент для работы с базой опросов
import PaginationTable from "@/components/tables/pagination_table/PaginationTable.vue";
import SurveyDetail from "@/components/forms/surveys/SurveyDetail.vue";

export default {
  name: 'SurveyBase',
  components: {SurveyDetail, PaginationTable},
  data() {
    return {
      // Заголовки таблицы
      tableHeaders: [
        {
          'title': 'Создатель',
          'key': 'creator_fio'
        },
        {
          'title': 'Описание опроса',
          'key': 'description'
        },
        {
          'title': 'Количество вопросов',
          'key': 'question_count'
        }
      ],
      // Описание полей таблицы
      fieldsArray: [
        {
          ui: 'input',
          type: 'text',
          key: 'creator_fio',
          addRequired: false,
          readOnly: true
        },
        {
          ui: 'input',
          type: 'text',
          key: 'description',
          addRequired: true,
        },
        {
          ui: 'input',
          type: 'number',
          key: 'question_count',
          addRequired: false,
          readOnly: true
        }
      ],
      // Выбранный опрос
      selectedSurvey: null
    }
  },
  methods: {
    // Выбор опроса из пагинационной таблицы
    selectSurvey(survey) {
      this.$refs.surveyDetail.surveyDescription = survey.description
      this.$refs.surveyDetail.surveyObjectID = survey.object_id
      this.$refs.surveyDetail.dialog = true
    },
    // Функция обновления записей в пагинационной таблице
    updateRecs() {
      this.$refs['surveyTable'].getRecs()
    }
  }
}

</script>

<style scoped>

</style>
