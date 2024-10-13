<template>

  <a
      :download="fileName"
      :href="'data:'+fileContentTypes.filter(
          (type) => type.extension === fileName.substring(fileName.length-3, fileName.length)
          )[0].mime+';base64,'+file"
  >
    <template
        v-if="fileName.length > 15"
    >
      {{fileName.substring(0, 10)}}.{{fileName.substring(fileName.length-3, fileName.length)}}
    </template>
    <template
      v-if="fileName.length <= 15"
    >
      {{fileName}}
    </template>
  </a>

</template>

<script>

// Блок для скачивания файла в формате base64
import fileContentTypes from "@/commons/consts/fileContentTypes";

export default {
  name: 'FileField',
  props: {
    // Наименование файла
    fileName: String,
    // Файл
    file: String,
  },
  data() {
    return {
      // Список типов контента
      fileContentTypes: fileContentTypes
    }
  }
}

</script>

<style scoped>

</style>