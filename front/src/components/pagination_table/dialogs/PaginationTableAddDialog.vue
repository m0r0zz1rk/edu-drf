<template>
  <v-dialog
    v-model="newItemDialog"
  >
    <template v-slot:activator="{ props }">

      <v-btn
        :icon="mobileDisplay && 'mdi-plus'"
        :prepend-icon="!(mobileDisplay) && 'mdi-plus'"
        color="coko-blue"
        :text="!(mobileDisplay) && 'Добавить'"
        @click="newItemDialog = !(newItemDialog)"
      />

    </template>
    <v-card>
      <v-card-title>
        <span class="text-h5">Новый элемент</span>
      </v-card-title>

      <v-card-text>
        <v-container>
          <v-row>
            <v-col
              cols="12"
              md="4"
              sm="6"
            >
              <v-text-field
                v-model="editedItem.name"
                label="Dessert name"
              ></v-text-field>
            </v-col>
            <v-col
              cols="12"
              md="4"
              sm="6"
            >
              <v-text-field
                v-model="editedItem.calories"
                label="Calories"
              ></v-text-field>
            </v-col>
            <v-col
              cols="12"
              md="4"
              sm="6"
            >
              <v-text-field
                v-model="editedItem.fat"
                label="Fat (g)"
              ></v-text-field>
            </v-col>
            <v-col
              cols="12"
              md="4"
              sm="6"
            >
              <v-text-field
                v-model="editedItem.carbs"
                label="Carbs (g)"
              ></v-text-field>
            </v-col>
            <v-col
              cols="12"
              md="4"
              sm="6"
            >
              <v-text-field
                v-model="editedItem.protein"
                label="Protein (g)"
              ></v-text-field>
            </v-col>
          </v-row>
        </v-container>
      </v-card-text>

      <v-card-actions>
        <v-spacer></v-spacer>
        <v-btn
          color="blue-darken-1"
          variant="text"
          @click="close"
        >
          Cancel
        </v-btn>
        <v-btn
          color="blue-darken-1"
          variant="text"
          @click="save"
        >
          Save
        </v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<script>
export default {
  name: "PaginationTableAddDialog",
  props: {
    mobileDisplay: Boolean, // Отображение на мобильном устройстве
  },
  data() {
    return {
      newItemDialog: false
    }
  }
}
</script>

<style scoped>

</style>
