<template>

  <v-skeleton-loader
    v-if="base64String === null"
    style="height: 100%"
    type="image"
  />

  <div
    id="viewerDiv"
    style="height: 100%; width: 100%"
  >
  </div>

</template>

<script>

// Компонент для просмотра документов
import {apiRequest} from "@/commons/api_request";
import {showAlert} from "@/commons/alerts";
import fileContentTypes from "@/commons/consts/fileContentTypes";

export default {
  name: 'DocViewer',
  props: {
    // Тип файла (student, pay или offer)
    fileType: String,
    // ojbect_id записи БД с файлом
    fileId: String
  },
  data() {
    return {
      // Полученное имя файла с сервера
      fileName: null,
      // Полученный файл с сервера
      file: null,
      // Строка base64
      base64String: null
    }
  },
  methods: {
    // Получение строки base64 для просмотра
    async getBase64String() {
      let fileRequest = await apiRequest(
          '/backend/api/v1/docs/doc_viewer/'+this.fileType+'/'+this.fileId+'/',
          'get',
          true,
          null
      )
      if (fileRequest.error) {
        showAlert(
            'error',
            'Просмотр файла',
            fileRequest.error
        )
      } else {
        this.base64String = 'data:'+fileContentTypes.filter(
            (type) => type.extension === fileRequest.file_name.substring(
                fileRequest.file_name.length-3, fileRequest.file_name.length
            )
        )[0].mime+';base64,'+fileRequest.file
        console.log(this.base64String)
      }
    }
  },
  mounted() {
    this.getBase64String()
  },
  watch: {
    base64String: function(newValue, oldValue) {
      if (newValue !== null) {
        const viewerFrame = document.createElement('iframe')
        viewerFrame.src = this.base64String
        try {
          document.querySelector('#viewerDiv').appendChild(viewerFrame)
        } catch (e) {
          console.log('ABOBA')

        }
      }
    }
  }
}

</script>

<style scoped>

</style>