<template>
  <v-switch
    v-model="selectModel"
    color="coko-blue"
    :label="selectModel"
    :loading="loading"
    false-value="Нет"
    true-value="Да"
    hide-details
    @change="changeCuratorGroup()"
  >
    <template v-slot:label>
      <span v-if="selectModel === 'Да'" style="color: green"><b>Да</b></span>
      <span v-if="selectModel === 'Нет'" style="color: red"><b>Нет</b></span>
    </template>


  </v-switch>
</template>

<script>
import {apiRequest} from "@/commons/apiRequest";
import {showAlert} from "@/commons/alerts";

export default {
  name: "CuratorGroupsField",
  props: {
    item: Object, // Полученная запись с пагинационной таблицы
  },
  data() {
    return {
      selectModel: this.item.curator_groups === true ? 'Да' : 'Нет',
      loading: false,
    }
  },
  methods: {
    async changeCuratorGroup() {
      this.loading = true
      let changeCuratorGroupRequest = await apiRequest(
        '/backend/api/v1/guides/coko/change_curator_groups/',
        'POST',
        true,
        {
          'object_id': this.item.object_id,
          'curator_groups': this.selectModel === 'Да'
        }
      )
      if (changeCuratorGroupRequest.error) {
        showAlert(
          'error',
          'Изменение информации',
          changeCuratorGroupRequest.error
        )
      }
      if (changeCuratorGroupRequest.success) {
        showAlert(
          'success',
          'Изменение информации',
          changeCuratorGroupRequest.success
        )
      }
      this.loading = false
    }
  }
}
</script>

<style scoped>

</style>
