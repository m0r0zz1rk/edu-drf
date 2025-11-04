<template>

  <PaginationTable
    v-if="fieldsArray !== null && urlGet !== ''"
    ref="studentGroupPaginationTable"
    tableTitle="Учебные группы"
    tableWidth="98"
    :noTab="false"
    :addButton="true"
    :addSpecialFunction="openCreateDialog"
    :xlsxButton="true"
    :getRecsURL="urlGet"
    editRecURL="/backend/api/v1/edu/student_group/update/"
    :tableHeaders="tableHeaders"
    :fieldsArray="fieldsArray"
    :itemSelectEvent="groupSelect"
  />

  <StudentGroupCreateDialog
    ref="groupCreateDialog"
    :getRecsFunction="getRecsTable"
    :userRole="userRole"
    :userDep="userDep"
  />

</template>

<script>
import PaginationTable from "@/components/tables/pagination_table/PaginationTable.vue";
import StudentGroupCreateDialog from "@/components/dialogs/edu/student_group/StudentGroupCreateDialog.vue";
import studentGroupStatuses from "@/commons/consts/edu/studentGroupStatuses";
import {getCookie} from "@/commons/cookie";

// Компонент для просмотра списка учебных групп
export default {
  name: "EduStudentGroup",
  components: {StudentGroupCreateDialog, PaginationTable},
  props: {
    // Роль пользователя (centre или dep)
    userRole: String
  },
  data() {
    return {
      // Подразделение работника
      userDep: this.userRole === 'dep' ? getCookie('cokoDep') : 'centre',
      statuses: [],
      tableHeaders: [
        {'title': 'Шифр', 'key': 'code'},
        {'title': 'Статус', 'key': 'status'},
        {'title': 'Наименование услуги', 'key': 'service_name'},
        {'title': 'Начало обучения', 'key': 'date_start'},
        {'title': 'Окончание обучения', 'key': 'date_end'},
        {'title': 'Куратор', 'key': 'curator'},
        {'title': 'Количество заявок', 'key': 'apps_count'}
      ], // Заголовки таблицы
      fieldsArray: null, // Описание заголовков
      // URL эндпоинта на получение данных
      urlGet: '',
    }
  },
  methods: {
    // Получить URL эндпоинта в зависимости от роли
    getURL() {
      let urlGet = "/backend/api/v1/edu/student_group/"
      if (this.userRole === 'dep') {
        urlGet += `?dep=${this.userDep}`
      }
      this.urlGet = urlGet
    },
    // Открыть диалоговое окно для создания учебной группы
    openCreateDialog() {
      this.$refs.groupCreateDialog.dialog = true
    },
    // Получение списка учебных групп
    getRecsTable() {
      this.$refs.studentGroupPaginationTable.getRecs()
    },
    // Открыть страницу управления учебной группой
    groupSelect(group) {
      this.$router.push({
        path: '/centre/edu/student-group/'+group.object_id
      })
    },
    // Получение списка возможных статусов учебных групп
    getStatuses() {
      studentGroupStatuses.map((status) => {
        this.statuses.push(status.title)
      })
      this.fieldsArray = [
        {
          ui: 'input',
          type: 'text',
          key: 'code',
          addRequired: true,
        },
        {
          ui: 'studentGroupStatus',
          items: this.statuses,
          key: 'status',
          addRequired: false
        },
        {
          ui: 'input',
          type: 'text',
          key: 'service_name',
          addRequired: true,
        },
        {
          ui: 'date',
          key: 'date_start',
          addRequired: true,
        },
        {
          ui: 'date',
          key: 'date_end',
          addRequired: true,
        },
        {
          ui: 'input',
          type: 'text',
          key: 'curator',
          addRequired: true,
        },
        {
          ui: 'input',
          type: 'number',
          key: 'apps_count',
          addRequired: true,
        }
      ]
    }
  },
  mounted() {
    this.getURL()
    this.getStatuses()
  }
}
</script>

<style scoped>

</style>
