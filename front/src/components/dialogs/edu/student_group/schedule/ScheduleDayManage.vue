<template>

  <v-btn
      prepend-icon="mdi-pencil"
      :loading="loading"
      color="coko-red"
      @click.native.stop="dialog=!dialog"
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
              style="overflow: auto; width: 98%;"
              :headers="headers"
              :mobile-breakpoint="960"
              :items="dayInfo.lessons.sort((a, b) => convertTimeStrToSeconds(a.time_start_str) - convertTimeStrToSeconds(b.time_start_str))"
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

                    <template
                        v-if="['distance', 'type'].includes(header.key)"
                    >

                      <BooleanBadge
                          v-if="header.key === 'distance'"
                          :bool="item[header.key]"
                      />

                      <p
                          v-if="header.key === 'type'"
                      >
                        {{ lTypes.filter((t) => t.key === item[header.key])[0].name }}
                      </p>

                    </template>


                    <div
                        v-if="!(['distance', 'type'].includes(header.key))"
                    >

                      <template v-if="header.key === 'actions'">

                        <div style="display: inline-block">

                          <v-icon
                              icon="mdi-pencil"
                              color="coko-blue"
                              @click="editLesson(item, index)"
                          />

                          &nbsp;&nbsp;&nbsp;

                          <v-icon
                              icon="mdi-delete"
                              color="coko-blue"
                              @click="deleteLesson(index)"
                          />
                        </div>

                      </template>

                      <template v-if="header.key !== 'actions'">

                        {{item[header.key]}}

                      </template>

                    </div>

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

  <v-dialog
      persistent
      v-model="editDialog"
  >

    <v-card class="lk-full-page-card">
      <v-card-title class="d-flex justify-space-between align-center">

        <template v-if="editLesson !== null">

          Редактирование занятия в {{editLesson.time_start_str}}

        </template>


        <v-btn
            icon="mdi-close"
            color="coko-blue"
            @click="dialog = !(dialog)"
        />
      </v-card-title>

      <v-card-text>

        <DialogContentWithError ref="content-error">

          <v-row
              v-if="editLesson !== null"
              dense
          >

            <v-col
                cols="12"
                md="6"
                sm="6"
            >
              <v-text-field
                  v-model="editLesson.time_start_str"
                  :active="editLessonTimeStart"
                  :focused="editLessonTimeStart"
                  prepend-icon="mdi-clock-time-four-outline"
                  readonly
              >

                <v-dialog
                    v-model="editLessonTimeStart"
                    activator="parent"
                    width="auto"
                >

                  <v-time-picker
                      v-if="editLessonTimeStart"
                      format="24hr"
                      title="Выберите время начала занятия"
                      v-model="editLesson.time_start_str"
                  ></v-time-picker>


                </v-dialog>

              </v-text-field>
            </v-col>

            <v-col
                cols="12"
                md="6"
                sm="6"
            >
              <v-text-field
                  v-model="editLesson.time_end_str"
                  :active="editLessonTimeEnd"
                  :focused="editLessonTimeEnd"
                  prepend-icon="mdi-clock-time-four-outline"
                  readonly
              >

                <v-dialog
                    v-model="editLessonTimeEnd"
                    activator="parent"
                    width="auto"
                >

                  <v-time-picker
                      v-if="editLessonTimeEnd"
                      format="24hr"
                      title="Выберите время начала занятия"
                      v-model="editLesson.time_end_str"
                  ></v-time-picker>


                </v-dialog>

              </v-text-field>
            </v-col>

            <v-col
                cols="12"
                md="12"
                sm="12"
            >
              <v-textarea
                  bg-color="white"
                  variant="solo"
                  v-model="editLesson.theme"
                  label="Тема"
                  :loading="loading"
              />
            </v-col>

            <v-col
                cols="12"
                md="6"
                sm="6"
            >
              <v-number-input
                  bg-color="white"
                  variant="solo"
                  controlVariant="split"
                  label="*"
                  :min="0"
                  v-model="programObject.duration"
                  :loading="loading"
              />
            </v-col>

            <v-col
                cols="12"
                md="6"
                sm="6"
            >
              <v-number-input
                  bg-color="white"
                  variant="solo"
                  controlVariant="split"
                  label="Цена (рублей)*"
                  :min="0"
                  :step="500"
                  v-model="programObject.price"
                  :loading="loading"
              />
            </v-col>

            <v-col
                cols="12"
                md="6"
                sm="6"
            >
              <v-textarea
                  bg-color="white"
                  variant="solo"
                  label="Аннотация"
                  v-model="programObject.annotation"
                  clearable
                  :loading="loading"
              />
            </v-col>

            <v-col
                cols="12"
                md="6"
                sm="6"
            >
              <v-select
                  bg-color="white"
                  variant="solo"
                  clearable
                  chips
                  multiple
                  label="Категории слушателей"
                  :items="audienceCategories"
                  v-model="programObject.categories"
                  :loading="loading"
              />
            </v-col>

          </v-row>

        </DialogContentWithError>

      </v-card-text>

    </v-card>

  </v-dialog>

</template>

<script>

// Компонент для управления учебным днем в расписании
import DialogContentWithError from "@/components/dialogs/DialogContentWithError.vue";
import {useDisplay} from "vuetify";
import BooleanBadge from "@/components/badges/BooleanBadge.vue";
import lessonTypes from "@/commons/consts/edu/lessonTypes";
import {convertTimeStrToSeconds} from "@/commons/time";

export default {
  name: 'ScheduleDayManage',
  components: {BooleanBadge, DialogContentWithError},
  props: {
    groupId: String, // object_id учебной группы
    serviceType: String, // Тип услуги учебной группы (ou или iku)
    dayInfo: Object, // Объект, содержащий учебный день и список занятий
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
    }
  },
  methods: {
    convertTimeStrToSeconds,
    // Добавить занятие
    addLesson() {
      this.dayInfo.lessons.push({
        "time_start_str": "00:00",
        "time_end_str": "00:45",
        "theme": "Тема",
        "type": "lecture",
        "teacher_fio": "-",
        "distance": false,
        "control": null
      })
    },
    // Изменение занятия
    editLesson(item, index) {

    },
    // Удаление занятия
    deleteLesson(index) {
      if (confirm('Вы уверены, что хотите удалить занятие в '+this.dayInfo.lessons[index].time_start_str+'?')) {
        this.dayInfo.lessons.splice(index, 1)
      }
    },
    // Сохранение изменений в расписании учебного дня
    async saveDayInfo() {

    }
  }
}

</script>

<style scoped>

</style>