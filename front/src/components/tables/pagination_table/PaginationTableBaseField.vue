<template>
  <div v-if="showField">

    <v-text-field
      v-if="['input', 'dppOrder', 'appStudentInfo'].includes(field.ui)"
      :type="field.type"
      :v-mask="
        ['phone', 'snils'].includes(field.ui) &&
          field.ui === 'snils' ?
            '###-###-### ##'
            :
            '+7 (###) ###-##-##'
      "
      v-model="localValue"
      :label="fieldTitle ?
                !checkRequired ?
                  fieldTitle
                  :
                  field.addRequired ?
                    fieldTitle+'*'
                    :
                    fieldTitle
              :
              ''
      "
      :disabled="field.readOnly"
      @change="e => onChangeEvent(field.key, localValue)"
    />

    <v-text-field
      v-if="field.ui === 'phone'"
      v-mask="'+7 (###) ###-##-##'"
      v-model="localValue"
      :label="fieldTitle ?
                !checkRequired ?
                  fieldTitle
                  :
                  field.addRequired ?
                    fieldTitle+'*'
                    :
                    fieldTitle
              :
              ''
      "
      :disabled="field.readOnly"
      @change="e => onChangeEvent(field.key, localValue)"
    />

    <v-text-field
      v-if="field.ui === 'snils'"
      v-mask="'###-###-### ##'"
      v-model="localValue"
      :label="fieldTitle ?
                !checkRequired ?
                  fieldTitle
                  :
                  field.addRequired ?
                    fieldTitle+'*'
                    :
                    fieldTitle
              :
              ''
      "
      :disabled="field.readOnly"
      @change="e => onChangeEvent(field.key, localValue)"
    />

    <v-select
      v-if="['select', 'journalModule', 'journalRecStatus', 'studentGroupStatus'].includes(field.ui)"
      :items="[
        '',
        ...field.items
      ]"
      v-model="localValue"
      :label="fieldTitle ?
                !checkRequired ?
                  fieldTitle
                  :
                  field.addRequired ?
                    fieldTitle+'*'
                    :
                    fieldTitle
              :
              ''
      "
      :disabled="field.readOnly"
      @update:modelValue="e => {
        try {
          onChangeEvent(field.key, localValue)
        } catch (e) {}
      }"
    />

    <v-date-input
      v-if="field.ui === 'date'"
      v-model="localValue"
      :label="fieldTitle ?
                !checkRequired ?
                  fieldTitle
                  :
                  field.addRequired ?
                    fieldTitle+'*'
                    :
                    fieldTitle
              :
              ''
      "
      :disabled="field.readOnly"
      prepend-icon=""
      prepend-inner-icon="$calendar"
      @update:modelValue="e => {
        if (onChangeEvent) {
          onChangeEvent(field.key, convertDateToBackend(this.localValue))
        }
      }"
      @click:clear="e => {this.localValue = null; onChangeEvent(field.key, '')}"
      clearable
    ></v-date-input>

    <v-file-input
      v-if="field.ui === 'file'"
      :accept="acceptExt"
      label="Выберите документ"
      id="addDialogFileInput"
      :disabled="field.readOnly"
      v-model="localValue"
    />
  </div>
</template>

<script>
import {convertDateToBackend} from "@/commons/date";
import fileContentTypes from "@/commons/consts/fileContentTypes";

export default {
  name: "PaginationTableBaseField",
  props: {
    useInTableManage: Boolean, // Параметр вызова компонента из PaginationTableManage
    checkRequired: Boolean, // Параметр, отображющий необходимость проверки обязательного заполнения
    field: Object, // Объект fieldsArray
    value: String, // Значение (при редактировании записи)
    fieldTitle: String, // Наименование поля
    onChangeEvent: Function, //Функция, вызываемая при изменении
    // Функция получения записей в таблице
    getRecs: Function
  },
  data() {
    return {
      // Список разрешенных расширений файлов (для file)
      acceptExt: '',
      localValue: '',
      showField: false,
    }
  },
  methods: {
    // Формирование строки с разрешенными расширениями файлов
    createAcceptExt() {
      let str = ''
      fileContentTypes.map((fct) => {
        str += fct.mime+', '
      })
      this.acceptExt = str.substring(0, str.length-2)
    },
    convertDateToBackend,
    checkUiDate() {
      try {
        if (this.field.ui === 'date') {
          this.localValue = null
        }
      } catch(e) {
        console.log(e)
      }
    },
  },
  mounted() {
    this.createAcceptExt()
    if (this.value) {
        this.localValue = this.value
    }
    if (this.useInTableManage) {
        this.showField = this.useInTableManage
    }
    this.checkUiDate()
  }
}
</script>

<style scoped>

</style>
