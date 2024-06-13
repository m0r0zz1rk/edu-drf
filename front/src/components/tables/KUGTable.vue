<template>

  <div v-if="kug === null">
      Получение информации о КУГ...
  </div>

  <div v-if="kug !== null">

      <div v-if="kug.on_edit === null">
          <v-btn
            prepend-icon="mdi-pencil"
            :loading="tableLoading"
            style="margin-bottom: 15px;"
            color="coko-blue"
            @click="kugEditRequest()"
            :text="!(mobileDisplay) && 'Редактировать'"
          />
      </div>

      <div v-if="kug.on_edit === 'yourself'" style="display: inline-block">
          <v-btn
            prepend-icon="mdi-check"
            :loading="tableLoading"
            style="margin-bottom: 15px; margin-right: 15px"
            color="coko-blue"
            @click="saveKug()"
            :text="!(mobileDisplay) && 'Сохранить'"
          />

          <v-btn
            prepend-icon="mdi-plus"
            :loading="tableLoading"
            style="margin-bottom: 15px;"
            color="coko-blue"
            @click="addChapter()"
            :text="!(mobileDisplay) && 'Новый раздел'"
          />
      </div>

      <div v-if="!(['yourself', null].includes(kug.on_edit))">
          КУГ на редактировании: <b>{{kug.on_edit}}</b>
      </div>

      <v-data-table
              sticky
              :key="tableKey"
              class="adaptive-kug-table"
              style="overflow: auto;"
              :headers="headers"
              :mobile-breakpoint="960"
              :items="chapters.sort((a, b) => a.position - b.position)"
              :loading="tableLoading"
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
                        v-if="!(['position', 'actions'].includes(column.key))"
                      >
                          <b
                            style="cursor: pointer"
                          >
                            {{column.title}}
                          </b>

                      </td>

                      <td
                        style="
                          text-align: center;
                          background-color: #373c59;
                          color: white;
                        "
                        v-if="(['position', 'actions'].includes(column.key) && (kugEdit))"
                      >
                          <b
                            style="cursor: pointer"
                          >
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
                        v-if="!(['position', 'actions'].includes(header.key))"
                        style="text-align: center; cursor: pointer"
                        @click="changeChapterThemeShow(item.object_id)"
                      >

                          <div v-if="mobileDisplay" class="v-data-table__td-title">{{header.title}}</div>

                          <template v-if="!(['position', 'name', 'object_id', 'program', 'actions'].includes(header.key))">

                              <p
                                v-if="header.key.includes('hour')"
                                v-bind:class="[
                                  checkHoursSum('chapter', header.key, item.object_id) ? 'sum_correct' : 'sum_incorrect'
                                ]"
                              >
                                {{ item[header.key] }}
                              </p>

                              <p
                                v-if="!(header.key.includes('hours'))"
                              >
                                {{ item[header.key] }}
                              </p>


                          </template>

                          <template v-if="header.key === 'name'">
                              Раздел {{item['position']}}. {{item['name']}}
                          </template>

                      </td>

                      <td
                        v-if="(['position', 'actions'].includes(header.key)) && kugEdit"
                        style="text-align: center;"
                      >

                          <div v-if="mobileDisplay" class="v-data-table__td-title">{{header.title}}</div>

                          <template v-if="header.key === 'position'">

                              <div style="display: inline-block">
                                  <div>
                                      <v-icon
                                        style="display: inline-block"
                                        icon="mdi-arrow-up-drop-circle"
                                        color="coko-blue"
                                        @click="changeChapterPosition('up', item.object_id)"
                                      />
                                  </div>
                                  <div>
                                      <v-icon
                                        style="display: inline-block"
                                        icon="mdi-arrow-down-drop-circle"
                                        color="coko-blue"
                                        @click="changeChapterPosition('down', item.object_id)"
                                      />
                                  </div>

                              </div>


                          </template>

                          <template v-if="header.key === 'actions'">

                              <div style="display: inline-block">

                                  <v-icon
                                    icon="mdi-plus"
                                    color="coko-blue"
                                    @click="addTheme(item.object_id)"
                                  />
                                  <v-icon
                                    icon="mdi-pencil"
                                    color="coko-blue"
                                    @click="openEditItem('chapter', null, item)"
                                  />
                                  <v-icon
                                    icon="mdi-delete"
                                    color="coko-blue"
                                    @click="deleteItem('chapter', null, item.object_id)"
                                  />
                              </div>
                          </template>

                      </td>

                  </template>

              </tr>

              <template v-if="openChapter.filter((chapter) => chapter.chapter_id === item.object_id)[0].open">

                  <tr
                    v-bind:class="{'v-data-table__tr v-data-table__tr--mobile': mobileDisplay}"
                    v-for="theme in item.themes.sort((a, b) => a.position - b.position)"
                  >

                      <template v-for="header in headers">

                          <div v-if="mobileDisplay" class="v-data-table__td-title">{{header.title}}</div>

                          <td
                            v-if="!(['position', 'actions'].includes(header.key))"
                            style="text-align: center; background-color: #373c59; color: white;"
                          >

                              <div v-if="mobileDisplay" class="v-data-table__td-title">{{header.title}}</div>

                              <template v-if="!(['position', 'name', 'object_id', 'program', 'actions'].includes(header.key))">

                                  <p
                                    v-if="header.key === 'total_hours'"
                                    v-bind:class="[
                                      checkHoursSum('theme', null, theme.object_id) ? 'sum_correct' : 'sum_incorrect'
                                    ]"
                                  >
                                      {{ theme[header.key] }}
                                  </p>

                                  <p
                                    v-if="!(header.key === 'total_hours')"
                                  >
                                      {{ theme[header.key] }}
                                  </p>

                              </template>

                              <template v-if="header.key === 'name'">

                                  Тема {{ theme['position'] }}. {{ theme['name'] }}

                              </template>

                          </td>

                          <td
                            v-if="(['position', 'actions'].includes(header.key)) && kugEdit"
                            style="text-align: center; background-color: #373c59; color: white;"
                          >
                              <template v-if="header.key === 'position'">

                                  <div style="display: inline-block">
                                      <div>
                                          <v-icon
                                            style="display: inline-block"
                                            icon="mdi-arrow-up-drop-circle"
                                            @click="changeThemePosition('up', item.object_id, theme.object_id)"
                                          />
                                      </div>
                                      <div>
                                          <v-icon
                                            style="display: inline-block"
                                            icon="mdi-arrow-down-drop-circle"
                                            @click="changeThemePosition('down', item.object_id, theme.object_id)"
                                          />
                                      </div>

                                  </div>

                              </template>

                              <template v-if="header.key === 'actions'">

                                  <v-icon
                                    icon="mdi-pencil"
                                    @click="openEditItem('theme', item.object_id, theme)"
                                  />

                                  &nbsp;&nbsp;

                                  <v-icon
                                    icon="mdi-delete"
                                    @click="deleteItem('theme', item.object_id, theme.object_id)"
                                  />
                              </template>

                          </td>

                      </template>

                  </tr>

              </template>

          </template>

          <template v-slot:loading>
              <v-skeleton-loader :type="'table-row@10'"></v-skeleton-loader>
          </template>

          <template v-slot:bottom></template>

      </v-data-table>

  </div>

  <v-dialog
      persistent
      v-model="editDialog"
  >

    <v-card>

      <v-card-title class="d-flex justify-space-between align-center">
        Редактирование элемента
        <v-btn
            icon="mdi-close"
            color="coko-blue"
            @click="editDialog = !(editDialog)"
        />
      </v-card-title>

      <v-card-text>
        <v-row dense>
          <v-col
              cols="12"
              md="4"
              sm="6"
          >
            <v-text-field
                v-model="editElement.name"
                bg-color="white"
                label="Наименование"
                variant="solo"
                clearable
            />
          </v-col>

          <v-col
              cols="12"
              md="4"
              sm="6"
          >
            <v-text-field
                v-model="editElement.total_hours"
                type="number"
                bg-color="white"
                label="Всего часов"
                variant="solo"
                clearable
            />
          </v-col>

          <v-col
              cols="12"
              md="4"
              sm="6"
          >
            <v-text-field
                v-model="editElement.lecture_hours"
                type="number"
                bg-color="white"
                label="Лекционных часов"
                variant="solo"
                clearable
            />
          </v-col>

          <v-col
              cols="12"
              md="4"
              sm="6"
          >
            <v-text-field
                v-model="editElement.practice_hours"
                type="number"
                bg-color="white"
                label="Часов практики"
                variant="solo"
                clearable
            />
          </v-col>

          <v-col
              cols="12"
              md="4"
              sm="6"
          >
            <v-text-field
                v-model="editElement.trainee_hours"
                type="number"
                bg-color="white"
                label="Часов стажировки"
                variant="solo"
                clearable
            />
          </v-col>

          <v-col
              cols="12"
              md="4"
              sm="6"
          >
            <v-text-field
                v-model="editElement.individual_hours"
                type="number"
                bg-color="white"
                label="Часов сам. работы"
                variant="solo"
                clearable
            />
          </v-col>

          <v-col
              cols="12"
              md="4"
              sm="6"
          >
            <v-text-field
                v-model="editElement.control_form"
                bg-color="white"
                label="Форма контроля"
                variant="solo"
                clearable
            />
          </v-col>
        </v-row>

      </v-card-text>

      <v-card-actions
        style="background-color: white"
      >

        <v-spacer></v-spacer>

        <v-btn
          color="coko-blue"
          text="Сохранить"
          @click="saveElement()"
        ></v-btn>
      </v-card-actions>

    </v-card>

  </v-dialog>
</template>

<script>
import {v4 as uuidv4} from 'uuid';
import PaginationTableBaseField from "@/components/tables/pagination_table/PaginationTableBaseField.vue";
import SpecialField from "@/components/tables/pagination_table/special_fields/SpecialField.vue";
import PaginationTableManage from "@/components/tables/pagination_table/PaginationTableManage.vue";
import {useDisplay} from "vuetify";
import {apiRequest} from "@/commons/api_request";
import {showAlert} from "@/commons/alerts";

// Компонент для работы с КУГ ДПП
export default {
  name: "KUGTable",
  components: {PaginationTableManage, SpecialField, PaginationTableBaseField},
  props: {
    programId: String, // object_id ДПП
  },
  data() {
    return {
      tableLoading: true, // Отображение индикатора загрузки в таблице
      tableKey: 0,
      mobileDisplay: useDisplay().smAndDown, // Проверка на дисплей мобильного устройства
      headers: [
        {
          'title': 'Наименование темы/раздела',
          'key': 'name'
        },
        {
          'title': 'Всего часов',
          'key': 'total_hours'
        },
        {
          'title': 'Лекция',
          'key': 'lecture_hours'
        },
        {
          'title': 'Практика',
          'key': 'practice_hours'
        },
        {
          'title': 'Стажировка',
          'key': 'trainee_hours'
        },
        {
          'title': 'Самостоятельная работа',
          'key': 'individual_hours'
        },
        {
          'title': 'Форма контроля',
          'key': 'control_form'
        },
        {
          'title': 'Позиция',
          'key': 'position'
        },
        {
          'title': 'Действия',
          'key': 'actions'
        }
      ], // Заголовки таблицы
      kug: null, // Объект КУГ, получение с сервера
      kugEdit: false, // Параметр редактирования КУГ
      chapters: null, // Список разделов КУГ
      openChapter: null, // Массив с параметрами раскрытия строк с темами раздела в таблице
      editDialog: false,
      editElement: {
        'type': 'chapter',
        'chapter_id': null,
        'position': 0,
        'name': '',
        "total_hours": 0,
        "lecture_hours": 0,
        "practice_hours": 0,
        "trainee_hours": 0,
        "individual_hours": 0,
        "control_form": "",
      } // Редактируемый объект
    }
  },
  methods: {
    // Получение объекта КУГ
    async initialize() {
      let kugRequest = await apiRequest(
        '/backend/api/v1/edu/kug/'+this.programId+'/',
        'GET',
        true,
        null
      )
      if (kugRequest.error) {
        showAlert(
          'error',
          'Получение КУГ',
          kugRequest.error
        )
      } else {
        this.kug = kugRequest
        this.kugEdit = this.kug.on_edit === 'yourself'
      }
    },
    // Отобразить/скрыть строки тем для раздела
    changeChapterThemeShow(chapter_id) {
      let param = this.openChapter.filter((chapter) => chapter.chapter_id === chapter_id)[0].open
      this.openChapter.filter((chapter) => chapter.chapter_id === chapter_id)[0].open = !(param)
    },
    // Проверка сумм часов (true - сумма верна, false - сумма не верна
    checkHoursSum(level, type, id) {
      if (level === 'chapter') {
        let chapter = this.chapters.filter((ch) => ch.object_id === id)[0]
        let existSum = Number(chapter[type])
        let sum = 0
        chapter.themes.map((theme) => {
          sum += Number(theme[type])
        })
        return existSum === sum
      } else {
        let theme = null
        this.kug.chapters.map((chapter) => {
          chapter.themes.map((th) => {
            if (th.object_id === id) {
              theme = th
            }
          })
        })
        let sum = 0
        let hoursTypes = Object.keys(theme).filter((key) =>((key.includes('hours')) && (key !== 'total_hours')))
        hoursTypes.map((t) => {
          sum += Number(theme[t])
        })
        return Number(theme['total_hours']) === sum
      }
    },
    // Отправка запроса на редактирование КУГ
    async kugEditRequest() {
        this.tableLoading = true
        let onEditRequest = await apiRequest(
            '/backend/api/v1/edu/program/set_kug_edit/'+this.programId+'/',
            'GET',
            true,
            null,
            true
        )
        if (onEditRequest.status !== 200) {
            showAlert(
                'error',
                'Запрос на редактирование КУГ',
                'Произошла ошибка, повторите попытку позже'
            )
        } else {
            await this.initialize()
        }
    },
    // Изменение позиции раздела
    changeChapterPosition(next, object_id) {
        let chapter = this.chapters.filter((ch) => ch.object_id === object_id)[0]
        if (((chapter.position === 1) && (next === 'up')) ||
            ((chapter.position === this.chapters.length) && (next === 'down'))) {
            return false
        }
        if (next === 'up') {
            this.chapters.filter((ch) => ch.position === chapter.position-1)[0].position += 1
            this.chapters.filter((ch) => ch.object_id === object_id)[0].position -= 1
        } else {
            this.chapters.filter((ch) => ch.position === chapter.position+1)[0].position -= 1
            this.chapters.filter((ch) => ch.object_id === object_id)[0].position += 1
        }
    },
    // Изменение позиции темы раздела
    changeThemePosition(next, chapter_id, object_id) {
        let chapter = this.chapters.filter((ch) => ch.object_id === chapter_id)[0]
        let theme = chapter.themes.filter((th) => th.object_id === object_id)[0]
        if (((theme.position === 1) && (next === 'up')) ||
            ((theme.position === chapter.themes.length) && (next === 'down'))) {
            return false
        }
        let useTheme = null
        if (next === 'up') {
            useTheme = chapter.themes.filter((ch) => ch.position === theme.position-1)[0]
            useTheme.position += 1
            theme.position -= 1
        } else {
            useTheme = chapter.themes.filter((ch) => ch.position === theme.position+1)[0]
            useTheme.position -= 1
            theme.position += 1
        }
  },
    // Добавление нового раздела
    addChapter() {
        let uuid4 = uuidv4()
        this.openChapter.push({
          "chapter_id": uuid4,
          "open": false
        })
        this.chapters.push({
          "object_id": uuid4,
          "themes":[],
          "program": this.programId,
          "position": this.chapters.length+1,
          "name": "Новый раздел",
          "total_hours": 0,
          "lecture_hours": 0,
          "practice_hours": 0,
          "trainee_hours": 0,
          "individual_hours": 0,
          "control_form": ""
        })
    },
    // Добавление новой темы раздела
    addTheme(chapter_id) {
      let uuid4 = uuidv4()
      this.chapters.filter((ch) => ch.object_id === chapter_id)[0].themes.push({
        "object_id": uuid4,
        "position": this.chapters.filter((ch) => ch.object_id === chapter_id)[0].themes.length+1,
        "name": "Новая тема",
        "total_hours": 0,
        "lecture_hours": 0,
        "practice_hours": 0,
        "trainee_hours": 0,
        "individual_hours": 0,
        "control_form": "",
        "chapter": chapter_id
      })
      this.openChapter.filter((ch) => ch.chapter_id === chapter_id)[0].open = true
    },
    // Удаление раздела/темы
    deleteItem(type, chapter_id, object_id) {
      if (confirm('Вы действительно хотите удалить элемент?')) {
        let deletedPosition = 0
        switch(type) {
          case 'chapter':
            deletedPosition = this.chapters.filter((ch) => ch.object_id === object_id)[0].position
            this.chapters.filter((ch) => ch.position > deletedPosition).map((ch) => {
              ch.position -=1
            })
            this.chapters = this.chapters.filter((ch) => ch.object_id !== object_id)
            this.openChapter = this.openChapter.filter((ch) => ch.object_id !== object_id)
            break

          default:
            deletedPosition = this.chapters.filter((ch) => ch.object_id === chapter_id)[0].themes.filter(
                (th) => th.object_id === object_id
            )[0].position
            this.chapters.filter((ch) => ch.object_id === chapter_id)[0].themes.filter(
                (th) => th.position > deletedPosition
            ).map((th) => {
              th.position -=1
            })
            this.chapters.filter((ch) => ch.object_id === chapter_id)[0].themes =
                this.chapters.filter((ch) => ch.object_id === chapter_id)[0].themes.filter(
                    (th) => th.object_id !== object_id
                )
        }
      }
    },
    // Редактирование раздела/темы
    openEditItem(type, chapter_id, obj) {
      this.editElement = obj
      this.editElement.type = type
      this.editElement.chapter_id = chapter_id
      this.editDialog = true
    },
    // Сохранение информации по редактируемой теме/разделу
    saveElement() {
      let keys = Object.keys(this.chapters[0])
      keys.map((key) => {
        if (!(['object_id', 'themes', 'program', 'position'].includes(key))) {
          if (this.editElement.type === 'chapter') {
            this.chapters.filter((ch) => ch.object_id === this.editElement.object_id)[0][key] = this.editElement[key]
          } else {
            this.chapters.filter((ch) => ch.object_id === this.editElement.chapter_id)[0].themes.filter(
                (th) => th.object_id === this.editElement.object_id
            )[0][key] = this.editElement[key]
          }
        }
      })
      this.tableKey += 1
      this.editDialog = false
    },
    // Сохранить изменения в КУГ
    async saveKug() {
      this.tableLoading = true
      let body = {
        'program_id': this.programId,
        'chapters': this.chapters
      }
      let saveKugRequest = await apiRequest(
        '/backend/api/v1/edu/kug_update/',
        'POST',
        true,
        body
      )
      if (saveKugRequest.error) {
        showAlert(
          'error',
          'Обновление КУГ',
          saveKugRequest.error
        )
      } else {
        await this.initialize()
      }

    }
  },
  mounted() {
    this.initialize()
  },
  watch: {
    // Проверка кем КУГ редактируется, установка значений
    kug: function() {
      if (this.kug !== null) {
        if (this.kug.on_edit === 'yourself') {
          this.kugEdit = true
        }
        this.chapters = this.kug.chapters
        if (this.openChapter === null) {
            let openChapter = []
            this.chapters.map((chapter) => {
                openChapter.push({
                    'chapter_id': chapter.object_id,
                    'open': false
                })
            })
            this.openChapter = openChapter
        }
        this.tableLoading = false
      }
    }
  }
}
</script>

<style scoped>
.sum_correct {
  color: green;
}

.sum_incorrect {
  color: #FF5722;
}
</style>
