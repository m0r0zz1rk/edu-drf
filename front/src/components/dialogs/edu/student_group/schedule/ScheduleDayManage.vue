<template>

  <v-btn
      prepend-icon="mdi-pencil"
      :loading="loading"
      color="coko-red"
      @click.native.stop="openChangeDialog"
      :text="!(mobileDisplay) && 'Изменить'"
  />

  <v-dialog
      persistent
      v-model="dialog"
  >

    <v-card class="lk-full-page-card">
      <v-card-title class="d-flex justify-space-between align-center">

        Управление расписанием {{dayInfo.day}}

        <v-btn
            icon="mdi-close"
            color="coko-blue"
            @click="dialog = !(dialog)"
        />
      </v-card-title>

      <v-card-text>

        <template v-if="kugRemainHours === null || lessonsDialogs === null">

          <b>Подождите, получаем информацию по остаточным часам...</b>

        </template>

        <template v-if="kugRemainHours !== null && lessonsDialogs !== null">

          <DialogContentWithError ref="content-error">

            <v-btn
                prepend-icon="mdi-plus"
                :loading="loading"
                style="margin-bottom: 5px"
                color="coko-blue"
                @click="addLesson()"
                :text="!(mobileDisplay) && 'Добавить'"
            />

            <v-data-table
                sticky
                class="adaptive-schedule-manage-table"
                style="overflow: auto; width: 100%;"
                :headers="headers"
                :mobile-breakpoint="960"
                :items="dayInfo.lessons"
                :loading="loading"
                loading-text="Подождите, идет загрузка данных..."
                hide-default-footer
                :disable-pagination="true"
            >

              <template v-slot:headers="{ columns, isSorted, getSortIcon, toggleSort }">
                <tr v-if="!(mobileDisplay)" style="position: sticky; top: 0; z-index: 5">
                  <template v-for="column in columns">
                    <td
                        style="
                          text-align: center;
                          background-color: #373c59;
                          color: white;
                        "
                    >
                      <b>
                        {{column.title}}
                      </b>

                    </td>

                  </template>

                </tr>

                <tr v-if="mobileDisplay" style="position: sticky; top: 0; z-index: 5">

                </tr>

              </template>

              <template v-slot:item="{ item, index }">

                <tr
                    v-bind:class="{'v-data-table__tr v-data-table__tr--mobile': mobileDisplay}"
                >

                  <template v-for="header in headers">

                    <td
                        style="text-align: center;"
                    >

                      <div v-if="mobileDisplay" class="v-data-table__td-title">

                        {{header.title}}

                      </div>

                      <template v-if="['time_start_str', 'time_end_str'].includes(header.key)">

                        <v-text-field
                            v-model="item[header.key]"
                            :active="lessonsDialogs.filter((rec) => rec.lessonId === index)[0][header.key]"
                            :focused="lessonsDialogs.filter((rec) => rec.lessonId === index)[0][header.key]"
                            append-inner-icon="mdi-clock-time-four-outline"
                            readonly
                        >

                          <v-dialog
                              v-model="lessonsDialogs.filter((rec) => rec.lessonId === index)[0][header.key]"
                              activator="parent"
                              width="auto"
                          >

                            <v-time-picker
                                v-if="lessonsDialogs.filter((rec) => rec.lessonId === index)[0][header.key]"
                                format="24hr"
                                :title="header.key === 'time_start_str' ?
                                  'Выберите время начала занятия'
                                  :
                                  'Выберите время окончания занятия'
                                "
                                v-model="item[header.key]"
                                @update:modelValue="e => {
                                    item['time_end_str'] = convertSecondsToTimeStr(
                                        convertTimeStrToSeconds(item['time_start_str'])+2700
                                    )
                                    if (item['teacher'] !== null) {
                                      checkTeacherBusy(
                                          item['teacher'],
                                          item['time_start_str'],
                                          index
                                      )
                                    }
                                }"
                            ></v-time-picker>


                          </v-dialog>

                        </v-text-field>

                      </template>

                      <template v-if="header.key === 'theme'">

                        <template v-if="serviceType === 'ou'">
                          <div :title="item[header.key]">
                            <v-text-field
                                v-model="item[header.key]"
                                :active="lessonsDialogs.filter((rec) => rec.lessonId === index)[0]['theme']"
                                :focused="lessonsDialogs.filter((rec) => rec.lessonId === index)[0]['theme']"
                                readonly
                            >

                              <v-dialog
                                  v-model="lessonsDialogs.filter((rec) => rec.lessonId === index)[0]['theme']"
                                  activator="parent"
                                  width="auto"
                              >

                                <v-card
                                    class="lk-full-page-card"
                                >

                                  <v-card-title class="d-flex justify-space-between align-center">
                                    Оставшиеся часы КУГ
                                  </v-card-title>

                                  <v-card-text>
                                    <v-expansion-panels>

                                      <v-expansion-panel
                                          color="coko-blue"
                                          v-for="chapter in kugRemainHours"
                                          :title="chapter.chapter"
                                          readonly
                                      >

                                        <v-data-table
                                            sticky
                                            style="overflow: auto; width: 100%;"
                                            :headers="remainHoursHeaders"
                                            :mobile-breakpoint="960"
                                            :items="chapter.themes"
                                            :loading="loading"
                                            loading-text="Подождите, идет загрузка данных..."
                                            hide-default-footer
                                            :disable-pagination="true"
                                        >

                                          <template v-slot:headers="{ columns, isSorted, getSortIcon, toggleSort }">
                                            <tr v-if="!(mobileDisplay)" style="position: sticky; top: 0; z-index: 5">
                                              <td
                                                  style="
                                                  text-align: center;
                                                  background-color: #373c59;
                                                  color: white;
                                                  width: 60%
                                                "
                                              >
                                                <b>Тема</b>
                                              </td>
                                              <template v-for="column in columns">
                                                <td
                                                    v-if="column.key !== 'theme'"
                                                    style="
                          text-align: center;
                          background-color: #373c59;
                          color: white;
                        "
                                                >
                                                  <b>
                                                    {{column.title}}
                                                  </b>
                                                </td>
                                              </template>
                                            </tr>
                                            <tr v-if="mobileDisplay" style="position: sticky; top: 0; z-index: 5">
                                            </tr>
                                          </template>

                                          <template v-slot:item="{ index: kugIndex, item: kugItem }">
                                            <tr
                                                v-bind:class="{'v-data-table__tr v-data-table__tr--mobile': mobileDisplay}"
                                            >
                                              <td
                                                  style="text-align: center; width: 60%"
                                              >
                                                <div v-if="mobileDisplay" class="v-data-table__td-title">
                                                  Тема
                                                </div>
                                                {{ kugItem['theme'] }}
                                              </td>

                                              <template v-for="header in remainHoursHeaders">
                                                <td
                                                    v-if="header.key !== 'theme'"
                                                    style="text-align: center"
                                                >
                                                  <div
                                                      v-if="mobileDisplay"
                                                      class="v-data-table__td-title"
                                                  >
                                                    {{lTypes.filter((type) => type.key === header.key)[0].name}}
                                                  </div>
                                                  <template v-if="header.key !== 'theme'">
                                                    <v-btn
                                                        color="coko-blue"
                                                        :disabled="kugItem[header.key] === 0"
                                                        @click="pickKUGHour(
                                                          index,
                                                          chapter.chapter,
                                                          kugItem,
                                                          header.key
                                                      )"
                                                        :text="kugItem[header.key]"
                                                    />
                                                  </template>
                                                </td>
                                              </template>
                                            </tr>
                                          </template>

                                          <template v-slot:loading>
                                            <v-skeleton-loader :type="'table-row@10'"></v-skeleton-loader>
                                          </template>

                                          <template v-slot:bottom></template>


                                        </v-data-table>


                                      </v-expansion-panel>

                                    </v-expansion-panels>
                                  </v-card-text>
                                </v-card>


                              </v-dialog>

                            </v-text-field>
                          </div>
                        </template>

                        <template v-if="serviceType !== 'ou'">
                          <div :title="item[header.key]">
                            <v-text-field
                              v-model="item[header.key]"
                            />
                          </div>
                        </template>

                      </template>

                      <template v-if="header.key === 'type'">
                        <div :title="lTypes.filter((type) => type.key === item[header.key])[0].name">
                          <template v-if="serviceType === 'ou'">
                            <v-text-field
                                v-model="lTypes.filter((type) => type.key === item[header.key])[0].name"
                                readonly
                            />
                          </template>

                          <template v-if="serviceType !== 'ou'">
                            <v-select
                                v-model="item[header.key]"
                                :items="lTypes"
                                item-value="key"
                                item-title="name"
                            />
                          </template>
                        </div>
                      </template>

                      <template v-if="header.key === 'teacher'">
                        <div
                            :title="lessonsDialogs[index].teacher_busy ? 'Преподаватель занят' : item['teacher_fio']"
                        >
                          <v-text-field
                              :class="lessonsDialogs[index].teacher_busy && 'text-red'"
                              v-model="item['teacher_fio']"
                              :active="teacherDialog"
                              :focused="teacherDialog"
                              @update:focused="selectedLessonID = index"
                              readonly
                          >
                            <v-dialog
                                persistent
                                activator="parent"
                                v-model="teacherDialog"
                            >

                              <v-card class="lk-full-page-card">
                                <v-card-title class="d-flex justify-space-between align-center">

                                  Выбор преподавателя

                                  <v-btn
                                      icon="mdi-close"
                                      color="coko-blue"
                                      @click="teacherDialog = !(teacherDialog)"
                                  />
                                </v-card-title>

                                <v-tabs
                                    style="width: 100%; top: 0; z-index: 10; position: sticky"
                                    v-model="teacherTypeTab"
                                    bg-color="coko-blue"
                                    show-arrows
                                >

                                  <v-tab
                                      class="coko-tab"
                                      value="coko"
                                  >
                                    Сотрудник ЦОКО
                                  </v-tab>

                                  <v-tab
                                      class="coko-tab"
                                      value="user"
                                  >
                                    Внешний пользователь
                                  </v-tab>
                                </v-tabs>

                                <PaginationTable
                                    tableTitle="Сотрудник ЦОКО"
                                    v-if="teacherTypeTab === 'coko'"
                                    tableWidth="80"
                                    :noTab="false"
                                    :addButton="false"
                                    :xlsxButton="false"
                                    getRecsURL="/backend/api/v1/guides/coko/"
                                    :tableHeaders="[
                                      ...teacherTableHeaders,
                                      {
                                        'title': 'Подразделение',
                                        'key': 'department'
                                      }
                                  ]"
                                    :fieldsArray="[
                                      ...teacherFieldsArray,
                                      {
                                        ui: 'input',
                                        type: 'text',
                                        key: 'department',
                                        addRequired: false,
                                      }
                                  ]"
                                    :itemSelectEvent="chooseTeacher"
                                />

                                <PaginationTable
                                    tableTitle="Пользователи"
                                    v-if="teacherTypeTab === 'user'"
                                    tableWidth="80"
                                    :noTab="false"
                                    :addButton="false"
                                    :xlsxButton="false"
                                    getRecsURL="/backend/api/v1/edu/teachers/"
                                    :tableHeaders="[
                                      ...teacherTableHeaders,
                                       {
                                          'title': 'Телефон',
                                          'key': 'phone'
                                       }
                                  ]"
                                    :fieldsArray="[
                                      ...teacherFieldsArray,
                                      {
                                        ui: 'phone',
                                        key: 'phone',
                                        addRequired: false,
                                      }
                                  ]"
                                    :itemSelectEvent="chooseTeacher"
                                />
                              </v-card>
                            </v-dialog>

                          </v-text-field>
                        </div>
                      </template>

                      <template v-if="header.key === 'distance'">
                        <v-switch
                            color="coko-blue"
                          v-model="item[header.key]"
                        />
                      </template>

                      <template v-if="header.key === 'control'">
                        <v-text-field
                          v-model="item[header.key]"
                          @change="e => item[header.key] = e.target.value"
                        />
                      </template>

                      <template v-if="header.key === 'actions'">
                        <div style="display: inline-block">
                          <v-icon
                              icon="mdi-delete"
                              color="coko-blue"
                              @click="deleteLesson(index)"
                          />
                        </div>
                      </template>

                    </td>

                  </template>

                </tr>

              </template>

              <template v-slot:loading>
                <v-skeleton-loader :type="'table-row@10'"></v-skeleton-loader>
              </template>

              <template v-slot:bottom></template>

            </v-data-table>

          </DialogContentWithError>

        </template>

      </v-card-text>

      <v-card-actions
          style="background-color: white"
      >

        <v-spacer></v-spacer>

        <v-btn
            color="coko-blue"
            text="Сохранить"
            :loading="loading"
            @click="saveDayInfo()"
        ></v-btn>
      </v-card-actions>

    </v-card>

  </v-dialog>

</template>

<script>

// Компонент для управления учебным днем в расписании
import DialogContentWithError from "@/components/dialogs/DialogContentWithError.vue";
import {useDisplay} from "vuetify";
import BooleanBadge from "@/components/badges/BooleanBadge.vue";
import lessonTypes from "@/commons/consts/edu/lessonTypes";
import {convertSecondsToTimeStr, convertTimeStrToSeconds} from "@/commons/time";
import {apiRequest} from "@/commons/api_request";
import PaginationTable from "@/components/tables/pagination_table/PaginationTable.vue";
import {convertBackendDate} from "@/commons/date";
import {showAlert} from "@/commons/alerts";

export default {
  name: 'ScheduleDayManage',
  components: {PaginationTable, BooleanBadge, DialogContentWithError},
  props: {
    groupId: String, // object_id учебной группы
    serviceType: String, // Тип услуги учебной группы (ou или iku)
    dayInfo: Object, // Объект, содержащий учебный день и список занятий
    getSchedule: Function // Функция для получения расписания занятий учебной группы
  },
  data() {
    return {
      loading: false, // Параметр отображения анимации загрузки на элементах формы
      dialog: false, // Параметр отображения диалогового окна
      editDialog: false, // Параметр отображения диалогового окна для изменения учебного занятия
      mobileDisplay: useDisplay().smAndDown, // Проверка на дисплей мобильного устройства
      headers: [
        {
          'title': 'Начало',
          'key': 'time_start_str'
        },
        {
          'title': 'Окончание',
          'key': 'time_end_str'
        },
        {
          'title': 'Тема',
          'key': 'theme'
        },
        {
          'title': 'Тип занятия',
          'key': 'type'
        },
        {
          'title': 'Преподаватель',
          'key': 'teacher'
        },
        {
          'title': 'Дистант',
          'key': 'distance'
        },
        {
          'title': 'Форма контроля',
          'key': 'control'
        },
        {
          'title': 'Действия',
          'key': 'actions'
        },
      ], // Список заголовков таблицы
      lTypes: lessonTypes, // Типы учебных занятий
      editLesson: null, // Изменяемое учебное занятие
      editLessonTimeStart: false, // Параметр отображения окна для выбора времени старта редактируемого занятия
      editLessonTimeEnd: false, // Параметр отображения окна для выбора времени окончания редактируемого занятия
      kugRemainHours: null, // Объект, содержащий остаточные часы по КУГ (для группы ОУ)
      lessonsDialogs: null, // Список параметров отображение компонентов диалоговых окон для уроков
      remainHoursHeaders: [
        {
          'title': 'Тема',
          'key': 'theme'
        },
        {
          'title': 'Лекция',
          'key': 'lecture'
        },
        {
          'title': 'Практика',
          'key': 'practice'
        },
        {
          'title': 'Стажировка',
          'key': 'trainee'
        },
        {
          'title': 'Самостоятельная работа',
          'key': 'individual'
        },
      ], // Список заголовков таблицы для выбора занятия из оставшихся часов КУГ
      teacherDialog: false, // Параметр отображения диалогового окна для выбора преподавателя
      selectedLessonID: 0, // Номер выбранного для редактирования занятия
      teacherTableHeaders: [
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
        }
      ], // Список заголовков таблицы для выбора преподавателя занятия
      teacherFieldsArray: [
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
        }
      ], // Список описаний заголовков таблицы для выбора преподавателя занятия
      teacherTypeTab: 'coko', //Значение вкладки при выбор преподавателя на занятие
    }
  },
  methods: {
    convertTimeStrToSeconds,
    convertSecondsToTimeStr,
    // Создание объекта для управления отображением окон для выбора времени начала и окончания занятия
    createTimePickerDialogs() {
      let tsd = []
      this.dayInfo.lessons.map((lesson, lessonId) => {
        tsd.push({
          'lessonId': lessonId,
          'time_start_str': false,
          'time_end_str': false,
          'theme': false,
          'teacher_busy': false
        })
      })
      this.lessonsDialogs = tsd
    },
    // Получить остаточные часы при открытии формы для изменения расписания дня (только для групп по ОУ)
    openChangeDialog() {
      this.dialog = !(this.dialog)
      this.getRemainHours()
    },
    // Получение остаточных часов по КУГ (для групп по образовательным услугам (ou))
    async getRemainHours() {
      if (this.serviceType === 'ou') {
        let remainHoursRequest = await apiRequest(
            '/backend/api/v1/edu/kug/remain_hours/'+this.groupId+'/',
            'GET',
            true,
            null
        )
        if (remainHoursRequest.error) {
          this.$refs["content-error"].showContentError(remainHoursRequest.error)
          return false
        } else {
          console.log(remainHoursRequest)
          this.kugRemainHours = remainHoursRequest['kug_remain']
        }
      } else {
        this.kugRemainHours = 0
      }
    },
    // Добавить занятие
    addLesson() {
      if (confirm('Вы уверены, что хотите добавить еще одно занятие?')) {
        this.lessonsDialogs.push({
          lessonId: this.lessonsDialogs.length,
          'time_start_str': false,
          'time_end_str': false,
          'theme': false,
          'teacher_busy': false
        })
        this.dayInfo.lessons.push({
          "time_start_str": "00:00",
          "time_end_str": "00:45",
          "theme": "Тема",
          "type": "lecture",
          "teacher_fio": "-",
          "distance": false,
          "control": null
        })
      }
    },
    // Удаление занятия
    deleteLesson(index) {
      if (confirm('Вы уверены, что хотите удалить занятие в '+this.dayInfo.lessons[index].time_start_str+'?')) {
        this.dayInfo.lessons.splice(index, 1)
        this.lessonsDialogs.splice(index, 1)
      }
    },
    // Выбрать час занятия из КУГ
    pickKUGHour(lessonId, chapter, theme, type) {
      let lesson = this.dayInfo.lessons[lessonId]
      console.log('lesson: '+JSON.stringify(lesson))
      this.kugRemainHours.map((ch) => {
        ch.themes.map((th) => {
          if (lesson['kug_theme_id'] === th['theme_id']) {
            console.log(th)
            console.log(lesson['type'])
            th[lesson['type']] += 1
          }
          if (th['theme_id'] === theme.theme_id) {
            th[type] -= 1
          }
        })
      })
      lesson['kug_theme_id'] = theme.theme_id
      lesson['theme'] = theme.theme
      lesson['type'] = type
      this.dayInfo.lessons[lessonId] = lesson
      this.lessonsDialogs.filter((rec) => rec.lessonId === lessonId)[0]['theme'] = false
      console.log(this.kugRemainHours)
      console.log(this.dayInfo.lessons)
    },
    // Выбор преподавателя
    chooseTeacher(teacher) {
      this.dayInfo.lessons[this.selectedLessonID].teacher = teacher.object_id
      this.dayInfo.lessons[this.selectedLessonID].teacher_fio = teacher.surname+' '+teacher.name+' '+teacher.patronymic
      this.teacherDialog = false
      console.log(this.dayInfo.lessons)
      this.checkTeacherBusy(
          teacher.object_id,
          this.dayInfo.lessons[this.selectedLessonID].time_start_str,
          this.selectedLessonID
      )
    },
    // Проверка занятости преподавателя
    async checkTeacherBusy(teacherId, timeStartStr, lessonId) {
      if (!([undefined, null].includes(teacherId))){
        let checkTeacherBusy = await apiRequest(
            '/backend/api/v1/edu/teacher_busy/',
            'POST',
            true,
            {
              'teacher_id': teacherId,
              'group_id': this.groupId,
              'day': this.dayInfo.day,
              'time_start_str': timeStartStr
            },
            true
        )
        if (checkTeacherBusy.status === 423) {
          this.lessonsDialogs[lessonId].teacher_busy = true
        } else if (checkTeacherBusy.status === 200) {
          this.lessonsDialogs[lessonId].teacher_busy = false
        } else {
          let data = await checkTeacherBusy.json()
          this.$refs["content-error"].showContentError(data.error)
        }
      }
    },
    // Сохранение изменений в расписании учебного дня
    async saveDayInfo() {
      this.loading = true
      let requestBody = this.dayInfo
      requestBody['group_id'] = this.groupId
      console.log(requestBody)
      let daySaveRequest = await apiRequest(
          '/backend/api/v1/edu/schedule/save_day/',
          'POST',
          true,
          requestBody
      )
      if (daySaveRequest.error) {
        this.$refs["content-error"].showContentError(daySaveRequest.error)
      } else {
        this.dialog = false
        showAlert('success', 'Сохранение расписания', daySaveRequest.success)
        this.getSchedule()
      }
      this.loading = false
    }
  },
  mounted() {
    this.createTimePickerDialogs()
  }
}

</script>

<style scoped>
.text-red input {
  color: red !important;
}
</style>
