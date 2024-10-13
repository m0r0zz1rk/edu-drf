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
        >
          Скачать
        </v-btn>

      </v-expansion-panel-text>

    </v-expansion-panel>

  </v-expansion-panels>

</template>

<script>
// Компонент для формирования документов по учебной группе
export default {
  name: "StudentGroupDocs",
  props: {
    groupId: String, // object_id учебной группы
    serviceType: String, // Тип услуги учебной группы
  },
}
</script>

<style scoped>

</style>
