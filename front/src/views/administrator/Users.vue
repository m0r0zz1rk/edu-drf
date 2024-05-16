<template>
  <LkPage :usePreLoader="usePreLoader">
    <slot>
      <v-card
        variant="outlined"
      >
        <v-card-text>
          <div style="background-color: white; overflow: auto;" class="adaptive-no-tab-table-card-text">
            <v-tabs class="guides-tabs"
                    v-model="guidesTab"
                    bg-color="coko-blue"
                    show-arrows
            >
              <v-tab class="coko-tab" value="user">Обучающиеся</v-tab>
              <v-tab class="coko-tab" value="coko">Сотрудники</v-tab>

            </v-tabs>

            <StudentUsers v-if="guidesTab === 'user'" />

            <CokoUsers v-if="guidesTab === 'coko'" />



          </div>
        </v-card-text>
      </v-card>
    </slot>
  </LkPage>
</template>

<script>
import StudentUsers from "@/views/administrator/users/StudentUsers.vue";
import LkPage from "@/components/LkPage.vue";
import CokoUsers from "@/views/administrator/users/CokoUsers.vue";

export default {
  name: "Users",
  components: {CokoUsers, LkPage, StudentUsers},
  props: {
    usePreLoader: Function,
  },
  data() {
    return {
      guidesTab: 'user'
    }
  },
  mounted() {
    this.usePreLoader(true)
  }
}
</script>

<style scoped>

</style>
