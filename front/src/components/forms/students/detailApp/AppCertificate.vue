<template>

  <v-btn color="coko-blue" text="Просмотр" @click="$refs.docViewerDialog.dialog = true"/>

  <CokoDialog ref="docViewerDialog">
    <template v-slot:title>Просмотр удостоверения</template>
    <template v-slot:text><DocViewer fileType="student" :fileId="certificateId"/></template>
  </CokoDialog>

</template>

<script>
import CokoDialog from "@/components/dialogs/CokoDialog.vue";
import DocViewer from "@/components/DocViewer.vue";

export default {
  name: "AppCertificate",
  components: {DocViewer, CokoDialog},
  props: {
    // object_id скана серитфиката
    certificateId: String
  }
}
</script>


<style scoped>

</style>
