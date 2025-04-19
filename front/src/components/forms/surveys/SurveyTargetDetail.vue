<template>

  <v-dialog
      persistent
      v-model="dialog"
  >

    <v-card class="lk-full-page-card">
      <v-card-title class="d-flex justify-space-between align-center">
        <template
          v-if="newTarget"
        >
          Добавление таргетирования
        </template>

        <template
          v-if="!(newTarget)"
        >
          Изменение таргетирования
        </template>

        <v-btn
            icon="mdi-close"
            color="coko-blue"
            @click="dialog = !(dialog)"
        />
      </v-card-title>

      <v-card-text>

        <DialogContentWithError
            ref="surveyTargetContentError"
        >

          <slot>

              <v-row
                  dense
              >

                <v-col
                    cols="12"
                    md="12"
                    sm="12"
                >

                  <v-text-field
                      label="Опрос"
                      :loading="loading"
                      v-model="surveyTarget.survey_description"
                      @click="dialogSelectSurvey = true"
                      readonly
                  />

                </v-col>

                <v-col
                    cols="12"
                    md="12"
                    sm="12"
                >

                  <v-select
                      bg-color="white"
                      variant="solo"
                      v-model="surveyTarget.type"
                      :items="targetTypes"
                      item-title="title"
                      item-value="key"
                      label="Тип таргетирования"
                      :loading="loading"
                  />

                </v-col>

                <v-col
                    v-if="['group', 'На определенные группы'].includes(surveyTarget.type)"
                    cols="12"
                    md="12"
                    sm="12"
                >

                  <v-text-field
                      label="Учебная группа"
                      :loading="loading"
                      v-model="surveyTarget.group_code"
                      @click="dialogSelectGroup = true"
                      readonly
                  />

                </v-col>

              </v-row>

          </slot>

        </DialogContentWithError>

      </v-card-text>

      <v-card-actions
          style="background-color: white"
      >

        <v-spacer></v-spacer>

        <v-btn
            v-if="!(newTarget)"
            color="coko-blue"
            text='Удалить'
            :loading="loading"
            @click="deleteTarget()"
        ></v-btn>

        <v-btn
            color="coko-blue"
            text='Сохранить'
            :loading="loading"
            @click="saveTarget()"
        ></v-btn>
      </v-card-actions>

    </v-card>

  </v-dialog>

  <v-dialog
      persistent
      v-model="dialogSelectSurvey"
  >

    <v-card class="lk-full-page-card">
      <v-card-title class="d-flex justify-space-between align-center">
        Выбор опроса

        <v-btn
            icon="mdi-close"
            color="coko-blue"
            @click="dialogSelectSurvey = !(dialogSelectSurvey)"
        />
      </v-card-title>

      <v-card-text>

        <PaginationTable
            tableTitle="Опросы"
            tableWidth="98"
            :noTab="false"
            :addButton="false"
            :xlsxButton="false"
            getRecsURL="/backend/api/v1/surveys/surveys/"
            addRecURL="/backend/api/v1/surveys/surveys/"
            :tableHeaders="surveyTableHeaders"
            :fieldsArray="surveyFieldsArray"
            :itemSelectEvent="selectSurvey"
        />

      </v-card-text>

    </v-card>

  </v-dialog>

  <v-dialog
      persistent
      v-model="dialogSelectGroup"
  >

    <v-card class="lk-full-page-card">
      <v-card-title class="d-flex justify-space-between align-center">
        Выбор учебной группы

        <v-btn
            icon="mdi-close"
            color="coko-blue"
            @click="dialogSelectGroup = !(dialogSelectGroup)"
        />
      </v-card-title>

      <v-card-text>

        <PaginationTable
            tableTitle="Учебные группы"
            tableWidth="98"
            :noTab="false"
            :addButton="false"
            :xlsxButton="false"
            getRecsURL="/backend/api/v1/edu/student_group/"
            :tableHeaders="groupTableHeaders"
            :fieldsArray="groupFieldsArray"
            :itemSelectEvent="selectGroup"
        />

      </v-card-text>

    </v-card>

  </v-dialog>

</template>

<script>

// Диалоговое окно для добавление/редактирования назначения опроса
import DialogContentWithError from "@/components/dialogs/DialogContentWithError.vue";
import surveyTargetTypes from "@/commons/consts/survey/surveyTargetTypes";
import PaginationTable from "@/components/tables/pagination_table/PaginationTable.vue";
import {apiRequest} from "@/commons/apiRequest";
import {showAlert} from "@/commons/alerts";
import studentGroupStatuses from "@/commons/consts/edu/studentGroupStatuses";

export default {
  name: 'SurveyTargetDetail',
  props: {
    // Функция получения списка записей назначений в родительском компоненте
    getTargets: Function
  },
  components: {PaginationTable, DialogContentWithError},
  data() {
    return {
      // Параметр отображения диалогового окна
      dialog: false,
      // Параметр добавления нового объекта
      newTarget: true,
      // Параметр отображения анимации загрузки на элементах формы
      loading: false,
      // объект назначения (если null - новый объект)
      surveyTarget: {
        'survey_id': null,
        'survey_description': '(Не выбран)',
        'type': '',
        'group_id': null,
        'group_code': '(Не выбрана)'
      },
      // Список типов назначений
      targetTypes: surveyTargetTypes,
      // Параметр отображения диалогового окна для выбора опроса
      dialogSelectSurvey: false,
      // Заголовки таблицы для выбора опроса
      surveyTableHeaders: [
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
      // Описание полей таблицы для выбора опроса
      surveyFieldsArray: [
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
      // Параметр отображения диалогового окна для выбора учебной группы
      dialogSelectGroup: false,
      // Заголовки таблицы для выбора учебной группы
      groupTableHeaders: [
        {
          'title': 'Шифр',
          'key': 'code'
        },
        {
          'title': 'Статус',
          'key': 'status'
        },
        {
          'title': 'Наименование услуги',
          'key': 'service_name'
        },
        {
          'title': 'Начало обучения',
          'key': 'date_start'
        },
        {
          'title': 'Окончание обучения',
          'key': 'date_end'
        },
        {
          'title': 'Куратор',
          'key': 'curator'
        }
      ],
      // Описание полей таблицы для выбора учебной группы
      groupFieldsArray: [],
    }
  },
  methods: {
    // Установка выбранного в таблице опроса
    selectSurvey(survey) {
      this.surveyTarget.survey_id = survey.object_id
      this.surveyTarget.survey_description = survey.description
      this.dialogSelectSurvey = false
    },
    // Сохранение информации по назначению
    async saveTarget() {
      if ([undefined, null, ''].includes(this.surveyTarget.survey_id)) {
        alert('Выберите опрос')
        return false
      }
      if (this.surveyTarget.type.length === 0) {
        alert('Выберите тип таргетирования')
        return false
      }
      if ((this.surveyTarget.type === 'group') &&
          (this.surveyTarget.group_id === null)) {
        alert('Выберите учебную группу')
        return false
      }
      this.loading = true
      let url = '/backend/api/v1/surveys/survey_target/'
      let method = 'POST'
      if (!(this.newTarget)) {
        url += this.surveyTarget.object_id+'/'
        method = 'PATCH'
      }
      let body = this.surveyTarget
      delete body['group_code']
      if (!(this.newTarget)) {
        delete body['object_id']
      }
      let saveTargetResponse = await apiRequest(
          url,
          method,
          true,
          this.surveyTarget
      )
      if (saveTargetResponse.error) {
        alert('Произошла ошибка: ' + saveTargetResponse.error)
      } else {
        showAlert(
            'success',
            'Таргетирование опроса',
            saveTargetResponse.success
        )
        this.getTargets()
        this.dialog = false
      }
      this.loading = false
    },
    // Получение статусов учебных групп и формирование списка описания полей таблицы выбора группы
    getStatuses() {
      let statuses = []
      studentGroupStatuses.map((status) => {
        statuses.push(status.title)
      })
      this.groupFieldsArray = [
        {
          ui: 'input',
          type: 'text',
          key: 'code',
          addRequired: true,
        },
        {
          ui: 'studentGroupStatus',
          items: statuses,
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
        }
      ]
    },
    // Выбор учебной группы
    selectGroup(group) {
      this.surveyTarget.group_id = group.object_id
      this.surveyTarget.group_code = group.code
      this.dialogSelectGroup = false
    },
    // Удалить назначение
    async deleteTarget() {
      if (confirm('Вы уверены, что хотите удалить таргетирование?')) {
        this.loading = true
        let deleteTargetResponse = await apiRequest(
            '/backend/api/v1/surveys/survey_target/'+this.surveyTarget.object_id+'/',
            'DELETE',
            true,
            null
        )
        if (deleteTargetResponse.error) {
          alert(deleteTargetResponse.error)
        } else {
          showAlert(
              'success',
              'Таргетирование опроса',
              deleteTargetResponse.success
          )
          this.getTargets()
          this.dialog = false
        }
        this.loading = false
      }
    }
  },
  mounted() {
    this.getStatuses()
  }
}

</script>

<style scoped>

</style>
