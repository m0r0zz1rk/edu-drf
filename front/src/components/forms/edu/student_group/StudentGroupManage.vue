<template>

  <v-expansion-panels
    style="padding-top: 10px"
    variant="accordion"
    color="coko-blue"
  >

    <v-expansion-panel
      color="coko-blue"
      title="Изменение шифра"
    >
      <v-expansion-panel-text>
        <v-text-field
          bg-color="white"
          variant="solo"
          v-model="studentGroup.code"
          label="Шифр группы"
          :loading="loading"
        />
      </v-expansion-panel-text>
    </v-expansion-panel>

    <v-expansion-panel
      title="Изменение куратора"
    >
      <v-expansion-panel-text>
        <b>{{curator}}</b><br/>
        <v-btn
          color="coko-blue"
          @click="$refs.curatorSelectDialog.dialog = true"
        >
          Изменить
        </v-btn>
      </v-expansion-panel-text>
    </v-expansion-panel>

    <v-expansion-panel
      title="Изменение статуса"
    >
      <v-expansion-panel-text>
        <v-select
          bg-color="white"
          variant="solo"
          :items="statuses"
          v-model="studentGroup.status"
          item-title="title"
          item-value="key"
          label="Статус"
          :loading="loading"
        />
      </v-expansion-panel-text>
    </v-expansion-panel>

    <v-expansion-panel
      v-if="!([undefined, null, 0].includes(studentGroup.plan_seats_number))"
      title="Изменение планового количества мест"
    >
      <v-expansion-panel-text>
        <v-number-input
          bg-color="white"
          variant="solo"
          controlVariant="split"
          label="Плановое количество мест"
          :min="1"
          v-model="studentGroup.plan_seats_number"
          :loading="loading"
        />
      </v-expansion-panel-text>
    </v-expansion-panel>

    <v-expansion-panel
      title="Изменение ссылки на мероприятие"
    >
      <v-expansion-panel-text>
        <v-textarea
          bg-color="white"
          variant="solo"
          controlVariant="split"
          label="Ссылка на мероприятие"
          :min="1"
          v-model="studentGroup.event_url"
          :loading="loading"
        />
      </v-expansion-panel-text>
    </v-expansion-panel>

    <v-expansion-panel
      title="Изменение формы обучения"
    >
      <v-expansion-panel-text>
        <v-select
          bg-color="white"
          variant="solo"
          :items="studyForms"
          v-model="studentGroup.form"
          item-title="title"
          item-value="key"
          label="Форма обучения"
          :loading="loading"
        />
      </v-expansion-panel-text>
    </v-expansion-panel>

    <v-expansion-panel
      title="Удаление учебной группы"
    >
      <v-expansion-panel-text>
        <v-btn
          color="coko-blue"
          :loading="loading"
          @click="groupDelete()"
        >
          Удалить
        </v-btn>

      </v-expansion-panel-text>
    </v-expansion-panel>

  </v-expansion-panels>

  <CokoDialog
    ref="curatorSelectDialog"
  >

    <template v-slot:title>
      Выбор куратора
    </template>

    <template v-slot:text>
      <PaginationTable
          tableTitle="Сотрудник ЦОКО"
          tableWidth="80"
          :noTab="false"
          :addButton="false"
          :xlsxButton="false"
          getRecsURL="/backend/api/v1/guides/cokos/"
          :tableHeaders="curatorTableHeaders"
          :fieldsArray="curatorFieldsArray"
          :itemSelectEvent="curatorSelect"
      />
    </template>

  </CokoDialog>

</template>

<script>
// Компонент для управления учебной группой
import {apiRequest} from "@/commons/api_request";
import {showAlert} from "@/commons/alerts";
import studentGroupStatuses from "@/commons/consts/edu/studentGroupStatuses";
import PaginationTable from "@/components/tables/pagination_table/PaginationTable.vue";
import studyForms from "@/commons/consts/edu/studyForms";
import CokoDialog from "@/components/dialogs/CokoDialog.vue";

export default {
  name: "StudentGroupManage",
  components: {CokoDialog, PaginationTable},
  props: {
    groupId: String, // object_id учебной группы
  },
  data() {
    return {
      studentGroup: {
        code: null,
        curator_id: null,
        status: null,
        event_url: null,
        form: null,
        plan_seats_number: 0
      }, // Объект с редактируемыми параметрами учебной группы
      curator: '-', // ФИО куратора
      loading: true, // Параметр отображения загрузки на элеметнах формы
      statuses: studentGroupStatuses, // Список статусов учебных групп
      curatorTableHeaders: [
        {
          'title': 'Фамилия',
          'key': 'surname'
        },
        {
          'title': 'Имя',
          'key': 'name'
        },
        {
          'title': 'Отчество',
          'key': 'patronymic'
        },
        {
          'title': 'Подразделение',
          'key': 'department'
        }
      ], // Список заголовков таблицы для выбора куратора учебной группы
      curatorFieldsArray: [
        {
          ui: 'input',
          type: 'text',
          key: 'surname',
          addRequired: false,
        },
        {
          ui: 'input',
          type: 'text',
          key: 'name',
          addRequired: false,
        },
        {
          ui: 'input',
          type: 'text',
          key: 'patronymic',
          addRequired: false,
        },
        {
          ui: 'input',
          type: 'text',
          key: 'department',
          addRequired: false,
        }
      ], // Список описаний заголовков таблицы для выбора куратора учебной группы,
      studyForms: studyForms // Возможные формы обучения в группе
    }
  },
  methods: {
    async getInfo() {
      let infoRequest = await apiRequest(
        '/backend/api/v1/edu/student_group/'+this.groupId+'/',
        'GET',
        true,
        null
      )
      if (infoRequest.error) {
        showAlert('error', 'Информация по учебной группе', infoRequest.error)
        return false
      } else {
        Object.keys(this.studentGroup).map((key) => {
          this.studentGroup[key] = infoRequest[key]
        })
        if (infoRequest['curator_id'] !== null) {
          this.curator = infoRequest['curator']
        }
      }
      this.loading = false
    },
    // Выбор куратора учебной группы
    curatorSelect(curator) {
      this.curator = curator.surname+' '+curator.name
      if (curator.patronymic.length > 0) {
        this.curator += ' '+curator.patronymic
      }
      this.studentGroup.curator_id = curator.object_id
      this.$refs.curatorSelectDialog.dialog = false
    },
    // Удаление учебной группы
    async groupDelete() {
      if (confirm('Вы уверены, что хотите удалить учебную группу?')) {
        this.loading = true
        let deleteRequest = await apiRequest(
          '/backend/api/v1/edu/student_group/'+this.groupId+'/',
          'delete',
          true,
          null
        )
        if (deleteRequest.error) {
          showAlert('error', 'Удаление группы', deleteRequest.error)
          this.loading = false
          return false
        } else {
          showAlert('success', 'Удаление группы', deleteRequest.success)
          this.$router.push({
            path: '/centre/edu/'
          })
        }
      }
    }
  },
  mounted() {
    this.getInfo()
  }
}
</script>

<style scoped>

</style>
