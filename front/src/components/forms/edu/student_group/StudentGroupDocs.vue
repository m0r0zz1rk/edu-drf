<template>

  <v-expansion-panels
    style="padding-top: 10px"
    variant="accordion"
    color="coko-blue"
  >

    <v-expansion-panel
      color="coko-blue"
      title="Информационное письмо"
    >

      <v-expansion-panel-text>

        <v-btn
          color="coko-blue"
          :loading="loading"
          @click="e => {getDoc('information_letter', 'docx')}"
        >
          Сформировать
        </v-btn>

      </v-expansion-panel-text>

    </v-expansion-panel>

    <v-expansion-panel
      color="coko-blue"
      title="Документы об оказании услуги"
    >

      <v-expansion-panel-text>

        <v-row
        dense
      >

        <v-col
          cols="12"
          md="6"
          sm="6"
        >

          <v-btn
            color="coko-blue"
            :loading="loading"
            @click="e => {getDoc('service_memo', 'docx')}"
          >
            Сформировать СЗ
          </v-btn>

        </v-col>

        <v-col
          cols="12"
          md="6"
          sm="6"
        >

          <v-btn
            color="coko-blue"
            :loading="loading"
            @click="e => {getDoc('service_order', 'docx')}"
          >
            Сформировать приказ
          </v-btn>

        </v-col>

      </v-row>

      </v-expansion-panel-text>

    </v-expansion-panel>

    <v-expansion-panel
      color="coko-blue"
      title="Договор оферты"
    >

      <v-expansion-panel-text>

        <v-row
          dense
        >

          <v-col
            cols="12"
            md="4"
            sm="6"
          >

            <v-btn
              color="coko-blue"
              :loading="loading"
              @click="e => {getDoc('offer_project', 'docx')}"
            >
              Сформировать проект
            </v-btn>

          </v-col>

          <v-col
            cols="12"
            md="4"
            sm="6"
          >

            <v-btn
              color="coko-blue"
              :loading="loading"
            >
              Загрузить скан
            </v-btn>

          </v-col>

          <v-col
            cols="12"
            md="4"
            sm="6"
          >

            <v-btn
              color="coko-blue"
              :loading="loading"
            >
              Скачать
            </v-btn>

          </v-col>

        </v-row>

      </v-expansion-panel-text>

    </v-expansion-panel>

    <v-expansion-panel
      v-if="serviceType === 'ou'"
      color="coko-blue"
      title="Приказы"
    >

      <v-expansion-panel-text>

        <v-row
            dense
        >

          <v-col
              cols="12"
              md="4"
              sm="6"
          >

            <v-btn
              color="coko-blue"
              :loading="loading"
              @click="e => {getDoc('transfer_order', 'docx')}"
            >
              О зачислении
            </v-btn>

          </v-col>

          <v-col
              cols="12"
              md="4"
              sm="6"
          >

            <v-btn
              color="coko-blue"
              :loading="loading"
              @click="e => {getDoc('deduction_order', 'docx')}"
            >
              Об отчислении
            </v-btn>

          </v-col>

        </v-row>

      </v-expansion-panel-text>

    </v-expansion-panel>

    <v-expansion-panel
      color="coko-blue"
      title="Анкеты"
    >

      <v-expansion-panel-text>

        <v-btn
          color="coko-blue"
          :loading="loading"
          @click="e => {getDoc('forms', 'xlsx')}"
        >
          Скачать
        </v-btn>

      </v-expansion-panel-text>

    </v-expansion-panel>

    <v-expansion-panel
      color="coko-blue"
      title="Журнал"
    >

      <v-expansion-panel-text>

        <v-btn
          color="coko-blue"
          :loading="loading"
        >
          Скачать
        </v-btn>

      </v-expansion-panel-text>

    </v-expansion-panel>

  </v-expansion-panels>

</template>

<script>
// Компонент для формирования документов по учебной группе
import {apiRequest} from "@/commons/api_request";
import {studentGroupDocTypes} from "@/commons/consts/edu/studentGroupDocTypes";
import {showAlert} from "@/commons/alerts";

export default {
  name: "StudentGroupDocs",
  props: {
    groupId: String, // object_id учебной группы
    serviceType: String, // Тип услуги учебной группы
    code: String, // Код учебной группы
  },
  data() {
    return {
      // Индикатор загрузки на элементах формы
      loading: false
    }
  },
  methods: {
    // Формирование запроса на получение документа запрашиваемого типа
    async getDoc(type, extension) {
      this.loading = true
      let getDocRequest = await apiRequest(
        '/backend/api/v1/edu/student_group/doc/',
        'POST',
        true,
        {group_id: this.groupId, doc_type: type},
        true
      )
      if (getDocRequest.status === 200) {
        let data = await getDocRequest.blob()
        let a = document.createElement('a')
        a.href = window.URL.createObjectURL(data)
        a.download = `${studentGroupDocTypes[type]} ${this.code}.${extension}`
        a.click()
      } else {
        showAlert('error', 'Документ группы', 'Произошла ошибка при получении документа')
      }
      this.loading = false
    }
  },
}
</script>

<style scoped>

</style>
