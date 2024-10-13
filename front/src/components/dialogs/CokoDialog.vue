<template>

  <v-dialog
      color="coko-blue"
      v-model="dialog"
      :fullscreen="mobileDisplay"
      persistent
  >

    <v-card
      class="lk-full-page-card"
      color="coko-blue"
      persistent
    >

      <v-card-title
          class="d-flex justify-space-between align-center"
      >

        <slot
            name="title"
        ></slot>

        <v-btn
            icon="mdi-close"
            color="coko-blue"
            @click="dialog = !(dialog)"
        />

      </v-card-title>

      <v-card-text
        style="color: black;"
      >

        <div
          ref="topTextDiv"
        />

          <slot
              name="text"
          ></slot>


      </v-card-text>

      <v-divider></v-divider>

      <v-card-actions
          v-if="cardActions"
          style="background-color: white"
      >

        <v-spacer></v-spacer>

        <slot
            name="actions"
        ></slot>

      </v-card-actions>

    </v-card>

  </v-dialog>

</template>

<script>

// Основной компонент диалогового окна для всех форм
import {useDisplay} from "vuetify";
import BooleanBadge from "@/components/badges/BooleanBadge.vue";

export default {
  name: 'CokoDialog',
  props: {
    // Параметр отображения блока для управляющих кнопок
    cardActions: Boolean,
  },
  data() {
    return {
      // Параметр проверки мобильного устройства
      mobileDisplay: useDisplay().smAndDown,
      // Параметр отображения диалогового окна
      dialog: false,
    }
  },
  methods: {
    // Прокрутить блок с контентом вверх
    scrollTextToTop() {
      this.$refs.topTextDiv.scrollIntoView()
    }
  }
}

</script>

<style scoped>

</style>
<script setup>
</script>