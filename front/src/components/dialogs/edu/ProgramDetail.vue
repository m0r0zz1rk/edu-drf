<template>

  <v-dialog
    persistent
    v-model="dialog"
  >

    <v-card class="lk-full-page-card">
      <v-card-title class="d-flex justify-space-between align-center">
        <v-tabs class="guides-tabs"
                v-model="programTab"
                bg-color="coko-blue"
                show-arrows
        >

          <v-tab
            class="coko-tab"
            value="info"
          >
            Информация
          </v-tab>

          <v-tab
            class="coko-tab"
            value="order"
          >
            Приказ
          </v-tab>

          <v-tab
            v-if="programObjectID"
            class="coko-tab"
            value="kug"
          >
            КУГ
          </v-tab>

        </v-tabs>

        <v-btn
          icon="mdi-close"
          color="coko-blue"
          @click="dialog = !(dialog)"
        ></v-btn>
      </v-card-title>

      <v-card-text>
        <v-container>

          <template v-if="programTab === 'info'">

            <v-row
              dense
            >

              <v-col
                cols="12"
                md="6"
                sm="6"
              >
                <v-select
                  :items="adCentres"
                  v-model="programObject.department"
                  label="Подразделение"
                  :loading="loading"
                />
              </v-col>

              <v-col
                cols="12"
                md="6"
                sm="6"
              >
                <v-text-field
                  v-model="programObject.name"
                  label="Наименование"
                  :loading="loading"
                />
              </v-col>

              <v-col
                cols="12"
                md="6"
                sm="6"
              >
                <v-text-field
                  v-model="programObject.type"
                  label="Тип"
                  :loading="loading"
                />
              </v-col>

              <v-col
                cols="12"
                md="6"
                sm="6"
              >
                <v-number-input
                  controlVariant="split"
                  label="Объем (часов)"
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
                <v-select
                  clearable
                  chips
                  multiple
                  label="Категории слушателей"
                  :items="audienceCategories"
                  v-model="programObject.categories"
                  :loading="loading"
                />
              </v-col>

              <v-col
                cols="12"
                md="6"
                sm="6"
              >
                <v-number-input
                  controlVariant="split"
                  label="Цена (рублей)"
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
                  label="Аннотация"
                  v-model="programObject.annotation"
                  clearable
                  :loading="loading"
                />
              </v-col>

            </v-row>

          </template>

          <template v-if="programTab === 'order'">

            <v-row
              dense
            >

              <v-col
                cols="12"
                md="6"
                sm="6"
              >
                <v-text-field
                  v-model="orderObject.number"
                  label="Номер приказа"
                  :loading="loading"
                />
              </v-col>

              <v-col
                cols="12"
                md="6"
                sm="6"
              >
                <v-text-field
                  v-model="orderObject.number"
                  label="Дата приказа"
                  :loading="loading"
                />
              </v-col>

              <v-col
                cols="12"
                md="6"
                sm="6"
              >
                <v-date-input
                  bg-color="white"
                  label="Дата приказа"
                  v-model="orderObject.date"
                  prepend-icon=""
                  prepend-inner-icon="$calendar"
                  variant="solo"
                  :loading="loading"
                  clearable
                />
              </v-col>

              <v-col
                cols="12"
                md="6"
                sm="6"
              >
                <v-file-input
                  label="File input"
                />
              </v-col>

            </v-row>

          </template>

        </v-container>

        <v-alert
          id="error-program-detail-alert"
          class="alert-hidden"
          style="width: 100%"
          :text="programDetailError"
          type="error"
        ></v-alert>

      </v-card-text>

      <v-card-actions style="background-color: white">

        <v-spacer></v-spacer>

        <v-btn
          color="coko-blue"
          :text="programObjectID ? 'Сохранить' : 'Добавить'"
          :loading="loading"
          @click="saveProgram()"
        ></v-btn>
      </v-card-actions>

    </v-card>

  </v-dialog>

</template>

<script>
import {apiRequest} from "@/commons/api_request";
import {showAlert} from "@/commons/alerts";

export default {
  name: "ProgramDetail",
  props: {
    programObjectID: String, // object_id ДПП (если редактирование объекта),
    adCentres: Array, // Список подразделений AD,
    audienceCategories: Array // Список категорий слушателей
  },
  data() {
    return {
      dialog: false,
      loading: true,
      programTab: 'info',
      programObject: null,
      orderObject: {
        'number': '',
        'date': '',
        'file': null,
      },
      programDetailError: ''
    }
  },
  methods: {
    setProgramObject() {
      if (this.programObjectID) {

      } else {
        this.programObject = {
          'department': '',
          'name': '',
          'type': '',
          'duration': 0,
          'categories': [],
          'annotation': '',
          'price': 0
        }
      }
    },
    async saveProgram() {

    }
  },
  mounted() {
    this.setProgramObject()
    this.loading = false
  }
}
</script>

<style scoped>
  @import '../../../assets/css/alerts.css';
</style>
