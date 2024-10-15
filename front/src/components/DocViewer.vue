<template>

  <v-skeleton-loader
    v-if="base64String === null"
    type="image"
  />

  <PdfApp
    v-if="(base64String !== null) && (contentType === 'application/pdf')"
    :pdf="base64String"
    style="width: 100%; height: 100%"
  />

  <object
      v-if="base64String !== null && (contentType !== 'application/pdf')"
      style="max-height: 150vh; max-width: 100vw"
      :data="base64String"
      :type="contentType"
  >
    <embed
        :src="base64String"
    />
  </object>

</template>

<script>

// Компонент для просмотра документов
import PdfApp from "vue3-pdf-app"
import "vue3-pdf-app/dist/icons/main.css"
import {apiRequest} from "@/commons/api_request";
import {showAlert} from "@/commons/alerts";
import fileContentTypes from "@/commons/consts/fileContentTypes";

export default {
  name: 'DocViewer',
  components: {
    PdfApp
  },
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
      base64String: null,
      // Тип контента
      contentType: null
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
        let ext = fileRequest.file_name.substring(
            fileRequest.file_name.indexOf('.'),
            fileRequest.file_name.length
        )
        console.log(ext)
        this.contentType = fileContentTypes.filter(
            (type) => type.extension === fileRequest.file_name.substring(
                fileRequest.file_name.length-3, fileRequest.file_name.length
            )
        )[0].mime
        this.base64String = 'data:'+this.contentType+';base64,'+fileRequest.file
      }
    }
  },
  mounted() {
    this.getBase64String()
  }
}

</script>

<style scoped>

</style>