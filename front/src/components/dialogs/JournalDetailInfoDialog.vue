<template>
  <v-dialog
    v-model="dialog"
  >
    <template v-slot:activator="{ props }">
      <v-btn
        v-if="item.payload !== null || item.output !== null"
        prepend-icon="mdi-information-outline"
        color="coko-blue"
        @click="dialog = !(dialog)"
      >
        Просмотр
      </v-btn>
      <p v-if="item.payload === null && item.output === null">
        -
      </p>
    </template>
    <v-card>
      <v-card-title class="d-flex justify-space-between align-center">
        <span class="text-h5">Детальная информация</span>

        <v-btn
          icon="mdi-close"
          color="coko-blue"
          @click="dialog = !(dialog)"
        ></v-btn>
      </v-card-title>

      <v-card-text>
        <v-container>
          <v-row no-gutters>

            <v-col
              cols="12"
              md="12"
              sm="12"
            >
              <v-text-field
                v-model="item.date_create"
                label="Дата создания"
                readonly
              ></v-text-field>
            </v-col>

            <v-col
              cols="12"
              md="12"
              sm="12"
            >
              <v-text-field
                v-model="item.source"
                label="Источник"
                readonly
              ></v-text-field>
            </v-col>

            <v-col
              cols="12"
              md="12"
              sm="12"
            >
              <b>Модуль:</b><br/>
              <JournalModuleBadge :moduleName="item.module" /><br/>
              <br/>
            </v-col>
            <v-col
              cols="12"
              md="4"
              sm="6"
            >
              <b>Статус:</b><br/>
              <JournalRecStatusBadge :recStatus="item.status" /><br/>
              <br/>
            </v-col>

            <v-col
              cols="12"
              md="12"
              sm="12"
            >
              <v-text-field
                v-model="item.description"
                label="Краткое описание"
                readonly
              ></v-text-field>
            </v-col>

            <v-col
              cols="12"
              md="12"
              sm="12"
            >
              <v-textarea
                :model-value="item.payload"
                label="Полезная нагрузка"
                readonly
              />
            </v-col>

            <v-col
              cols="12"
              md="12"
              sm="12"
            >
              <v-textarea
                :model-value="item.output"
                label="Выходные данные"
                readonly
              />
            </v-col>
          </v-row>
        </v-container>
      </v-card-text>

    </v-card>
  </v-dialog>
</template>

<script>
import JournalModuleBadge from "@/components/badges/journal/JournalModuleBadge.vue";
import JournalRecStatusBadge from "@/components/badges/journal/JournalRecStatusBadge.vue";

export default {
  name: "JournalDetailInfoDialog",
  components: {JournalRecStatusBadge, JournalModuleBadge},
  props: {
    item: Object, //Переданная запись журнала событий
  },
  data() {
    return {
      dialog: false,
    }
  }
}
</script>

<style scoped>

</style>
