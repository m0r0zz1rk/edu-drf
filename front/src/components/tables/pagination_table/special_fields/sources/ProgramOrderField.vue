<template>
  {{ item.order_number }}<br/>
  <v-icon
    v-if="item.order_number !== '-'"
    icon="mdi-tray-arrow-down"
    @click="downloadFile()"
  />

</template>

<script>
import {showAlert} from "@/commons/alerts";
import {apiRequest} from "@/commons/apiRequest";
import contentTypeFormats from "@/commons/consts/contentTypeFormats";

export default {
  name: "ProgramOrderField",
  props: {
    item: Object, // Полученная запись с пагинационной таблицы
  },
  methods: {
    async downloadFile() {
      showAlert(
        'success',
        'Скачивание приказа',
        'Загрузка файла скоро начнется, ожидайте...'
      )
      let orderRequest = await apiRequest(
        '/backend/api/v1/edu/program/order_file/'+this.item.object_id+'/',
        'GET',
        true,
        false,
        true
      )
      let contentType = orderRequest.headers.get('Content-Type')
      let getBlob = await orderRequest.blob();
      let url = window.URL.createObjectURL(getBlob);
      var a = document.createElement('a');
      a.href = url;
      a.download = this.item.order_number+contentTypeFormats[contentType];
      document.body.appendChild(a);
      a.click();
      a.remove();
    }
  }
}
</script>

<style scoped>

</style>
